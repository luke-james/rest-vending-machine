# rest-vending-machine
A REST API for a vending machine written in Python, deployed using Docker.

# Usage

```json
{
    "data": "Mixed tpe holding the content of the response",
    "message": "Description of what happened"
}
```

Subsequent response definitions will only detail the expected value of the 'data field'.

## Initialize machine

**Definition**
`POST /init/<amount>`

**Arguments**
- `[ { "coin": float, count: int } ]` an array of coins (& number of them) that have been deposited to set the initial float.  The vending machine will override all change available in the machine with the payload of this request, when this request has been made.

**Response**
- `404 Not Found` invalid coin requested.
- `200 OK` on success

```json
[
    {
        "coin": 0.5,
        "count": 2,
    },
    {
        "coin": 0.10,
        "count": 1,
    }
]
```

## Get change (float amount)

**Definition**
`GET /change/<amount>`

**Arguments**
- `"amount": float` the amount of change that has been requested.

**Response**
- `404 Not Found` if there are no coins left in the machine.
- `204 No Content` if the sum of coins in the machine is not 0 < amount < sum_of_coins.
- `200 OK` on success

```json
[
    {
        "coin": 0.5,
        "count": 2,
    },
    {
        "coin": 0.10,
        "count": 1,
    }
]
```

## Deposit coins

**Definition**

`POST /change/<coin>` 

**Arguments**
- `"coin": float` the type of coin being deposited.

**Response**
- `404 Not Found` invalid coin deposited
- `201 Created` on success

```json
    {
        "coin": 0.5,
    },
```


## Assumptions

1. The machine can initialize using multiple coins at once (as if the engineer as opened the side and 'popped a few coins in for change').
2. The user can only deposit one coin at a time (similar to a user paying for a 'coca-cola' - a traditional vending machine will only accept one coin at a time until the balance has been reached).