from django.views.generic.base import View
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from os import path
import markdown
import logging

import json
from json.decoder import JSONDecodeError


from rest_framework import status
from rest_framework.parsers import JSONParser

from .models import CoinRegister
from .utils import CoinEnum

from exceptions import ChangeError

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name="dispatch")
def index(request):
    
    """ 
    
    This function will retrieve the README documentation and present it when the user navigates to the home page.

    This function will return:
    - HTTP 200: OK (if the README.md file can be found, opened & read)
    - HTTP 404: NOT FOUND (if the RREADME.md file cannot be found - the function will return a prompt for the user to use Docker using basic HTML).
    
    """

    try:

        # Open the README.md file, read the content of the file & convert to HTML
        with open(path.dirname('/code/') + '/README.md', 'r') as markdown_file:
            content = markdown_file.read()
            return HttpResponse(markdown.markdown(content), content_type='text/html')
    
    # Show docker prompt if the user has just run 'python manage.py runserver' on their local machine...
    except FileNotFoundError:
        return HttpResponse('<h1> Page not found! </h1> <p> Unable to open documentation (README.md)! Please use the official `vending_machine` docker image to view the documentation using this page. </p>', 
        content_type='text/html', status=status.HTTP_404_NOT_FOUND)

@method_decorator(csrf_exempt, name="dispatch")
class RegisterStatusView(View):

    """
    
    This class will handle the initialization of the vending machine's cash register.

    """

    def post(self, request):

        ''' Initialize the vending machine.  

            A POST request should contain a collection of coin types & counts to be initialized.  Every coin 
            in the collection MUST correspond to a member of CoinEnum.  If a coin type is not provided as 
            part of the request, its count will be initialized to 0.

            This function will return:
            - HTTP 200: OK (if all coin types are valid and have successfully been initialized).
            - HTTP 400: BAD REQUEST (if any of the coin types are invalid - no changes to the vending machine will be made).
            - HTTP 500: INTERNAL SERVER ERROR (general error to catch any unexpectected exceptions)
        '''

        try:

            logger.info('Request for initialize machine register received!')
            data = JSONParser().parse(request) 
            logger.debug('Request successfully parsed in JSON format!')
            
            # Let's check to make sure all coin types given are valid...
            logger.debug('Checking for invalid coin types in JSON data...')
            [ CoinEnum[coin['id']] for coin in data ]
            coins_initialized = []
            
            # For each coin type (defined by enum), intiialize a CoinRegister model object.
            # If the enum member coin type exists in POST request, use the given coin count.
            # Else, initialise the coin type to have a count of 0 (a.k.a no coins of this type in the machine.)
            # All count values must be > 0!!
            for coin_value, coin_id in CoinEnum.choices():
                coin_in_register, created = CoinRegister.objects.get_or_create(unit=CoinEnum[coin_id])
                coin_in_register.count = 0
                for initialized_coin in data:
                    if coin_id == initialized_coin['id']:
                        logger.debug(f'Attempting initialization for coin type { initialized_coin["id"] } with a count of { initialized_coin["count"] }')
                        if initialized_coin['count'] > 0:
                            logger.debug(f'Initializing coin type: { initialized_coin["id"] } with a count of: { initialized_coin["count"] }...')
                            coin_in_register.count += initialized_coin['count']
                        else:
                            logger.debug(f'Not enough coins deposited for type: { initialized_coin["id"] }! Aborting initialization...')
                            raise (ValueError)
                    else:
                        logger.debug(f'Coin type { initialized_coin["id"] } not part of the request!  Initializing with a count of 0...')

                coin_in_register.save()
                coins_initialized.append({ "id": coin_in_register.unit, "count": coin_in_register.count})
                logger.info(f'Coin type: { coin_in_register.unit }, count: { coin_in_register.count } initialized!')

            # return collection of coins (& counts) initialized 
            logger.info(f'Initialized coins: { coins_initialized }! Sending response to client...')
            return JsonResponse({
                "Register balance": coins_initialized
            }, status=status.HTTP_200_OK)

        except ValueError:
            return JsonResponse({
                "message": "Unable to initialize machine!  One or more coin count values are less than 0."
            }, status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return JsonResponse({
                "message": "Unable to initialize machine!  One or more coin types are invalid.  Please see valid type in the README file."
            }, status=status.HTTP_400_BAD_REQUEST)

        except:
            return JsonResponse({
                "message": "Unable to initialize machine!  Please check the format of your JSON request."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name="dispatch")
class TransactionView(View):

    """

        This class will handle the exchange of funds between the user and the vending machine.
        Currently the only interactions are: 1. Deposit 2. Withdraw   
    
    """

    def get(self, request):    
       
        """

        This function will handle the withdrawl of funds (amount of change given in pence as a parameter).
        
        This function will return:
        - HTTP 200: OK (if full amount of change can be given).
        - HTTP 206: PARTIAL CONTENT (if the vending machine does not have enough change to complete the request in full)
        - HTTP 503: SERVICE UNAVAILABLE (if the vending machine does not have any change to return to the user)
        - HTTP 400: BAD REQUEST (if the query does not match the README.md format)
        - HTTP 500: INTERNAL SERVER ERROR (general error to catch any unexpectected exceptions)

        """

        try:

            logger.info('Request for withdraw transaction received!')
            requested_change = int(request.GET.get('amount'))
            if requested_change <= 0:
                raise(ValueError)

            change_given = dict()

            # Get coins in wallet in reverse order so we can minimise the number of coins returned...
            coins_in_wallet = CoinRegister.objects.order_by("-unit")

            # For the coins available in the wallet/register, we must check to see if we have a valid number available to give back to the user.
            # This loop will check each coin type (from largest to smallest) - if the coin is small enough to be used as change, the vending machine will give 
            logger.debug('Collecting coins for withraw...')
            for coin_type in coins_in_wallet:
                if (coin_type.unit <= requested_change):
                    logger.debug(f'Coin type { coin_type.unit } can be used for withdraw.  Calculating withdraw count...')
                    coin_given = requested_change // coin_type.unit
                    logger.debug(f'{coin_given}x of coin type { coin_type.unit } can be used for withdraw!')
                    if coin_type.count > 0:
                        if coin_type.count >= coin_given:
                            coin_type.count -= coin_given
                            logger.debug(f'{coin_given} used of coin type: { coin_type.unit }')
                        else:
                            logger.warning(f'Coin type: { coin_type.unit } not enough coins to be used to minimise change given!  Using all coins available...')
                            coin_given = coin_type.count
                            coin_type.count = 0
                        
                        coin_type.save()   
                        change_given[CoinEnum(coin_type.unit).name] = coin_given
                        requested_change -= coin_type.unit * coin_given
                        logger.debug(f'{ requested_change } pence still owed for withdraw...')
                    

            # Check to make sure we have given any change at all
            if not bool(change_given):
                logger.warning('Vending machine has no cash left!  Re-initialization/cash deposits need to be made before any more coins can be withdrawn...')
                raise(ChangeError)
        
            # if the full change request can be fulfilled - return full change.
            if requested_change == 0:
                logger.info(f'{ change_given } pence widthrawm (full amount owed)!')
                return JsonResponse({
                    "Change Given": change_given    
                    }, status=status.HTTP_200_OK)
            
            # Tell the user what happened... (i.e not enough change!)
            else:
                logger.warning(f'{ change_given } pence widthrawm (not the full amount owed)!')
                return JsonResponse({
                    "Coins withdrawn": change_given    
                    }, status=status.HTTP_206_PARTIAL_CONTENT)

        except ChangeError:
            return JsonResponse({
            "message": "The vending machine is out of change!  Please contact an engineer to refill the machine..."
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)  

        except ValueError:
            return JsonResponse({
            "message": "The amount of change requested is not valid!  The amount of change requested should be > 0 (given as an integer)."
                }, status=status.HTTP_400_BAD_REQUEST)  

        except TypeError:
            return JsonResponse({
               "message": "Query not valid!  Please see the README.md file for valid query parameters."
                }, status=status.HTTP_400_BAD_REQUEST) 

        except:
            return JsonResponse({
                "message": "Unable to withdraw coins!  Please check the format of your JSON request."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     

    def post(self, request):

        """

        This function handles the deposit of funds from a user into the vending machine.
        The format of coins sent should be defined as a json structure (guidance provided in the README).

        This function will return:
        - HTTP 200: OK (if all coins have been deposited).
        - HTTP 400: BAD REQUEST (if any of the coins are of an invalid type OR if 0 coins have been requested for deposit)
        - HTTP 500: INTERNAL SERVER ERROR (general error to catch any unexpectected exceptions)

        """

        try:
    
            logger.info('Request for deposit transaction received!')
            data = JSONParser().parse(request)
            logger.debug('Request successfully parsed in JSON format!')
            
            # Let's check to make sure all coin types given are valid...
            logger.debug('Checking for invalid coin types in JSON data...')
            [ CoinEnum[coin["id"]] for coin in data ]

            # Raise error if no coins have been requested for deposit...
            if not bool(data):
                raise(ChangeError)

            deposited_coins_dict = []
            # Deposit all coins from data into a CoinRegister model object...
            for coin_value, coin_id in CoinEnum.choices():
                for deposited_coin in data:
                    logger.debug(f'Attempting to deposit coin type: { deposited_coin["id"] }')
                    if deposited_coin["count"] > 0:
                        if isinstance(deposited_coin["count"], int):
                            if (coin_id == deposited_coin["id"]):
                                coin_in_register, created = CoinRegister.objects.get_or_create(unit=CoinEnum[coin_id])
                                if not created:
                                    coin_in_register.count += deposited_coin["count"]
                                    coin_in_register.save()
                                else:
                                    coin_in_register = deposited_coin["count"]
                                    coin_in_register.save()
                                    break
                        else:
                            logger.info(f'Cannot deposit coin type: { deposited_coin["id"] } - count not expressed as integer type!')
                            raise (ChangeError)
                    else:
                        logger.info(f'Cannot deposit coin type: { deposited_coin["id"] } - deposit count less than 1!')
                        raise (ValueError)
            
            return JsonResponse({
                "Coins deposited":  deposited_coins_dict
            }, status=status.HTTP_200_OK)

        except ChangeError:
            return JsonResponse({
                "message": "You did not request for any coins to be deposited!  Please provide a list of coins to be deposited into the vending machine."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except KeyError:
            return JsonResponse({
                "message": "`One or more of the coins specificed are of the wrong type!  None of the deposited coins have been accepted.  Please read the README.md for a list of acceptable coins"
            }, status=status.HTTP_400_BAD_REQUEST)

        except ValueError:
            return JsonResponse({
                "message": "`One or more of the coins requested for deposit has a count value of <= 0.  All coins being deposited must have a count value > 0."
            }, status=status.HTTP_400_BAD_REQUEST)

        except TypeError:
            return JsonResponse({
                "message": "`One or more of the coins requested for deposit has a (count) type that is not an integer."
            }, status=status.HTTP_400_BAD_REQUEST)

        except:
            return JsonResponse({
                "message": "Unable to deposit coins!  Please check the format of your JSON request."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  



    

