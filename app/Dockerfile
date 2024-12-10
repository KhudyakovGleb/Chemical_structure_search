FROM python:3.12-alpine3.20

ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

RUN pip3 install --no-cache-dir \
  virtualenv==20.26.2 \
  pip==24.1.1 \
  pyyaml==6.0.1

RUN mkdir -p $POETRY_HOME && \
  python3 -m venv $POETRY_HOME && \
  $POETRY_HOME/bin/pip install poetry==1.8.3

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
  poetry install --no-root --only main

COPY . /app

ENTRYPOINT [ "fastapi", "run" ]
