# Rate task API Backend

## Project setup

add a .env file at the root of the directory
containing the following values

```SECRET_KEY=django-insecure-*%)osy81o%^y15!61)q-t$6_coicx0w42u4z60m3amx+l8^xcv
DEBUG=True
ALLOWED_HOSTS=*

SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=<database_name>
SQL_USER=<database_username>
SQL_PASSWORD=<user_password>

# AS the project will be run by docker,
# make sure to allow remote_connection in postgres
# then add your hostname IP in the datbase host

SQL_HOST=<database_host>
SQL_PORT=<database_port>
```

## Build project
run the following command from project root using terminal
```shell
docker build -t rate_backend .
```

## Run the project
run the following command from project root using terminal
```shell
docker run --env-file ./.env -p 8000:8000 --name rate_backend rate_backend
```

## Run unittest
run the following command from project root using terminal
```shell
docker exec -it rate_backend ./run_unit_test.sh
```