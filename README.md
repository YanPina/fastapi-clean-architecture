# 🚀 FastAPI Clean Architecture

This project is a **FastAPI** boilerplate following **Clean Architecture** and **Test-Driven Development (TDD)** principles. It provides a scalable and maintainable backend structure with well-defined layers, dependency injection, and full test coverage.

## 📂 Project Structure

```
📦 src/
├── application/         # Use cases (business logic)
├── core/                # Core configurations and utilities
├── domain/              # Entities and domain models
├── infrastructure/      # Database models, repositories, security
├── interfaces/          # API routes and controllers
├── main.py              # FastAPI app entry point
├── tests/               # Unit and integration tests
```

## 🎯 What This Project Can Be Used For

This project serves as a **base template** for building **scalable FastAPI applications** using best practices like:
- **Clean Architecture** (separating business logic from frameworks and tools)
- **Dependency Injection** for flexibility and testability
- **Asynchronous Programming** for high-performance APIs
- **JWT Authentication** for secure user authentication
- **Alembic Migrations** for database version control
- **Pre-Commit Hooks** for consistent code quality

This template is ideal for building **microservices, RESTful APIs, and production-ready applications**.

---

## 📦 Project Setup

### 1️⃣ Install Dependencies

Ensure you have Poetry installed. If not, install it first:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Then, install dependencies:
```bash
poetry install
```

### 2️⃣ Pre-Commit Hooks

This project uses pre-commit hooks for linting and formatting. To set them up, run:
```bash
poetry run pre-commit install
```

To manually run the hooks on all files:
```bash
poetry run pre-commit run --all-files
```

To run only on modified and new files:
```bash
poetry run pre-commit run --files $(git ls-files -m -o)
```

### 3️⃣ Running PostgreSQL with Docker

Start the PostgreSQL database using Docker:
```bash
docker-compose up -d
```

This will start a PostgreSQL container with the following credentials:
- **User**: `myuser`
- **Password**: `mypassword`
- **Database**: `mydatabase`
- **Port**: `5432`

## 🔄 Database Migrations with Alembic

### ✨ Creating a New Migration
To generate a new migration file after modifying models:
```bash
poetry run alembic revision --autogenerate -m "Your migration message"
```

### 🚀 Applying Migrations
To apply database migrations:
```bash
poetry run alembic upgrade head
```

### ⏪ Rolling Back a Migration
To revert the last applied migration:
```bash
poetry run alembic downgrade -1
```

## 🛠 Development Tools & Configurations

### 📏 Code Formatting & Linting

This project uses several tools for code quality:
- **Black**: Code formatter (`poetry run black .`)
- **Ruff**: Linter and auto-fixer (`poetry run ruff .`)
- **isort**: Organizes imports (`poetry run isort .`)
- **mypy**: Static type checking (`poetry run mypy .`)

All these are executed automatically via `pre-commit` hooks.

### 🧪 Running Tests

To run unit tests with pytest:
```bash
poetry run pytest
```

---

Feel free to **contribute** or **customize** it to fit your needs! 🚀

