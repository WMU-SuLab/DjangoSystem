#本脚本非用来执行，而是应该复制粘贴到终端使用的
conda activate django
python manage.py collectstatic
sudo ln -s /data/DjagnoSystem/System/nginx.conf /etc/nginx/conf.d/django_system.conf
sudo nginx -s reload
sudo ln -s /data/DjagnoSystem/System/supervisor.ini /etc/supervisord.d/django_system.ini
gunicorn Config.wsgi -c gunicorn.py
echo 'run done'