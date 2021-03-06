# Django Celery Flower test project

This project has the only purpose of being used as a minimal working example to test the interaction between Django, Celery and Flower.

## Start playing

Just run
```bash
docker-compose up -d
```
After the initialization, populate the backend with 
```
./populate_backend.sh
```
Now, the backend has 10 instances of the ```HeavyComputation``` model. 
We can submit each instance for a computation by issuing
```
./submit_heavy_computation_task.sh --task_number $TASK_NUMBER
```
where $TASK_NUMBER is a value between 0 and 9.
If we submit the same task before its completion, the task will not be queue.

## Check flower from cURL
If you have ```curl``` you can check the tasks using
```
curl localhost:8888/api/tasks?offset=0
```
Beware that ```offset=0``` is required due to a bug in the specific version of Flower

## How was this project build?

If you are willing to recreate a similar project from scratch, here are some hints:

### Start a Django project within docker-compose from scratch
A good resource can be found [here](https://docs.docker.com/samples/django/).
In general, an easy way is to use this Dockerfile:
```Dockerfile
FROM python:3

ARG user=dcfuser
ARG group=dcfuser
ARG uid=1000
ARG gid=1000
ARG HOME=/home/${user}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p ${HOME} \
    && chown ${uid}:${gid} ${HOME} \
    && addgroup --gid ${gid} ${group} \
    && useradd --home ${HOME} --uid ${uid} --gid ${gid} --shell /bin/bash ${user}

USER dcfuser
ENV PATH="${PATH}:${HOME}/.local/bin"

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
```

and launch this docker-compose command:

```
docker-compose run backend-dcf django-admin startproject dcf .
```
All the subsequent modifications follow the same pattern i.e. apply a Django command throught ```docker-compose run```

