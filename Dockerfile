FROM python:3.10-slim

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

ENV PORT 8080

RUN pipenv install --system --deploy

COPY . /app

WORKDIR src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", $PORT]