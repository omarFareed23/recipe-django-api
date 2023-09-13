FROM python:3.9-alpine3.13

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app

EXPOSE 8000

# create env default to false
# override it in docker-compose.yml 
ARG DEV=false

# create virtual environment to avoid some conflicts inside the container
# create user to avoid using root user
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # must be installed before installing requirements.txt as you need them to install psycopg2
    # install postgresql adapter
    # apk is a package manager for alpine linux
    apk add --update --no-cache postgresql-client && \
    # install dependencies for psycopg2
    # these packages are needed to build psycopg2 but not needed to run it
    # so we can remove them after the build
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt;\
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser --disabled-password --no-create-home django-user

# add /py/bin to the PATH
ENV PATH="/py/bin:$PATH"

# switch to the new user
USER django-user



