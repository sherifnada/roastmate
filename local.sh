
# Setup database
mkdir secrets
echo '{"user": "postgres","password": "password","port": 5432,"host": "localhost","database": "postgres"}' > secrets/db.json
docker run --rm --name roastmate-pg-local -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres

