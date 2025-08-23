# Auth Service

This service manages authentication using a Flask application backed by a MySQL database.

## Start MySQL with Docker

Run a local MySQL instance and create the initial database:

```bash
docker run --name auth-mysql \
  -e MYSQL_ROOT_PASSWORD=auth_root_password \
  -e MYSQL_DATABASE=auth \
  -p 3306:3306 \
  -d mysql:8
```

Create an application user and grant access:

```bash
docker exec -it auth-mysql mysql -uroot -pauth_root_password -e "\
  CREATE USER 'auth_user'@'%' IDENTIFIED BY 'auth_user_password';\
  GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'%';\
  FLUSH PRIVILEGES;\
"
```

## Configure the database URL

The service reads `AUTH_DATABASE_URL` for the Flask SQLAlchemy engine.

Set it in your shell:

```bash
export AUTH_DATABASE_URL="mysql+pymysql://auth_user:auth_user_password@host.docker.internal:3306/auth"
```

Or create a `.env` file (listed in `.gitignore`):

```
AUTH_DATABASE_URL=mysql+pymysql://auth_user:auth_user_password@host.docker.internal:3306/auth
```

## Build and run the service

From this directory:

```bash
docker build -t auth-service .
```

Run the container, expose the port and provide the database URL:

```bash
docker run --rm \
  -p 8000:8000 \
  -e AUTH_DATABASE_URL="$AUTH_DATABASE_URL" \
  auth-service
```

The service will apply database migrations on startup using Flask-Migrate and start a Flask server on port `8000`.

## Create a new migration (developers)

Set the Flask application for CLI commands:

```bash
export FLASK_APP=server.py
```

After modifying models, generate a migration:

```bash
flask db migrate -m "your message"
```

Then apply it:

```bash
flask db upgrade
```

