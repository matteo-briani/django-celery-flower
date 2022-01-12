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
