# NCSU-Updates

Food-related updates sent via email.

## Deployment with Docker:

First, set required environment variables:
 - MYSQL_DATABASE
 - MYSQL_ROOT_PASSWORD
 - GMAIL_USERNAME
 - GMAIL_APP_PASSWORD

Start database in background: `docker compose up db -d`
Run updater: `docker compose run updater`

Start database, run updater, then end database: `docker compose up --abort-on-container-exit`