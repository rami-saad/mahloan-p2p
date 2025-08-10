# Mahloan P2P Lending Platform 

A cloud-based peer‑to‑peer lending simulation that models the loan lifecycle from request to repayment. Built to showcase backend API development, Infrastructure as Code, CI/CD automation, and AWS deployment patterns.

## Features
- REST APIs for loan creation, approval, funding, and repayment
- MySQL persistence via SQLAlchemy ORM + Alembic migrations
- Dockerized API and local DB using `docker compose`
- CI with GitHub Actions (unit tests on every push/PR)
- Ready for Infra‑as‑Code (Terraform scaffolding)

## Tech Stack
**Python**, **FastAPI**, **SQLAlchemy**, **Alembic**, **MySQL**, **Docker**, **GitHub Actions**

## 🗺 Architecture (high‑level)
1. Clients call FastAPI endpoints
2. API runs in a container (local or EC2)
3. MySQL stores state (local container or RDS)
4. Logs/metrics can flow to CloudWatch (extension point)

![Architecture Diagram](docs/architecture.png)

## Quickstart (Docker)
```bash
git clone https://github.com/rami-saad/mahloan-p2p.git
cd mahloan-p2p
docker compose up --build
# API -> http://localhost:8000/docs
```

## Local Dev (venv)
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## API (examples)
```
POST /loans                # create
POST /loans/{id}/approve # approve
POST /loans/{id}/fund    # fund
POST /loans/{id}/repay?amount=123.45
GET  /loans/{id}         # fetch
GET  /metrics              # sample metrics
```

## Testing
```bash
pytest -q
```

## Roadmap
- JWT auth & role‑based endpoints
- Request throttling / rate limiting
- Basic cost dashboards (CloudWatch or Prometheus)
