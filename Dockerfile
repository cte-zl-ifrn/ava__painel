FROM python:3.12.1-slim-bookworm

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get -y install --no-install-recommends curl=7.88.1-10+deb12u5 vim=2:9.0.1378-2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /

RUN pip install --upgrade --no-cache-dir 'pip>=24.0' && \
    pip install --no-cache-dir -r /requirements.txt

COPY requirements-dev.txt /apps/req/requirements-dev.txt
WORKDIR /apps/req

RUN pip install --no-cache-dir -r requirements-dev.txt

# FIX: bug on corsheaders
# RUN echo 'import django.dispatch;check_request_enabled = django.dispatch.Signal()' > /usr/local/lib/python3.10/site-packages/corsheaders/signals.py

COPY src /apps/app
WORKDIR /apps/app
RUN python manage.py collectstatic --noinput

EXPOSE 8000
# ENTRYPOINT [ "executable" ]
WORKDIR /apps/app
CMD ["python", "manage.py", "runserver_plus", "0.0.0.0:80"]
