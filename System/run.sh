conda activate django
python manage.py collectstatic
sudo ln -s nginx.conf /etc/nginx/conf.d/django-backend.conf
sudo nginx -s reload
gunicorn ManageSys.wsgi -c gunicorn.py
echo 'run done'