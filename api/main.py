from fastapi import FastAPI
from sqlalchemy import create_engine, text
import pandas as pd
import os
from dotenv import load_dotenv
from etl.pipeline import run_pipeline

load_dotenv()

app = FastAPI(title="E-Commerce Analytics API")

def get_engine():
    db_url = f"postgresql://{os.getenv('POSTGRES_USER')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    return create_engine(db_url)

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/run-pipeline")
def trigger_pipeline():
    run_pipeline()
    return {"message": "Pipeline completed!"}

@app.get("/revenue/monthly")
def monthly_revenue():
    engine = get_engine()
    df = pd.read_sql("""
                     SELECT year, month, ROUND(SUM(revenue)::numeric, 2) as total_revenue
                     FROM cleaned_transactions
                     GROUP BY year, month
                     ORDER BY year, month
                     """, engine)
    return df.to_dict(orient='records')

@app.get("/products/top")
def top_products():
    engine = get_engine()
    df = pd.read_sql("""
                     SELECT description,
                            ROUND(SUM(revenue)::numeric, 2) as total_revenue,
                            SUM(quantity) as total_quantity
                     FROM cleaned_transactions
                     GROUP BY description
                     ORDER BY total_revenue DESC
                         LIMIT 10
                     """, engine)
    return df.to_dict(orient='records')

@app.get("/customers/top")
def top_customers():
    engine = get_engine()
    df = pd.read_sql("""
                     SELECT customer_id,
                            ROUND(SUM(revenue)::numeric, 2) as total_spent,
                            COUNT(DISTINCT invoice_no) as total_orders
                     FROM cleaned_transactions
                     GROUP BY customer_id
                     ORDER BY total_spent DESC
                         LIMIT 10
                     """, engine)
    return df.to_dict(orient='records')

@app.get("/sales/by-country")
def sales_by_country():
    engine = get_engine()
    df = pd.read_sql("""
                     SELECT country,
                            ROUND(SUM(revenue)::numeric, 2) as total_revenue,
                            COUNT(DISTINCT customer_id) as total_customers
                     FROM cleaned_transactions
                     GROUP BY country
                     ORDER BY total_revenue DESC
                     """, engine)
    return df.to_dict(orient='records')

@app.get("/summary")
def summary():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM cleaned_transactions", engine)
    return {
        "total_transactions": len(df),
        "total_revenue": round(float(df['revenue'].sum()), 2),
        "total_customers": int(df['customer_id'].nunique()),
        "total_products": int(df['stock_code'].nunique()),
        "top_country": df['country'].value_counts().index[0],
        "date_range": f"{df['invoice_date'].min()} to {df['invoice_date'].max()}"
    }