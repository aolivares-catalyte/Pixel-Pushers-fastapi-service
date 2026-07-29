# Pixel Pushers FastAPI Service

## Overview

**Pixel Pushers FastAPI Service** is a training project that evolves across multiple days:

- **Day 1-2:** basic request handling and in-memory data
- **Day 3+:** real **Postgres + SQLAlchemy** integration
- **Day 4-6:** production-style API behavior, validation, and test coverage

The focus is on clean architecture, dependable API behavior, and strong development habits.

---

## Prerequisites

Make sure these are installed before running the project:

- **Python 3.10+**
- **Virtual environment** support (`venv`)
- **Postgres** (local install or Docker)
- **Postman** (manual API verification)
- **Pytest** (automated verification)

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/aolivares-catalyte/Pixel-Pushers-fastapi-service.git
cd Pixel-Pushers-fastapi-service
```

2. **Create and activate a virtual environment**

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Postgres Setup

Starting on **Day 3**, the app uses a real Postgres database.

1. **Install Postgres**

- Local installer: https://www.postgresql.org/
- Docker (recommended):

```bash
docker run --name pixel-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
```

2. **Create the database**

Using `psql`:

```sql
CREATE DATABASE pixel_pushers;
```

Or create it with **pgAdmin**.

3. **Connection string format**

```text
postgresql://postgres:postgres@localhost:5432/pixel_pushers
```

Connection values in this example:

- **host:** `localhost`
- **port:** `5432`
- **database:** `pixel_pushers`
- **username:** `postgres`

4. **Add the database URL to a `.env` file**

Create a `.env` file in the project root and store your database URL there:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/pixel_pushers
```

The application should read the database connection from this environment variable.

---

## Running the Application

From the project root:

```bash
uvicorn main:app --reload
```

Useful routes:

- `/docs` - interactive OpenAPI docs
- `/products` - product endpoints

---

## Tasks Completed Day 6

- [x] Introduced pytest for automated API verification
- [x] Created required tests
- [x] Happy path tests
- [x] Bad path tests
- [x] Not Found path tests
- [x] Added validation tests for PUT/PATCH/POST
- [x] Ensured tests hit real Postgres (no mocks)
- [x] Cleaned up configuration modules
- [x] Ensured predictable test behavior (no external state dependency)
- [x] Verified FastAPI/Pydantic error message structure
- [x] Updated README
- [x] Comprehension Checkpoint

## Tasks Completed Day 5

- [x] Added `PUT /products/{id}` for full updates
- [x] Added `PATCH /products/{id}` for partial updates
- [x] Added `DELETE /products/{id}` with soft delete behavior
- [x] Implemented consistent error responses (`404`, `422`)
- [x] Extended day technical spec (did not replace it)
- [x] Enforced validation rules for update operations
- [x] Confirmed no SQLAlchemy leakage in update/delete responses
- [x] Verified new endpoints via Postman
- [x] Updated README
- [x] Comprehension Checkpoint

## Tasks Completed Day 4

- [x] day4-spec technical specification
- [x] Reviewed personal specifications with team
- [x] Stored product objects in Postgres
- [x] Listed all products
- [x] Got product by ID
- [x] Searched products by name and optional unit
- [x] Enforced response model
- [x] Added database session dependency
- [x] Added input validation
- [x] Maintained consistent API shape
- [x] Avoided SQLAlchemy leakage
- [x] Comprehension Checkpoint

## Tasks Completed Day 3

- [x] Postgres confirmed running and reachable
- [x] SQLAlchemy and driver installed
- [x] Database connection module created
- [x] Product SQLAlchemy model created
- [x] Create/drop strategy implemented
- [x] Connectivity verified via endpoint
- [x] Postman collection updated
- [x] README updated
- [ ] Comprehension Checkpoint

## Tasks Completed Day 2

- [x] Product Pydantic model created
- [x] POST endpoint accepts product model
- [x] In-memory storage for products
- [x] `GET /products` returns all products
- [x] Query parameters added for searching
- [x] Validation rules reflecting business constraints
- [x] Postman collection updated
- [x] README updated
- [x] Comprehension Checkpoint (individual, no AI assistance)

## Tasks Completed Day 1

- [x] GitHub repository created and shared
- [x] Team collaborators added
- [x] `.gitignore` added
- [x] README created
- [x] Virtual environment created and used
- [x] FastAPI and Uvicorn installed
- [x] Basic "Hello World" endpoint
- [x] Endpoint with a path parameter
- [x] Verified via Postman
- [x] `requirements.txt` created
- [x] Comprehension Checkpoint
