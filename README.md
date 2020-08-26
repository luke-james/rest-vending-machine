# rest-vending-machine
A REST API for a vending machine written in Python, deployed using Docker.

**Services:**<br>
REST API : PORT 8000<br>
DOCS : PORT 1000 (Docker-ONLY)<br>

Note: Documentation is generated using Sphinx default settings - no custom modules used due to time constraints.<br>

**Valid Currency**<br>
<ul>
<li>1p      = "PENCE_1"</li>
<li>2p      = "PENCE_2"</li>
<li>5p      = "PENCE_5"</li>
<li>10p     = "PENCE_10"</li>
<li>20p     = "PENCE_20"</li>
<li>50p     = "PENCE_50"</li>
<li>£1      = "PENCE_100"</li>
<li>£2      = "PENCE_200"</li>
</ul>

## Deployment Option 1: Local (no html-based REAME.md or Sphinx docs)
**Requires Python >= 3.4x & Virtual Environments**<br>
`git clone https://github.com/luke-james/rest-vending-machine.git`<br>
`python3 -m venv [git repository path]/env` <br>
`source /path/to/env/bin/activate` <br>
`pip install -r requirements.txt` <br>

**To run the API:**<br>
`python vending_machine/manage.py runserver`

**To run the tests:**<br>
`python vending_machine_manage.py test`

## Deployment Option 2: Docker (CE/Compose - all services)
**Requires DockerCE & Compose**<br>
`git clone https://github.com/luke-james/rest-vending-machine.git`<br>
`docker-compose build`<br>

**To run the API:**<br>
`docker-compose up`<br>

**To run the tests:**<br>
`docker-compose up` <br>
`docker exec -it <container name> bash` <br>
`python /code/vending_machine/manage.py test` <br>

# Usage

```json
{
    "data": "Mixed tpe holding the content of the response",
    "message": "Description of what happened"
}
```

Subsequent response definitions will only detail the expected value of the 'data field'.

## Initialize machine

**Definition**<br>
`POST /init/<coins>`

**Arguments**<br>
- ` { "coin_type": { "count": integer }} ` <br>

A collection of coins to be initialized into the vending machine.  The key will correspond to the valid list of coin types available in the machine, and the value will correspond to the number of coins being initialized for this type.  The vending machine will override all change available in the machine with the payload of this request, when this request has been made.

**Response**<br>
- `200 OK` on success<br>
- `400 BAD REQUEST` invalid coin requested.<br>
- `500 INTERNAL SERVER ERROR` general error <br>

```json
{
    "PENCE_1": {
        "count": 2
    },      
     
    "PENCE_2": {
        "count": 10
    }
}
```

## Get change (float amount)

**Definition**<br>
`GET /change/<amount>`

**Arguments**<br>
- `"amount": integer` the amount of change (in pence) that has been requested - this must be a positive value.

**Response**<br>
- `200 OK` on success <br>
- `206 PARTIAL CONTENT` if the sum of coins in the machine is not 0 < amount < sum_of_coins. <br>
- `400 BAD REQUEST` if the JSON format is invalid. <br>
- `500 INTERNAL SERVER ERROR ` general server error. <br>
- `503 SERVICE UNAVAILABLE` if there are no coins left in the machine.` <br>

```json
{
    "PENCE_1": {
        "count": 20
    },

    "PENCE_200": {
        "count": 1
    }
}
```

## Deposit coins

**Definition**<br>
`POST /change/<coins>` 

**Arguments**<br>
- `{ "coin_type": { "count": integer }}` collection of coin being deposited.

**Response**<br>
- `200 OK` on success
- `400 BAD REQUEST` invalid coin deposited/0 coins have been deposited

```json
{
    "PENCE_1": {
        "count": 5
    },

    "PENCE_2": {
        "count": 10
        
}
```


## Assumptions<br>
1. The machine can initialize using multiple coins at once (as if the engineer as opened the side and 'popped a few coins in for change').
2. The 'float' has been treated as the machine balance as opposed to a data type.  For simplicity this machine has been designed to work in units of 'pence' using UK currency.