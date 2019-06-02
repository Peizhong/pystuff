# py

# hello
pip list --outdated
pip install --upgrade Django
pipenv check

python manage.py makemigrations podcasts
python manage.py migrate
python manage.py createsuperuser

celery -A pystuff worker --pool=solo --purge -l info --detach
celery -A pystuff beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach

# docker
sudo docker build -t pystuff:v3 .
sudo docker run --name pystuff -d --link rabbitmq:rabbitmq -p 8085:80 -v /home/peizhong/downloads:/app/downloads pystuff:v3

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

# log
{
    "app":"",
    "type":"",
    "module:"",
    "level":"",
    "message":"",
    "error":"",
    "host":""
}

# logstash
# config/pipelines.yml -> /usr/share/logstash/pipeline/logstash.conf
input {
    beats {
        port => "5044"
    }    
    tcp {
        port => "5959"
        codec => json
    }
}
# The filter part of this file is commented out to indicate that it is
# optional.
filter {
    grok {
        match => { "message" =>"\[%{TIMESTAMP_ISO8601:logdate}: %{LOGLEVEL:level}\/%{DATA:process}\](?<host>) (?<data>(.|\r|\n)*)"}
    }
    date {
        match => ["logdate", "yyyy-MM-dd HH:mm:ss,SSS"]
        target => "@timestamp"  ## 默认target就是"@timestamp
    }
    mutate {
        rename => { "[host][name]" => "host" }
        remove_field => ["logdate"]
    }
}
output {
#    stdout { codec => rubydebug }
    elasticsearch {
        hosts => [ "193.112.41.28:9200" ]
    }
}