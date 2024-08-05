FROM python:3.10-slim

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --system --deploy

COPY . /app

EXPOSE 8080

WORKDIR src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]