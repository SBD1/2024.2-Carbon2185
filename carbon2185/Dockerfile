FROM python:3.11-slim

ENV POSTGRES_USER=carbon_user
ENV POSTGRES_PASSWORD=carbon_password
ENV POSTGRES_DB=carbon2185
ENV POSTGRES_HOST=postgres
ENV POSTGRES_PORT=5432

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "carbon2185/main.py"]
