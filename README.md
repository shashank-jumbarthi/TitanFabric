# TitanFabric

TitanFabric is a lightweight fabric sourcing and quote-management MVP for mills, boutiques, and production teams. It includes a polished static frontend, a small Python API, seed data, database schema, Docker configuration, and basic tests.

## Features

- Browse a curated textile catalog by category, composition, sustainability, and price.
- Build an inquiry cart with yardage and shipping destination estimates.
- Submit quote requests through a JSON API.
- Serve a static frontend from any web server or directly from disk.
- Run the backend locally or through Docker.

## Project Structure

```text
frontend/     Static web app
backend/      Python API and catalog logic
database/     SQLite schema and seed data
docker/       Backend Dockerfile
docs/         API and project documentation
tests/        Unit tests
scripts/      Local helper scripts
```

## Run The Frontend

Open [frontend/index.html](frontend/index.html) in a browser, or serve the repo root:

```bash
python3 -m http.server 8080
```

Then visit `http://localhost:8080/frontend/`.

## Run The Backend

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m backend.app
```

The API will be available at `http://127.0.0.1:8000`.

## Run Tests

```bash
python3 -m unittest discover -s tests
```

## Docker

```bash
docker compose up --build
```

The API will run on `http://127.0.0.1:8000`.
