ARG PYTHON_VERSION=3.11.1
ARG PYTHON_CONTAINER=python

FROM $PYTHON_CONTAINER:$PYTHON_VERSION-slim-buster

# install required packages for django postgis
RUN apt update && apt install -y  \
    curl \
    gcc \
    python3-dev \
    libpq-dev software-properties-common \
    gdal-bin libgdal-dev g++

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
RUN /etc/poetry/bin/poetry config virtualenvs.create false

ENV PATH="$PATH:/etc/poetry/bin"
ENV PATH="$PATH:/root/.local/bin"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFEERED=1

COPY . /app
WORKDIR /app

RUN poetry install && rm -rf /root/.cache/pypoetry && rm -rf /root/.cache/pip

EXPOSE 8080

CMD [ "gunicorn", "--reload", "-b", "0.0.0.0:8080", "payments.wsgi:application" ]
