1. Install Docker and docker-compose.
2. Apply environment:
```
cp sample.env .env
```
4. Install dependencies:

```
pipenv install
pipenv shell
```
5. Up docker-compose:

```
docker-compose up -d
```
6.Migrate database:
```
alembic upgrade head
```
7. Run the server:

```
cd src
uvicorn main:app --reload
```
8. Run Celery
```
celery -A tasks.tasks:celery worker --loglevel=INFO
```
