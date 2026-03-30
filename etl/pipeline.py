import snowflake.connector
import pandas as pd
from sqlalchemy import create_engine
from snowflake.connector.pandas_tools import write_pandas
import os
from dotenv import load_dotenv

load_dotenv()

def get_snowflake_connection():
    return snowflake.connector.connect(
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE')
    )

def load_raw_to_snowflake():
    print("Loading raw data to Snowflake...")
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM RAW_TRANSACTIONS")
    count = cursor.fetchone()[0]

    if count > 0:
        print(f"RAW_TRANSACTIONS already has {count} rows, skipping upload!")
        conn.close()
        return

    df = pd.read_csv('data/data.csv', encoding='latin-1')
    df.columns = df.columns.str.upper().str.replace(' ', '_')
    df = df.rename(columns={
        'INVOICENO': 'INVOICE_NO',
        'STOCKCODE': 'STOCK_CODE',
        'INVOICEDATE': 'INVOICE_DATE',
        'UNITPRICE': 'UNIT_PRICE',
        'CUSTOMERID': 'CUSTOMER_ID'
    })
    write_pandas(conn, df, 'RAW_TRANSACTIONS')
    conn.close()
    print(f"Loaded {len(df)} rows to Snowflake RAW_TRANSACTIONS!")

def extract_from_snowflake():
    print("Extracting from Snowflake...")
    conn = get_snowflake_connection()
    df = pd.read_sql("SELECT * FROM RAW_TRANSACTIONS", conn)
    conn.close()
    print(f"Extracted {len(df)} rows from Snowflake")
    return df

def transform_data(df):
    print("Transforming data...")
    df.columns = df.columns.str.upper()

    # Drop rows with missing CustomerID
    df = df.dropna(subset=['CUSTOMER_ID'])

    # Drop rows with negative quantity (returns)
    df = df[df['QUANTITY'] > 0]

    # Drop rows with negative price
    df = df[df['UNIT_PRICE'] > 0]

    # Drop duplicates
    df = df.drop_duplicates()

    # Calculate revenue
    df['REVENUE'] = df['QUANTITY'] * df['UNIT_PRICE']

    # Parse invoice date
    df['INVOICE_DATE'] = pd.to_datetime(df['INVOICE_DATE'])

    # Extract date parts
    df['YEAR'] = df['INVOICE_DATE'].dt.year
    df['MONTH'] = df['INVOICE_DATE'].dt.month
    df['DAY_OF_WEEK'] = df['INVOICE_DATE'].dt.day_name()

    print(f"Transformed data has {len(df)} rows")
    return df

def load_to_snowflake_cleaned(df):
    print("Loading cleaned data to Snowflake...")
    conn = get_snowflake_connection()
    write_pandas(conn, df, 'CLEANED_TRANSACTIONS')
    conn.close()
    print(f"Loaded {len(df)} rows to Snowflake CLEANED_TRANSACTIONS!")

def load_to_postgres(df):
    print("Loading to PostgreSQL...")
    user = os.getenv('POSTGRES_USER', 'postgres')
    password = os.getenv('POSTGRES_PASSWORD', 'postgres')
    host = os.getenv('POSTGRES_HOST', 'localhost')
    port = os.getenv('POSTGRES_PORT', '5432')
    db = os.getenv('POSTGRES_DB', 'ecommerce_db')

    if password:
        db_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    else:
        db_url = f"postgresql://{user}@{host}:{port}/{db}"

    engine = create_engine(db_url)
    df.columns = df.columns.str.lower()
    df.to_sql('cleaned_transactions', engine, if_exists='replace', index=False)
    print(f"Loaded {len(df)} rows to PostgreSQL!")

def run_pipeline():
    print("Starting ETL pipeline...")
    load_raw_to_snowflake()
    df = extract_from_snowflake()
    df = transform_data(df)
    load_to_snowflake_cleaned(df)
    load_to_postgres(df)
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    run_pipeline()