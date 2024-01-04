FROM python:3.12.1-alpine

RUN apk add --no-cache python3 py3-gunicorn

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install --without dev,doc

COPY . .

EXPOSE 8000

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh
#ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]