# Travel Planner API

A RESTful API for managing travel projects and places, integrated with the [Art Institute of Chicago API](https://api.artic.edu/docs/).

## Setup & Run

### Prerequisites

- Python 3.13+
- [Poetry](https://python-poetry.org/docs/#installation)

### Local

```bash
git clone https://github.com/Maks-Siglov/travel-planner.git
cd travel-planner

cp .env.example .env
poetry install
make run
```

The app starts at **http://127.0.0.1:8000**

### Docker

```bash
cp .env.example .env
docker compose up --build
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_PATH` | SQLite database file path | `travel_planner.db` |
| `ARTIC_BASE_URL` | Art Institute of Chicago API base URL | `https://api.artic.edu/api/v1` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `LOG_IN_CONSOLE` | Print logs to console | `1` |
| `LOG_FILE` | Log file path | `logs/travel_planner.log` |

## Architecture

```
Request → API Route → Service → Client / Repository            
```

- **API routes** (`src/api/`) — Thin layer. Accepts requests, validates input via Pydantic schemas, delegates to services, returns responses. No business logic.
- **Services** (`src/services/`) — Business logic. Orchestrates calls to repositories and external clients. Raises domain exceptions (`NotFoundError`, `BusinessLogicError`, `ExternalAPIError`).
- **Repositories** (`src/db/repositories/`) — Database access via SQLAlchemy. All queries, creates, updates, deletes.
- **Clients** (`src/clients/`) — Third-party API integration (Art Institute of Chicago).
- **DI Container** (`src/system/resources.py`) — All dependencies wired via `dependency-injector`. Services and clients are injected into routes using `@inject` + `Depends(Provide[...])`.

## Tech Stack

- **Python 3.13+**, **FastAPI**, **SQLAlchemy 2.0**, **Pydantic v2**
- **SQLite** (file-based, no setup required)
- **dependency-injector** for IoC
- **httpx** for external API calls
- **loguru** for logging
- **ruff** for linting

## Database

SQLite with auto-creation on startup (no migrations needed). Two tables:

- **projects** — `id`, `name`, `description`, `start_date`, `is_completed`
- **places** — `id`, `project_id`, `external_id`, `title`, `notes`, `visited` (unique constraint on `project_id` + `external_id`)

## API Documentation

Interactive Swagger UI is available at **http://127.0.0.1:8000/docs**

### Endpoints

#### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/projects` | Create project (optionally with places) |
| `GET` | `/api/v1/projects` | List projects (paginated) |
| `GET` | `/api/v1/projects/{id}` | Get project with its places |
| `PATCH` | `/api/v1/projects/{id}` | Update project |
| `DELETE` | `/api/v1/projects/{id}` | Delete project |

#### Places

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/projects/{id}/places` | Add place to project |
| `GET` | `/api/v1/projects/{id}/places` | List places (paginated) |
| `GET` | `/api/v1/projects/{id}/places/{place_id}` | Get single place |
| `PATCH` | `/api/v1/projects/{id}/places/{place_id}` | Update place (notes, visited) |

### Request Examples

**Create project with places:**
```json
POST /api/v1/projects
{
  "name": "Art Tour",
  "description": "Visit famous artworks",
  "start_date": "2026-06-01",
  "place_external_ids": [27992, 28560]
}
```

**Add place to project:**
```json
POST /api/v1/projects/1/places
{
  "external_id": 129884
}
```

**Update place:**
```json
PATCH /api/v1/projects/1/places/1
{
  "notes": "Must see!",
  "visited": true
}
```

### Business Rules

- Each place is validated against the Art Institute of Chicago API before being stored
- A project can have between 1 and 10 places
- No duplicate places (same `external_id`) within a project
- A project cannot be deleted if any of its places are marked as visited
- When all places in a project are marked as visited, the project is automatically marked as completed

### Pagination

List endpoints support `page` and `per_page` query parameters:

```
GET /api/v1/projects?page=1&per_page=10
```

Response includes `items`, `total`, `page`, `per_page`, and `pages`.
