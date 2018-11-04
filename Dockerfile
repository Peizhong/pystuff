
# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM python:3.6-alpine

# If you prefer miniconda:
#FROM continuumio/miniconda3

LABEL Name=pystuff Version=0.0.1
EXPOSE 8080

ENV ENV="production"

WORKDIR /app
ADD . /app

# Using pip:
#RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev
#RUN python3 -m pip install -r requirements.txt

# Using pipenv:
RUN python3 -m pip install pipenv
RUN pipenv install
# pipenv install –dev

RUN python3 manage.py migrate
#python manage.py createsuperuser
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

#cmd: 如果 docker run 指定了其他命令，CMD 指定的默认命令将被忽略，只有最后一个 CMD 有效
ENTRYPOINT ["pipenv", "run", "python3","manage.py","runserver","0.0.0.0:8080"]

# Using miniconda (make sure to replace 'myenv' w/ your environment name):
#RUN conda env create -f environment.yml
#CMD /bin/bash -c "source activate myenv && python3 -m pystuff"
