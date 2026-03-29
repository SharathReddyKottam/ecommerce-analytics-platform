## API Endpoints
| Endpoint | Method | Description |
|---|---|---|
| /health | GET | Health check |
| /summary | GET | Overall metrics |
| /revenue/monthly | GET | Monthly revenue trend |
| /products/top | GET | Top 10 products |
| /customers/top | GET | Top 10 customers |
| /sales/by-country | GET | Sales by country |
| /run-pipeline | POST | Trigger ETL pipeline |

## Dashboard Insights
- £8,887,208 total revenue
- 392,692 cleaned transactions
- 4,338 unique customers
- 3,665 unique products
- Monthly revenue trend
- Top products by revenue
- Sales breakdown by country

## Setup
1. Clone the repo
2. Create Kaggle account → download API key → place in ~/.kaggle/
3. Create Snowflake free trial account
4. Create .env file (see .env.example)
5. Install dependencies: `pip install -r requirements.txt`
6. Run setup SQL in Snowflake: `snowflake/setup.sql`
7. Download dataset: `python data/download_data.py`
8. Run pipeline: `python etl/pipeline.py`
9. Start API: `uvicorn api.main:app --port 8000`
10. Start dashboard: `streamlit run dashboard/app.py`