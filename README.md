# test task Python Backend Developer 

## Description

**REST API to create sales receipts with user registration**

**API register user**

```
POST: http://0.0.0.0:8000/register
{
    "name": "admin",
    "username": "admin",
    "password": "11111111"
}
```
**API login user**

```
POST: http://0.0.0.0:8000/login
{
    "username": "admin",
    "password": "11111111"
}
response(access_token, refresh_token)
```
**API change oassword**

```
POST: http://0.0.0.0:8000/change-password
{
    "username": "admin",
    "old_password": "11111111",
    "new_password": "1111111111"
}
key: Authorization
value: Bearer value(access_token) (get after login)
```
**API logout user**

```
POST: http://0.0.0.0:8000/logout
key: Authorization
value: Bearer value(access_token) (get after login)
```
**API get users**

```
GET: http://0.0.0.0:8000/getusers
key: Authorization
value: Bearer value(access_token) (get after login)
```
**API sale receipt(create new sale receipt)**

```
POST: http://0.0.0.0:8000/sale_receipts
{
    "products": [
        {
            "name": "Ford",
            "price": 111.5,
            "quantity": 1
        },
        {
            "name": "Mazda",
            "price": 2.25,
            "quantity": 2
        }
    ],
    "payment": {
        "type": "Cash",
        "amount": 213
    }
}
key: Authorization
value: Bearer value(access_token) (get after login)
```
**API get receipt by id**

```
GET: http://0.0.0.0:8000/sale_receipts/1
key: Authorization
value: Bearer value(access_token) (get after login)
```
**API get receipts(filtrations)**

```
GET: http://0.0.0.0:8000/sale_receipts/1
key: Authorization
value: Bearer value(access_token) (get after login)
key: total_amount   value: 20(int)
key: payment_type   value: Cash(str)
key: start_date   value: 2024-05-01
key: end_date   value: 2024-05-06
```



## Technologies used in the project
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- Docker-compose
- Git
- alembic
- pydantic


## Local setup

**Create python environment**

```
$ python3 -m venv venv
```

**Activate python environment**

```
$ source venv/bin/activate
```

**Install dependencies**

```
$ pip install -r requirements.txt
```

**Create .env file and insert there all code from .envexample file**

```
$ touch .env
```

**Build web and database containers**

```
$ sudo docker-compose build
```

**Run web and database containers**

```
$ sudo docker-compose up
```

**Go to the middle of the running container in a new terminal window**

```
$ sudo docker-compose exec web bash
```

**Perform database migrations**

```
$ python manage.py migrate
```

**Create superuser**

```
$ python manage.py createsuperuser
```