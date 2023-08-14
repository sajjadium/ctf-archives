TASK_FOLDER="source"
DB_PASS="$(pwgen -s 20 1)"
FLAG="CTFZone{...}"

cd $TASK_FOLDER
echo "DB_USER=postgres\nDB_PASS=$DB_PASS\nDB_HOST=postgres_db\nDB_PORT=5432\nDB_NAME=bb_ctf\nIS_PROD=TRUE\nJWT_SECRET=$(pwgen -s 30 1)\nFLAG=$FLAG" > golang.env
echo "POSTGRES_USER=postgres\nPOSTGRES_PASSWORD=$DB_PASS\nPOSTGRES_DB=bb_ctf" > postgres.env
