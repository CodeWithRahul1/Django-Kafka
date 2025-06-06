# Django + Kafka + Redis + PostgreSQL Microservices with Docker Compose

This project demonstrates a microservice architecture using Django REST API with Kafka messaging, Redis caching, and PostgreSQL database — all orchestrated with Docker Compose.

---

## Features

- Django REST API for managing products and orders
- Kafka Producer sends product quantity update messages asynchronously
- Kafka Consumer listens and updates product quantities in the database and Redis cache
- Redis used as a caching layer for product quantity to speed up reads
- PostgreSQL as the main persistent store
- Docker Compose to orchestrate all services in containers

---

## Services

| Service       | Description                          |
|---------------|------------------------------------|
| **web**       | Django API server                   |
| **db**        | PostgreSQL database                 |
| **redis**     | Redis cache server                  |
| **zookeeper** | Kafka dependency for coordination  |
| **kafka**     | Kafka message broker                |
| **consumer**  | Kafka consumer service (updates qty)|

---

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject

Building a Kafka-Integrated Django Application with Docker

Introduction

In this blog post, I’ll walk you through how I built and containerized a Django application integrated with Apache Kafka to process order events and update product quantities asynchronously. This was my first time working with Kafka and Docker Compose for a complete microservices-style architecture.

Goals

Process product orders using an API

Use Kafka to decouple and asynchronously update inventory

Cache inventory in Redis for fast reads

Ensure services are containerized and orchestrated using Docker Compose

Architecture Overview

+-----------+      +------------+      +-------------+      +----------+
|  Django   | ---> | Kafka Prod | ---> | Kafka Broker| ---> | Kafka Cons|
|  Web App  |      |            |      | + Zookeeper |      |          |
+-----------+      +------------+      +-------------+      +----------+
      |                                                       |
      |-------------> Redis & PostgreSQL <---------------------|

Services:

Web App: Django API for placing orders

Kafka Producer: Sends quantity update messages when orders are created

Kafka Consumer: Listens and applies updates to DB and Redis

Redis: Caching layer for product quantity

PostgreSQL: Primary datastore

Kafka Producer Logic

In the create_order API view:

Checks if product quantity is available from Redis (fallbacks to DB if not)

Creates the order and reduces quantity

Sends a message to Kafka:

producer.send(
    settings.KAFKA_TOPIC,
    {
        'product_id': product.id,
        'new_quantity': product.quantity
    }
)

Kafka Consumer Logic

Runs independently and listens to the topic:

consumer = KafkaConsumer(
    settings.KAFKA_TOPIC,
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    data = message.value
    product = Product.objects.get(id=data['product_id'])
    product.quantity = data['new_quantity']
    product.save()
    cache.set(f"product:{product.id}:quantity", data['new_quantity'], timeout=300)

Dockerization

Dockerfile for Web App and Consumer:

FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

For consumer service, override the command in docker-compose.yml:

consumer:
  build: .
  command: python myapp/kafka_consumer.py
  depends_on:
    - kafka
    - redis
    - db

Docker Compose File:

version: '3.9'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - kafka
      - redis
      - db
    environment:
      KAFKA_BOOTSTRAP_SERVERS: kafka:9092

  consumer:
    build: .
    command: python myapp/kafka_consumer.py
    depends_on:
      - kafka

  kafka:
    image: confluentinc/cp-kafka:7.2.1
    depends_on:
      - zookeeper
    environment:
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181

  zookeeper:
    image: confluentinc/cp-zookeeper:7.2.1
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  db:
    image: postgres:14
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password

  redis:
    image: redis:7

Benefits of Kafka in This Project

Asynchronous Processing: Order processing is fast, while inventory updates happen in the background.

Decoupling: Consumer logic is separated and can scale independently.

Scalability: Kafka can handle high-throughput, and consumers can scale horizontally.

Final Thoughts

This was a significant learning experience where I got hands-on experience with:

Kafka architecture and message flow

Redis caching strategies

Docker and Compose-based microservice orchestration

Decoupling business logic for better maintainability

Excited to build on top of this! 🔥


