if [[ -d migrations ]]; then
    echo "migrations folder exists; will remove..."
    rm -rf migrations
else
    echo "migrations folder does not exist..."
fi


python3 manage.py create_db
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade

