# E-Commerce Analytics Platform

End-to-end data engineering platform processing 541,909 real e-commerce
transactions through Snowflake, ETL pipeline, PostgreSQL, FastAPI REST API,
and Streamlit dashboard with Docker deployment.

## Architecture
```
Kaggle Dataset (541,909 rows)
        ↓
Snowflake (RAW + CLEANED tables)
        ↓
ETL Pipeline (Python + Pandas)
        ↓
PostgreSQL (app database)
        ↓
FastAPI (REST API)
        ↓
Streamlit (dashboard)
        ↓
Docker-compose (3 containers)
        ↓
AWS EC2 (deployed)
```

## Tech Stack
- **Data Source**: Kaggle UK E-Commerce Dataset (541,909 real transactions)
- **Data Warehouse**: Snowflake (RAW + CLEANED layers)
- **ETL**: Python + Pandas (removes returns, nulls, duplicates)
- **App Database**: PostgreSQL
- **REST API**: FastAPI (6 endpoints)
- **Dashboard**: Streamlit + Plotly
- **Containers**: Docker + docker-compose (3 containers)
- **Registry**: Docker Hub (multi-platform ARM64 + AMD64)
- **Cloud**: AWS EC2
- **CI/CD**: GitHub Actions (5 pytest tests)

## Dashboard Metrics
| Metric | Value |
|---|---|
| Total Revenue | £8,887,208.89 |
| Transactions | 392,692 |
| Customers | 4,338 |
| Products | 3,665 |

## API Endpoints
| Endpoint | Method | Description |
|---|---|---|
| /health | GET | Health check |
| /summary | GET | Overall metrics |
| /revenue/monthly | GET | Monthly revenue trend |
| /products/top | GET | Top 10 products by revenue |
| /customers/top | GET | Top 10 customers |
| /sales/by-country | GET | Sales by country |
| /run-pipeline | POST | Trigger ETL pipeline |

## Pipeline Flow
1. Download Kaggle dataset (541,909 rows)
2. Load raw data to Snowflake RAW_TRANSACTIONS
3. ETL cleans data → 392,692 rows remain
4. Load to Snowflake CLEANED_TRANSACTIONS
5. Load to PostgreSQL for API
6. FastAPI serves data as JSON
7. Streamlit visualizes insights

## Local Setup
```bash
# Clone repo
git clone https://github.com/SharathReddyKottam/ecommerce-analytics-platform.git

# Create .env file (see .env.example)
cp .env.example .env

# Start all services
docker-compose up -d

# Run ETL pipeline
docker-compose exec api python etl/pipeline.py

# Visit dashboard
open http://localhost:8501
```

## CI/CD
GitHub Actions runs 5 pytest tests on every push:
- Negative quantities removed
- Negative prices removed
- Missing customers removed
- Revenue calculated correctly
- Year/month columns extracted