# test task Python Backend Developer 

## Description

**REST API to create sales receipts with user registration**

**All API doc(after start server)**

```
http://0.0.0.0:8000/docs#/
```

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

**Build web and database containers**

```
$ sudo docker-compose build
```

**Run web and database containers**

```
$ sudo docker-compose up
```

**Create alembic(open terminal when server start)**

```
$ alembic init alembic
```

**Replace file**

```
Replace env.py from main directory to directory alembic
```

**Initial migrations(open terminal when server start)**

```
$ alembic revision --autogenerate -m "initial"
```
**Add function for migration tables to DB**

```
$ Open file alembic/versions/.........._initial.py and replace function upgrade from file test.py
```
**Delete all tables from DB without alembic_version(open terminal when server start)**

```
$ docker-compose exec db bash
$ psql -U postgres
$ psql \dt
$ DROP TABLE name_table;
...
exit
exit
```
**Add migrations to DB tables**

```
$ alembic upgrade head
```
**Use all API**

```
Postman or http://0.0.0.0:8000/docs#/ or ...
```