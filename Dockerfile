FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN pip install docker-compose==1.29.2 && pip install poetry==1.4.2 && poetry config virtualenvs.create false

WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

COPY . .

EXPOSE 8000

CMD alembic upgrade head && uvicorn app:app --host 0.0.0.0 --port 8000
