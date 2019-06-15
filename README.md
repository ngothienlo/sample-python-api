# Falcon DEMO CRUD API with PostgreSQL

Before install
==============

Cd into source code folder and run command

```
chmod +x install.sh
```


Installation
============

Setup env for app

```
./install.sh
```

Demodata <optional> - Run after create db from git-repo folder
```
python3 testing_script.py
```

Start server - From git-repo folder

```
chmod +x ./app/run.sh
./app/run.sh start
```

Stop server

```
Ctrl + C
```

Usage
=====

CREATE
```shell
echo '{"name": "create_demo_01", "dob": "2019-06-10"}' | http POST http://localhost:5000/customers
```

- Reponse
```json
HTTP/1.1 201 Created
Connection: close
Date: Wed, 12 Jun 2019 21:31:03 GMT
Server: gunicorn/19.9.0
content-length: 106
content-type: application/json

{
    "data": {
        "dob": "2019-06-10",
        "id": 103,
        "name": "create_demo_01",
        "updated_at": "2019-06-13T04:31:03Z"
    }
}
```

READ
http://localhost:5000/customers/1

- get
```shell
http GET http://localhost:5000/customers/1
```

- search
```shell
http GET http://localhost:5000/customers\?name\='Eric Dominguez'
```

- Reponse
```json
HTTP/1.1 200 OK
Connection: close
Date: Wed, 12 Jun 2019 21:20:11 GMT
Server: gunicorn/19.9.0
content-length: 86
content-type: application/json

{
    "data": {
        "dob": "1997-08-05",
        "id": 1,
        "name": "Eric Dominguez",
        "updated_at": null
    }
}

```

UPDATE
```shell
echo '{"name": "Cus_name_update_01"}' | http PUT http://localhost:5000/customers/12
echo '{"name": "Cus_name_update_01"}' | http PATCH http://localhost:5000/customers/12
```

- Reponse
```json
HTTP/1.1 200 OK
Connection: close
Date: Wed, 12 Jun 2019 21:32:51 GMT
Server: gunicorn/19.9.0
content-length: 109
content-type: application/json

{
    "data": {
        "dob": "1970-01-07",
        "id": 12,
        "name": "Cus_name_update_01",
        "updated_at": "2019-06-13T04:32:51Z"
    }
}
```

DELETE
```shell
http DELETE  http://localhost:5000/customers/13
```

- Reponse
```json
HTTP/1.1 200 OK
Connection: close
Date: Wed, 12 Jun 2019 21:33:42 GMT
Server: gunicorn/19.9.0
content-length: 2
content-type: application/json

{}
```