FROM python:3.9.7-slim-buster

ENV PYTHONUNBUFFERED 1

ENV TODODEMO_DIR=/usr/src/app/tododemo

RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && apt-get update \
    && apt-get purge --auto-remove \
    && apt-get clean \
    && apt-get install -y python3-dev default-libmysqlclient-dev build-essential gcc

RUN python -m pip install --upgrade pip

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir -p ${TODODEMO_DIR}

WORKDIR ${TODODEMO_DIR}
COPY . ${TODODEMO_DIR}

# to be executed correctly in the environments (envconsul)
# startup commands are placed in shell script,
# so that application can have correctly access to environment variables
RUN chmod +x start-app.sh
CMD sh start-app.sh
