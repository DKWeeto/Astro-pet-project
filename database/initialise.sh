echo "Connecting to DB"
export $(cat .env | xargs)
export PGPASSWORD=$DB_PASSWORD
echo "Setting up schema"
psql --host=$DB_HOST --port=$DB_PORT --username=$DB_USER --dbname=$DB_NAME -f schema.sql
echo "Inserting metadata"
psql --host=$DB_HOST --port=$DB_PORT --username=$DB_USER --dbname=$DB_NAME -f metadata.sql