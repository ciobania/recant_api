if [[ -d migrations ]]; then
    echo "migrations folder exists; will remove..."
    rm -rf migrations
else
    echo "migrations folder does not exist..."
fi


#psql -h 192.168.1.137 -p 54320 -U es_user -W eventstore -c "create database flask_jwt_auth;"
#psql -h 192.168.1.137 -p 54320 -U es_user -W eventstore -c "create database flask_jwt_auth_test;"
python3 manage.py create_db
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade

