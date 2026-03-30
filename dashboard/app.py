import streamlit as st
import requests
import pandas as pd
import plotly.express as px

import os
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 E-Commerce Analytics Dashboard")
st.markdown("Real-time insights from 500K+ transactions")

# Summary metrics
summary = requests.get(f"{API_URL}/summary").json()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"£{summary['total_revenue']:,.2f}")
col2.metric("Total Transactions", f"{summary['total_transactions']:,}")
col3.metric("Total Customers", f"{summary['total_customers']:,}")
col4.metric("Total Products", f"{summary['total_products']:,}")

st.divider()

# Monthly Revenue Chart
st.subheader("📈 Monthly Revenue Trend")
monthly = requests.get(f"{API_URL}/revenue/monthly").json()
df_monthly = pd.DataFrame(monthly)
df_monthly['period'] = df_monthly['year'].astype(str) + '-' + df_monthly['month'].astype(str).str.zfill(2)
fig1 = px.line(df_monthly, x='period', y='total_revenue', markers=True)
st.plotly_chart(fig1, use_container_width=True)

st.divider()

col_left, col_right = st.columns(2)

# Top Products
with col_left:
    st.subheader("🏆 Top 10 Products by Revenue")
    products = requests.get(f"{API_URL}/products/top").json()
    df_products = pd.DataFrame(products)
    fig2 = px.bar(df_products, x='total_revenue', y='description', orientation='h')
    st.plotly_chart(fig2, use_container_width=True)

# Sales by Country
with col_right:
    st.subheader("🌍 Sales by Country")
    countries = requests.get(f"{API_URL}/sales/by-country").json()
    df_countries = pd.DataFrame(countries)
    fig3 = px.pie(df_countries.head(10), values='total_revenue', names='country')
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# Top Customers
st.subheader("👥 Top 10 Customers")
customers = requests.get(f"{API_URL}/customers/top").json()
df_customers = pd.DataFrame(customers)
st.dataframe(df_customers, use_container_width=True)