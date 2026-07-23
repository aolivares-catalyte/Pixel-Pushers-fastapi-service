# Pixel Pushers FastAPI Service

## Overview 

A CLI-driven FastAPI application built as part of a multi-day training program.
The project evolves from simple request/response handling (Day 1-2) into a real Postgres-backed API using SQLAlchemy (Day 3).
The goal is to establish strong development habits, clean architecture, and responsible use of AI tooling.

## Prerequisites

- Python 3.10 or newer
- A virtual environment (venv)
- Postgres installed locally or running via Docker
- Postman (for API verification)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/aolivares-catalyte/Pixel-Pushers-fastapi-service.git
    cd  Pixel-Pushers-fastapi-service
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3. Install required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Postgres Setup

Day 3 requires the app to connect to a real Postgres instance.

1. Install Postgres

    You may install Postgres via:

    - Local installer (postgres.org)
    - Docker (recommended)
    Example Docker command:
    
    ```bash
    docker run --name pixel-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
    ```

2. Create the Database

    Using psql:

    ```bash
    psql -U postgres
    CREATE DATABASE pixel_pushers;
    ```

    Or using pgAdmin

3. Connection Details

    The FastAPI app expects a connection string like:

    ```bash
    postgresql://postgres:postgres@localhost:5432/pixel_pushers
    ```

    In this example
    - host: localhost
    - post: 5432
    - database: pixel_pushers
    - username: postgres

## Running the Application

From the project root, run:

```bash
uvicorn main:app --reload
```

## API Endpoints

To view API endpoint information visit the /docs/ endpoint.

## Tasks Completed Day 3

- [x] Postgres Confirmed Running and Reachable
- [x] SQLAlchemy and Driver Installed
- [x] Database Connection Module Created
- [x] Product SQLAlchemy Model Created
- [x] Create/Drop Strategy Implemented
- [x] Connectivity Verified via Endpoint
- [x] Postman Collection Updated
- [x] README Updated
- [ ] Comprehension Checkpoint

## Tasks Completed Day 2

- [x] Product Pydantic Model Created
- [x] POST Endpoint Accepting the Product Model
- [x] In-Memory Storage of Products
- [x] GET /products Endpoint Returns All Products
- [x] Query Parameters Added for Searching
- [x] Validation Rules Reflecting Real Business Constraints
- [x] Postman Collection Updated
- [x] README Updated
- [x] Comprehension Checkpoint (Individual, No AI Assistance)

## Tasks Completed Day 1

- [x] GitHub Repository Created and Shared
- [x] All Team Members Added as Collaborators
- [x] .gitignore File Added
- [x] README created
- [x] Virtual Environment Created and Used
- [x] FastAPI and Uvicorn Installed
- [x] Basic "Hello World" Endpoint
- [x] Endpoint With a Path Parameter
- [x] Verification via Postman
- [x] requirements.txt Created
- [x] Comprehension Checkpoint
