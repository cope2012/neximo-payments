
# Payments Service

### Requirements
- Poetry: This project uses [poetry](https://python-poetry.org/) as dependency manager, in order to properly run the project this tool has to be
  installed on your development machine.
- For dev environment create a .env file in the root of the project, copy lines below and paste it in the just created .env file:
  ```
    # App
    DEBUG=True
    
    # Django
    SECRET_KEY='django-insecure-x*8m0a23cp9h@lxj^-+b*#cg+@f!_cw93@s%sp-9b&x_!msu_y'
    
    # DB
    DB_NAME=payments
    DB_PASSWORD=root
    DB_USER=postgres
    DB_HOST=payments-db
    DB_PORT=5432
    
    # JWT
    ACCESS_TOKEN_LIFETIME=40
  ```

### Building and running the service
- To build the project for the first time:
    ```
    docker-compose build
    ```
- To run the service:
    ```
    docker-compose up
    ```
- Apply migrations:
    ```
    docker compose run --rm payments python manage.py migrate
    ```
