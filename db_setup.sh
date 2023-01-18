#PGPASSWORD=es_password
export PGPASSWORD=es_password

if [[ -d migrations ]]; then
    echo "migrations folder exists; will remove..."
    rm -rf migrations
else
    echo "migrations folder does not exist..."
fi

#λ
DB_SUFFIXES=("" "_test" "_prod")
export ALEMBIC_EXCLUDE="\n[alembic:exclude]
tables = spatial_ref_sys,topology,layer,alembic_version\n"

for DB_SUFFIX in "${DB_SUFFIXES[@]}"; do
  DB_NAME="flask_jwt_auth${DB_SUFFIX}"

  echo "Drop DB:: ${DB_NAME}"
  psql -h ${HOST_IP} -p 54320 -U es_user -w eventstore -c "drop database ${DB_NAME};"

  echo "Create DB:: ${DB_NAME}"
  psql -h ${HOST_IP} -p 54320 -U es_user -w eventstore -c "create database ${DB_NAME};"

#  echo "Grant CONNECT permissions on DB:: ${DB_NAME}"
#  psql -h ${HOST_IP} -p 54320 -U es_user -w eventstore -c "GRANT CONNECT ON DATABASE ${DB_NAME} TO es_user;"
#
#  echo "Grant USAGE permissions on public schema:: ${DB_NAME}"
#  psql -h ${HOST_IP} -p 54320 -U es_user -w eventstore -c "GRANT USAGE ON SCHEMA public TO es_user;"
  echo "Grant ALL privileges to DB:: ${DB_NAME}"
  psql -h ${HOST_IP} -p 54320 -U es_user -w eventstore -c "grant all privileges on DATABASE ${DB_NAME} TO es_user;"
done

#psql -h ${HOST_IP} -p 54320 -U es_user -w eventstore -c "drop database flask_jwt_auth_test;"
#psql -h ${HOST_IP} -p 54320 -U es_user -w eventstore -c "create database flask_jwt_auth_test;"
#
#psql -h ${HOST_IP} -p 54320 -U es_user -w flask_jwt_auth_test -c "delete from alembic_version;"
#psql -h ${HOST_IP} -p 54320 -U es_user -w flask_jwt_auth_test -c "\c flask_jwt_auth"

# old_migrate via manage.py
# python3 manage.py create_db
# python3 manage.py db init
# python3 manage.py db migrate
# python3 manage.py db upgrade

echo -e "\n\n==================== Flask DB init ===================="

flask db init
#cp configs/script.py.mako migrations/script.py.mako
awk '/import sqlalchemy/ { print; print "import flask_jwt_auth"; next }1' configs/script.py.mako |tee migrations/script.py.mako

echo -e "\n\n==================== Flask DB migrate ===================="

echo -e "${ALEMBIC_EXCLUDE}" >> ./migrations/alembic.ini
flask db migrate -m "Create Initial DB:: migration."

echo -e "\n\n==================== Flask DB upgrade ===================="

flask db upgrade --tag "Create Initial DB:: tables."
