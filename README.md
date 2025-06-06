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
