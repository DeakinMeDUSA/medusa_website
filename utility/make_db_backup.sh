printf -v date '%(%Y-%m-%d)T' -1
pg_dump --file="db_backup/backup-$date.sqlc" --dbname=medusa_website
echo "Backed up database to db_backup/backup-$date.sqlc successfully!"
