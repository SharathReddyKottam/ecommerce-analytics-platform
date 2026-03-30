import pandas as pd
import pytest
import sys
sys.path.insert(0, '.')
from etl.pipeline import transform_data

def get_sample_data():
    data = {
        'INVOICE_NO': ['536365', '536365', '536366', '536367', '536368'],
        'STOCK_CODE': ['85123A', '71053', '84406B', '84029G', '84029E'],
        'DESCRIPTION': ['WHITE HANGING HEART', 'WHITE METAL LANTERN', 'CREAM CUPID HEARTS', 'KNITTED UNION FLAG', 'RED WOOLLY HOTTIE'],
        'QUANTITY': [6, -1, 8, 6, -2],
        'INVOICE_DATE': ['12/1/2010 8:26', '12/1/2010 8:26', '12/1/2010 8:34', '12/1/2010 8:34', '12/1/2010 8:34'],
        'UNIT_PRICE': [2.55, 3.39, 2.75, 3.39, -1.00],
        'CUSTOMER_ID': ['17850.0', '17850.0', None, '13047.0', '13047.0'],
        'COUNTRY': ['United Kingdom', 'United Kingdom', 'United Kingdom', 'United Kingdom', 'United Kingdom']
    }
    return pd.DataFrame(data)

def test_negative_quantity_removed():
    df = transform_data(get_sample_data())
    assert (df['QUANTITY'] <= 0).sum() == 0

def test_negative_price_removed():
    df = transform_data(get_sample_data())
    assert (df['UNIT_PRICE'] <= 0).sum() == 0

def test_missing_customer_removed():
    df = transform_data(get_sample_data())
    assert df['CUSTOMER_ID'].isnull().sum() == 0

def test_revenue_calculated():
    df = transform_data(get_sample_data())
    assert 'REVENUE' in df.columns
    assert (df['REVENUE'] > 0).all()

def test_year_month_extracted():
    df = transform_data(get_sample_data())
    assert 'YEAR' in df.columns
    assert 'MONTH' in df.columns
    assert 'DAY_OF_WEEK' in df.columns