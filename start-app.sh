#
# to be executed correctly in the environments (envconsul)
# startup commands are placed in shell script,
# so that application can have correctly access to environment variables
#
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn -b :8000 tododemo.wsgi
