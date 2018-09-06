
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

WORKDIR /app
ADD . /app

# Using pip:
#RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev
RUN python3 -m pip install -r requirements.txt
#RUN apk del gcc musl-dev python3-dev libffi-dev openssl-dev
RUN python3 manage.py migrate
#python manage.py createsuperuser??
#cmd: 容器启动且 docker run 没有指定其他命令时运行
CMD ["python3","manage.py","runserver","0.0.0.0:8080"]

# Using pipenv:
#RUN python3 -m pip install pipenv
#RUN pipenv install --ignore-pipfile
#CMD ["pipenv", "run", "python3", "-m", "pystuff"]

# Using miniconda (make sure to replace 'myenv' w/ your environment name):
#RUN conda env create -f environment.yml
#CMD /bin/bash -c "source activate myenv && python3 -m pystuff"
