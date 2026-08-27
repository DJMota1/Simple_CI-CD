# Simple API — CI/CD & DevOps Pipeline

A simple REST API (FastAPI + PostgreSQL) built as a hands-on project to learn and demonstrate a complete DevOps pipeline: containerization, automated testing, CI/CD, infrastructure as code, and monitoring.

🔗 **Live API:** https://simple-api-ujyi.onrender.com/docs


## Architecture

```
┌─────────────┐     push      ┌──────────────┐
│  Git/Local  │ ─────────────▶│   GitHub     │
└─────────────┘                └──────┬───────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    ▼                                      ▼
            ┌────────────────┐                   ┌──────────────────┐
            │ GitHub Actions  │                   │      Render      │
            │  (CI: tests)    │                   │ (CD: auto-deploy)│
            └────────────────┘                   └────────┬─────────┘
                                                            │
                                                  ┌─────────┴─────────┐
                                                  ▼                   ▼
                                          ┌───────────────┐   ┌───────────────┐
                                          │  FastAPI App   │──▶│  PostgreSQL   │
                                          └───────────────┘   └───────────────┘

Infrastructure provisioned via Terraform (see /terraform)
Local monitoring stack: Prometheus + Grafana (docker-compose)
```

## Tech Stack

- **API:** Python, FastAPI, SQLModel
- **Database:** PostgreSQL
- **Containerization:** Docker, Docker Compose
- **CI:** GitHub Actions (automated testing on every push)
- **CD:** Render (auto-deploy on push to `main`)
- **Infrastructure as Code:** Terraform (Render provider)
- **Monitoring:** Prometheus, Grafana
- **Testing:** Pytest, SQLite (in-memory test database)

## Running Locally

### Prerequisites
- Docker and Docker Compose installed

### Setup

1. Clone the repository:
```bash
   git clone https://github.com/DJMota1/Simple_CI-CD.git
   cd Simple_CI-CD
```

2. Copy the example environment file and adjust if needed:
```bash
   cp .env.example .env
```

3. Start the full stack (API + PostgreSQL + Prometheus + Grafana):
```bash
   docker compose up --build
```

4. Available services:
   | Service | URL |
   |---|---|
   | API docs (Swagger) | http://localhost:8000/docs |
   | Prometheus | http://localhost:9090 |
   | Grafana | http://localhost:3000 (login: `admin` / `admin`) |

### Running Tests

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest -v
```
## Project Structure

```
.
├── main.py                    # FastAPI application
├── test_main.py                # Automated tests
├── requirements.txt
├── Dockerfile
├── docker-compose.yml          # Full local stack: API, DB, Prometheus, Grafana
├── .env.example                 # Environment variables template
├── prometheus/
│   └── prometheus.yml          # Prometheus scrape configuration
├── terraform/
│   ├── main.tf                  # Render infrastructure definition
│   └── variables.tf
└── .github/
    └── workflows/
        └── ci.yml                # GitHub Actions CI pipeline
```

## CI/CD Pipeline

**Continuous Integration (GitHub Actions):**
On every push or pull request to `main`, the pipeline:
1. Spins up a temporary PostgreSQL service
2. Installs dependencies
3. Runs the automated test suite (`pytest`)

**Continuous Deployment (Render):**
Render is connected directly to the GitHub repository. Every push to `main` that passes CI automatically triggers a new build and deployment — no manual steps required.

## Infrastructure as Code

The Render infrastructure (PostgreSQL database + Web Service) is defined and provisioned using Terraform, located in `/terraform`.

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

This avoids manual configuration through the Render dashboard and makes the infrastructure reproducible and version-controlled.

## Monitoring

The local stack includes Prometheus and Grafana for observability:
- The API is instrumented with `prometheus-fastapi-instrumentator`, exposing metrics at `/metrics`
- Prometheus scrapes these metrics every 5 seconds
- Grafana visualizes request rate, latency, and memory usage on a custom dashboard

## Security Notes

- Secrets (`.env`, `terraform.tfvars`) are excluded from version control via `.gitignore` and are never committed
- The Render API key and database credentials are managed as environment variables, not hardcoded
- The `.env.example` file documents required variables without exposing real values
