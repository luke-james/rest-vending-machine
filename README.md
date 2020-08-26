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

## Local Setup - PRE-REQUISITE TO DEPLOYING LOCALLY/WITH DOCKER
**Requires Python >= 3.4x & Virtual Environments**<br>
`git clone https://github.com/luke-james/rest-vending-machine.git`<br>
`python3 -m venv [git repository path]/env` <br>
`source /path/to/env/bin/activate` <br>
`pip install -r requirements.txt` <br>

**Create tables for app without migrations...** <br>
`cd [git_repository_path]/vending_machine/ && python manage.py migrate --run-syncdb` <br>

**Compile Sphinx Documentation...** <br>
`cd [git_repository_path]/vending_machine/docs && sphinx-apidoc -o . .. && make html`

**To run the API (locally):**<br>
`python vending_machine/manage.py runserver`

**To run the tests (locally):**<br>
`python vending_machine_manage.py test`

## Deployment with Docker (CE/Compose - all services)
**Requires DockerCE & Compose**<br>
`docker-compose build`<br>

**To run the API (docker):**<br>
`docker-compose up`<br>

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
[
    {
        "id": "PENCE_1",
        "count": 2
    },
    {
        "id": "PENCE_2",
        "count": 10
    }
]
```

## Get change (float amount)

**Definition**<br>
`GET /change/<amount>`

**Arguments**<br>
- `"amount": integer` the amount of change (in pence) that has been requested - this must be a positive integer value.

**Response**<br>
- `200 OK` on success <br>
- `206 PARTIAL CONTENT` if the sum of coins in the machine is not 0 < amount < sum_of_coins. <br>
- `400 BAD REQUEST` if the JSON format is invalid. <br>
- `500 INTERNAL SERVER ERROR ` general server error. <br>
- `503 SERVICE UNAVAILABLE` if there are no coins left in the machine.` <br>

```json
{
    "amount": 100
}
```

## Deposit coins

**Definition**<br>
`POST /change/<coins>` 

**Arguments**<br>
- `{ "coin_type": { "count": integer }}` collection of coins being deposited.

**Response**<br>
- `200 OK` on success
- `400 BAD REQUEST` invalid coin deposited/0 coins have been deposited

```json
[
    {
        "id": "PENCE_1",
        "count": 2
    },
    {
        "id": "PENCE_2",
        "count": 10
    }
]
```

## Assumptions/Limitation
1. The machine can initialize, deposit & withdraw using multiple coins per transaction.
2. The initial 'float' is set by the number of coins deposited at initialization - this is not set using a float data type.
3. For simplicity this machine stores each coin type as an Enumeration.  This approach has allowed me to easily control & validate coin types initialized & submitted (on this small scale) - if you were to introduce notes/other currencies - this may not be an appropriate data type.
3. The vending machine does not check for duplicate entries.  The following is acceptable to initialize/deposit (this will give you a total of 12x 1p coins):

```json
[
    {
        "id": "PENCE_1",
        "count": 2
    },
    {
        "id": "PENCE_1",
        "count": 10
    }
]
```
4. Sphinx documentation does not use any custom modules due to time constraints.
5. Dev/Staging/Prod configuration (settings, logging, secrets/keys etc.) has not been implemented for the Django project/app due to time limitations.

## Other Notes
I have provided a suite of test cases that can be run with the instructions above.  If you wish to have more flexibility with interacting with the API, any freely available API client will work nicely.  

e.g. 
https://insomnia.rest/
