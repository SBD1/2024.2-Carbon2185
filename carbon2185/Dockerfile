FROM python:3.12.3

ENV POSTGRES_USER=carbon_user
ENV POSTGRES_PASSWORD=carbon_password
ENV POSTGRES_DB=carbon2185
ENV POSTGRES_HOST=postgres
ENV POSTGRES_PORT=5432

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "main.py"]
