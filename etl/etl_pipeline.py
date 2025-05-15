import pandas as pd
import sqlite3
import os

# Paths
data_path = 'C:/Users/laxmiprasanna/Documents/sales_insights_dashboard/data/Sample - Superstore.csv'
db_folder = 'C:/Users/laxmiprasanna/Documents/sales_insights_dashboard/db'
db_path = os.path.join(db_folder, 'sales.db')

# Ensure db folder exists
os.makedirs(db_folder, exist_ok=True)

# Load the CSV file
df = pd.read_csv(data_path,encoding='ISO-8859-1')

# Clean column names
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Convert dates
df['order_date'] = pd.to_datetime(df['order_date'])
df['ship_date'] = pd.to_datetime(df['ship_date'])

# Connect to SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table (only needed for extra safety — optional with `to_sql`)
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    order_id TEXT,
    order_date DATE,
    ship_date DATE,
    ship_mode TEXT,
    segment TEXT,
    country TEXT,
    city TEXT,
    state TEXT,
    region TEXT,
    product_id TEXT,
    category TEXT,
    sub_category TEXT,
    product_name TEXT,
    sales REAL,
    quantity INTEGER,
    discount REAL,
    profit REAL
)
''')

# Load data to SQL (this replaces if table already exists)
df.to_sql('sales', conn, if_exists='replace', index=False)

conn.commit()
conn.close()
print("✅ Data loaded successfully into SQLite.")