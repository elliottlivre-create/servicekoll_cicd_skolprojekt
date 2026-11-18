FROM python:3.15-slim

# Python skriver inga .pyc-filer och loggar direkt (syns i docker logs)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Egen användare så att appen inte körs som root
RUN useradd --create-home --uid 1000 appuser

# Beroenden först: det lagret återanvänds från cache så länge requirements.txt inte ändras
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

# Pipelinen skickar in commit-SHA:n här, så /version visar exakt vilken kod som körs
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION} \
    APP_ENV=container

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]