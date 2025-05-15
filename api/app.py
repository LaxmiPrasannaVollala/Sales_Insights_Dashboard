from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Full absolute path to your sales.db file
DB_PATH = r'C:/Users/laxmiprasanna/Documents/sales_insights_dashboard/db/sales.db'

def get_connection():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"❌ Database not found at {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return "✅ Sales Insights Dashboard API is running!"

@app.route('/top-products')
def top_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT product_name, SUM(sales) as total_sales
        FROM sales
        GROUP BY product_name
        ORDER BY total_sales DESC
        LIMIT 10
    """)
    rows = cursor.fetchall()
    return jsonify([dict(row) for row in rows])

@app.route('/revenue-by-region')
def revenue_by_region():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT region, ROUND(SUM(sales), 2) as revenue
        FROM sales
        GROUP BY region
    """)
    rows = cursor.fetchall()
    return jsonify([dict(row) for row in rows])

if __name__ == '__main__':
    app.run(debug=True)