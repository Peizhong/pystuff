# py

# hello
python manage.py makemigrations podcasts
python manage.py migrate
python manage.py createsuperuser

celery -A pystuff worker --pool=solo --purge -l info --detach
celery -A pystuff beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach

# docker
docker build -t pystuff:v1 .
docker run --name pystuff -d --link rabbitmq:rabbit -p 8085:80 -v /home/peizhong/downloads:/app/downloads pystuff:v1

# nginx 
nginx -t
server {
    listen       80;
    server_name  localhost;
    
    location / {
        uwsgi_pass 172.17.0.4:8080;
        include uwsgi_params;
    }
    location /static/ {
        alias /app/pystuff/static/;
    }
    location /downloads/ {
        alias /app/downloads/;
    }
}