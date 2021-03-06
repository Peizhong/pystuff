
# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM mydjango:v0

# If you prefer miniconda:
#FROM continuumio/miniconda3

LABEL Name=pystuff Version=0.0.1
EXPOSE 80

ENV ENV="production"

WORKDIR /app
ADD . /app

#RUN apt-get nginx 

# Using pip:
# RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev
#RUN python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple setuptools 
#RUN python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple uwsgi
RUN python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# Using pipenv:
#RUN python3 -m pip install pipenv
#RUN pipenv install

RUN python manage.py migrate
#python manage.py createsuperuser
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

#RUN pipenv run celery -A pystuff worker --pool=solo --purge -l info --detach
#RUN pipenv run celery -A pystuff beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach

#cmd: 如果 docker run 指定了其他命令，CMD 指定的默认命令将被忽略，只有最后一个 CMD 有效
#ENTRYPOINT ["pipenv", "run", "python3","manage.py","runserver","0.0.0.0:8080"]
#CMD pipenv run celery -A pystuff worker --pool=solo --purge -l info --detach & pipenv run celery -A pystuff beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach & pipenv run python3 manage.py runserver 0.0.0.0:8080

#sudo nginx -s reload
COPY nginx-default /etc/nginx/conf.d/default.conf
RUN rm -rf /etc/nginx/sites-enabled/*

#RUN mkdir /var/run/nginx
#RUN touch /var/run/nginx/nginx.pid
#service  nginx status

#CMD celery -A pystuff worker --pool=solo --purge -l info --detach & celery -A pystuff beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach & /usr/sbin/nginx & uwsgi --ini uwsgi.ini
CMD celery -A pystuff worker --pool=solo --purge -l info --detach & celery -A pystuff beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach & /usr/sbin/nginx & uwsgi --ini uwsgi.ini

# Using miniconda (make sure to replace 'myenv' w/ your environment name):
#RUN conda env create -f environment.yml
#CMD /bin/bash -c "source activate myenv && python3 -m pystuff"
