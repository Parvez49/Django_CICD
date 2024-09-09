cd api/
gunicorn api.wsgi:application --bind 0.0.0.0:9020 --workers 3
poetry run nohup bash api/gunicorn_run.sh > gunicorn.log 2>&1 &
