FROM python:3.12.1-alpine

RUN apk add --no-cache python3 py3-gunicorn

# set work directory
WORKDIR /usr/src/app

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install --without dev,doc

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]