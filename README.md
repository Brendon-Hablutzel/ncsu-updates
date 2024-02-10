# NCSU-Updates

Food-related updates sent via email.

## Deployment with Docker

### Service Deployment

First, set required environment variables:
- `MYSQL_PASSWORD` - the password to use when connecting to the db container from the app and the notifier
- `MYSQL_ROOT_PASSWORD` - the password to set for the root user in the db container
- `GMAIL_USERNAME` - the gmail username to use for sending emails
- `GMAIL_APP_PASSWORD` - an app password associated with the given gmail username

Optional environment variables:
- `MYSQL_DATABASE` - the name of the database, defaults to `notifs`
- `MYSQL_USER` - the user to access the database with, defaults to `root`
- `MYSQL_HOST` - the database host, defaults to `db`

Start database in the background: `docker compose up db -d`

Run notifier: `docker compose run --rm notifier`

Run notifier and close DB after: `docker compose run --rm notifier && docker compose down db`

### Scripts

Some scripts are available to edit the notifs database:
- `docker compose run --rm scripts read [recipient]` returns all records in the database, optionally filtering by recipient
- `docker compose run --rm scripts create <dining hall> <meal> <keyword(s)> <recipient>` adds a record to the database, where multiple keywords can be specified if separated with commas
- `docker compose run --rm scripts delete <recipient>` deletes all records with the given recipient
