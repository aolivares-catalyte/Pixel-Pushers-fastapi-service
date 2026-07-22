# Pixel Pushers FastAPI Service

## Overview 

A CLI based FastAPI app running locally that helps establish habits for using Cursor responsibly.

## Prerequisites

- Python 3.10 or newer
- A virtual environment for dependency isolation

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

## Running the Application

From the project root, run:

```bash
uvicorn main:app --reload
```

## API Endpoints

To view API endpoint information visit the /docs/ endpoint.

## Tasks Completed Day 2

- [x] Ingredient Pydantic Model Created
- [x] POST Endpoint Accepting the Product Model
- [x] In-Memory Storage of Products
- [x] GET /products Endpoint Returns All Products
- [x] Query Parameters Added for Searching
- [x] Validation Rules Reflecting Real Business Constraints
- [x] Postman Collection Updated
- [x] README Updated
- [ ] Comprehension Checkpoint (Individual, No AI Assistance)

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
