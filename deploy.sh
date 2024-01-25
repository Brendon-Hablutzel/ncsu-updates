# export DB_HOSTNAME="db"
export MYSQL_DATABASE=""
export MYSQL_ROOT_PASSWORD=""
export MYSQL_USER=""
export GMAIL_USERNAME=""
export GMAIL_APP_PASSWORD=""

echo "Building Docker compose services..."
docker compose build

echo "Starting Docker compose services..."
docker compose up --abort-on-container-exit