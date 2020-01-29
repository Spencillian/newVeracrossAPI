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

### Requesting Grades

**Definitions**

`POST /users`

**Post Body** - From client - React NativeA

```
fetch('https://randomString.ngrok.com/users/', {
    method: 'POST',
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: "username",
        password: "password",
    }),
});
```

If a user already has the username, then the existing user will be over written.

**Response**

- `201 Created` on success

```json
{
    "message": "User found", 
    "data": [{
        "id": "INT_id",
        "name": "course_name",
        "number": "INT_number_grade",
        "letter": "letter_grade"
    },
    {
        "id": 0,
        "name": "English 2",
        "number": 98.9,
        "letter": "A+"
    }]
}
```

## Delete a user

**Definitions**

`DELETE /users/<id>`

**Response**

- `404 Not Found` if user doesn't exist
- `204 No Content` on success