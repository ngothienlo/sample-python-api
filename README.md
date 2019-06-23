# Falcon DEMO CRUD API with PostgreSQL

Before install
==============

Cd into source code folder and run command

```
chmod +x install.sh
```

Setup env for app

```
./install.sh
```

If you don't want run script. You need:

- config db info for connection in:
    ```shell
    \app\config\config.py
    ```

- run this command to create db struct.
    ```shell
    python3 ./app/youngest_customers.py
    ```

Installation
============

Demodata <optional> - Run after create db from git-repo folder
```
python3 create_demo_data.py
```

Start server - From git-repo folder

```
chmod +x ./app/run.sh
./app/run.sh start
```

Stop server

```shell
    Ctrl + C
```

or 

```shell
    ./app/run.sh stop
```

Usage
=====

LOGIN
```shell
http POST http://45.77.250.38:5000/login?email=user_test@sample.test&pwd=user_test_pwd
```

- Response
```json
HTTP/1.1 200 OK
Connection: close
Date: Sun, 23 Jun 2019 13:51:10 GMT
Server: gunicorn/19.9.0
content-length: 0
content-type: application/json
set-cookie: my_auth_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkZW50aWZpZXIiOiJ1c2VyX3Rlc3RAc2FtcGxlLnRlc3QiLCJleHAiOjE1NjEzMDE0NzB9.WAPPGG5OlfhIot_QfeMOKibpFRusWvIEiNM6ZzXuvSw; HttpOnly; Max-Age=86400; Path=/customers; Secure
```




CREATE
```shell
http POST http://localhost:5000/customers?name=<customer_name>&dob=<customer_dob> { HEADER: { HEADER: authorization:<access_token> } }
```

- Example
```shell
http POST http://localhost:5000/customers?name=customer_01&dob=1989-01-01 authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkZW50aWZpZXIiOiJ1c2VyX3Rlc3RAc2FtcGxlLnRlc3QiLCJleHAiOjE1NjEzMDE0NzB9.WAPPGG5OlfhIot_QfeMOKibpFRusWvIEiNM6ZzXuvSw
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
http://localhost:5000/customers/1 { HEADER: authorization:<access_token> }

- get
```shell
http GET http://localhost:5000/customers/1 { HEADER: authorization:<access_token> }
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
http PUT http://localhost:5000/customers/12?<field_update>=<update_value> { HEADER: authorization:<access_token> }
```
- Example
```shell
http PUT http://localhost:5000/customers/12?name=customer_01&dob=1989-01-01  authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkZW50aWZpZXIiOiJ1c2VyX3Rlc3RAc2FtcGxlLnRlc3QiLCJleHAiOjE1NjEzMDE0NzB9.WAPPGG5OlfhIot_QfeMOKibpFRusWvIEiNM6ZzXuvSw
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
http DELETE http://localhost:5000/customers/13 { HEADER: authorization:<access_token> }
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
