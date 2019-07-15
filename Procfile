web: gunicorn run:app

release: python manage.py db merge 53301fb65ee1 42717361e091 af019111fe6c fc58019bd853
release: python manage.py db migrate
release: python manage.py db upgrade