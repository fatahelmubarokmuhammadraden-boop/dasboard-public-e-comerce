import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

try:
    # Load data
    @st.cache_data
    def load_data():
        orders = pd.read_csv('E-commerce-dataset/E-Commerce Public Dataset/orders_dataset.csv')
        customers = pd.read_csv('E-commerce-dataset/E-Commerce Public Dataset/customers_dataset.csv')
        products = pd.read_csv('E-commerce-dataset/E-Commerce Public Dataset/products_dataset.csv')
        order_items = pd.read_csv('E-commerce-dataset/E-Commerce Public Dataset/order_items_dataset.csv')
        order_payments = pd.read_csv('E-commerce-dataset/E-Commerce Public Dataset/order_payments_dataset.csv')
        order_reviews = pd.read_csv('E-commerce-dataset/E-Commerce Public Dataset/order_reviews_dataset.csv')
        return orders, customers, products, order_items, order_payments, order_reviews

    orders, customers, products, order_items, order_payments, order_reviews = load_data()

    # Merge data
    merged = orders.merge(customers, on='customer_id', how='left')
    merged = merged.merge(order_items, on='order_id', how='left')
    merged = merged.merge(products, on='product_id', how='left')

    # Dashboard
    st.title('Dashboard Visualisasi Data E-commerce')
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Tren Penjualan
st.header('Tren Penjualan')
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
sales_trend = orders.groupby(orders['order_purchase_timestamp'].dt.to_period('M')).size().reset_index(name='count')
sales_trend['order_purchase_timestamp'] = sales_trend['order_purchase_timestamp'].astype(str)
fig = px.line(sales_trend, x='order_purchase_timestamp', y='count', title='Tren Penjualan Bulanan')
st.plotly_chart(fig)

# Kategori Produk Teratas
st.header('Kategori Produk Teratas')
top_categories = merged['product_category_name'].value_counts().head(10)
fig = px.bar(top_categories, title='Top 10 Kategori Produk')
st.plotly_chart(fig)

# Distribusi Status Pesanan
st.header('Distribusi Status Pesanan')
status_dist = orders['order_status'].value_counts()
fig = px.pie(status_dist, title='Distribusi Status Pesanan')
st.plotly_chart(fig)

# Lokasi Pelanggan
st.header('Lokasi Pelanggan')
customer_locations = customers['customer_state'].value_counts()
fig = px.bar(customer_locations, title='Jumlah Pelanggan per Negara Bagian')
st.plotly_chart(fig)

# Tren Pendapatan
st.header('Tren Pendapatan')
orders_payments = orders.merge(order_payments, on='order_id', how='left')
orders_payments['order_purchase_timestamp'] = pd.to_datetime(orders_payments['order_purchase_timestamp'])
revenue_trend = orders_payments.groupby(orders_payments['order_purchase_timestamp'].dt.to_period('M'))['payment_value'].sum().dropna().reset_index(name='revenue')
revenue_trend['order_purchase_timestamp'] = revenue_trend['order_purchase_timestamp'].astype(str)
fig = px.line(revenue_trend, x='order_purchase_timestamp', y='revenue', title='Tren Pendapatan Bulanan')
st.plotly_chart(fig)

# Tren Skor Ulasan Rata-rata
st.header('Tren Skor Ulasan Rata-rata')
orders_reviews = orders.merge(order_reviews, on='order_id', how='left')
orders_reviews['review_creation_date'] = pd.to_datetime(orders_reviews['review_creation_date'])
review_trend = orders_reviews.groupby(orders_reviews['review_creation_date'].dt.to_period('M'))['review_score'].mean().reset_index(name='avg_score')
review_trend['review_creation_date'] = review_trend['review_creation_date'].astype(str)
fig = px.line(review_trend, x='review_creation_date', y='avg_score', title='Tren Skor Ulasan Rata-rata Bulanan')
st.plotly_chart(fig)

# Tren Waktu Pengiriman
st.header('Tren Waktu Pengiriman')
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
orders['delivery_time'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.days
delivery_trend = orders.groupby(orders['order_purchase_timestamp'].dt.to_period('M'))['delivery_time'].mean().dropna().reset_index(name='avg_delivery_time')
delivery_trend['order_purchase_timestamp'] = delivery_trend['order_purchase_timestamp'].astype(str)
fig = px.line(delivery_trend, x='order_purchase_timestamp', y='avg_delivery_time', title='Tren Waktu Pengiriman Rata-rata Bulanan (Hari)')
st.plotly_chart(fig)
