# Django Bonds API

This is a Django implementation of a bonds API which allows ingesting data representing bonds, querying an external api for additional data about the specific bond and make the resulting data queryable via the API. The API leverages Django & Django Rest Framework & Django-Rest-Knox.

- Authentication allows each user to only see their own data.
- Each bond has a `lei` field (Legal Entity Identifier). The [GLEIF API](https://www.gleif.org/en/lei-data/gleif-lei-look-up-api/access-the-api) is used to find the corresponding `Legal Name` of the entity which issued the bond.
- SQLite is used for the database.

#### Project Quickstart

Inside a virtual environment running Python 3:

- `pip install -r requirement.txt`
- `./manage.py runserver` to run server.
- `./manage.py test` to run tests.

### APIs

Manual testing of the API was performed using [Postman](https://www.postman.com/) API Development Platform. Brief description of core functionality of the API is given below, but please refer to the [documentation](https://documenter.getpostman.com/view/10868302/TVKHUFWw) for more details.

#### AUTHENTICATION API

`POST /login/`,
`POST /register/` to login and register respectively,
with the following data being passed in:

```
{
    "username": "john",
    "email": "john@gmail.com",
    "password": "123456"
}
```

`POST /logout/` - makes the token generated at login no longer valid.

#### BONDS API

Using the token that is generated when a user is registered or logged in (by adding the token in the header), the user can send a request to:

`POST /bonds/`
to create a "bond" with data that looks like:

```
{
    "isin": "FR0000131104",
    "size": 100000000,
    "currency": "EUR",
    "maturity": "2025-02-28",
    "lei": "R0MUWSFPU8MPRO8K5P83"
}
```

---

The user can send a request to:

`GET /bonds/`

to see all of the bonds that are currently in their account:

```
[
    {
        "isin": "FR0000131104",
        "size": 100000000,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "lei": "R0MUWSFPU8MPRO8K5P83",
        "legal_name": "BNPPARIBAS"
    },
    ...
]
```

By sending a filter query by legal_name:

`GET /bonds/?legal_name=BNPPARIBAS`

the user is able to retrieve the bonds which fall under that legal_name query only, therefore narrowing down the number of results returned.
