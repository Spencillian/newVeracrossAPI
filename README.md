# API to get grades from Veracross

## USAGE

```json
{
    "message": "Extra description of what is going on",
    "data": "Mixed typed content of the response"
}
```

Below are the definitions for the `"data"` field

### List all users

`Get /users`

**Response**

- `200 OK`

```json
[
    {
        "username": "some username"
    },
    {
        "username": "lis73243"
    }
]
```
The response here is not supposed to include much information
and may be deleted in the near future as it poses a security risk.

###Registering New Users

**Definitions**

`POST /users`

**Arguments**

- `"username":string` : `USERNAME` : a globally unique id for each user
- `"password":string` : `PASSWORD` : password associated with user

If a user already has the username, then the existing user will be over written.

**Response**

- `201 Created` on success

```json
{
    "username": "lis73243"
}
```

## Get grades from users

`GET /users/<id>`

**Response**

- `404 Not Found` if the device is not found
- `200 OK` on success

```json
{
    "username": "lis73243",

    "num_grade_0": "num_grade_0",
    "num_grade_1": "num_grade_1",
    "num_grade_#": "num_grade_#",

    "let_grade_0": "let_grade_0",
    "let_grade_1": "let_grade_1",
    "let_grade_#": "let_grade_#"
}
```

## Delete a user

**Definitions**

`DELETE /devices/<id>`

**Response**

- `404 Not Found` if user doesn't exist
- `204 No Content` on success