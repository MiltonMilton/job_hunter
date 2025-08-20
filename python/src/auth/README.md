# Auth Service

This service manages authentication using a MySQL database.

## Start MySQL with Docker

Run a local MySQL instance and create the initial database:

```bash
docker run --name local-mysql \
  -e MYSQL_ROOT_PASSWORD=tu_password \
  -e MYSQL_DATABASE=auth \
  -p 3306:3306 \
  -d mysql:8
```

Create an application user and grant access:

```bash
docker exec -it local-mysql mysql -uroot -ptu_password -e "\
  CREATE USER 'auth_user'@'%' IDENTIFIED BY 'otra_password';\
  GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'%';\
  FLUSH PRIVILEGES;\
"
```

## Configure the database URL

The service reads `AUTH_DATABASE_URL` for the SQLAlchemy engine.

Set it in your shell:

```bash
export AUTH_DATABASE_URL="mysql+pymysql://auth_user:otra_password@localhost:3306/auth"
```

Or create a `.env` file (listed in `.gitignore`):

```
AUTH_DATABASE_URL=mysql+pymysql://auth_user:otra_password@localhost:3306/auth
```

## Build and run the service

From this directory:

```bash
docker build -t auth-service .
```

Run the container and provide the database URL:

```bash
docker run --rm \
  -e AUTH_DATABASE_URL="$AUTH_DATABASE_URL" \
  auth-service
```

The service will apply database migrations on startup using Alembic.

## Create a new migration (developers)

After modifying models, generate a migration:

```bash
alembic revision --autogenerate -m "your message"
```

Then apply it:

```bash
alembic upgrade head
```

