import pandas as pd
from sqlalchemy import create_engine
import os

# 1. PostgreSQL Connection Details
db_user = 'postgres'
db_password = 'sumit' 
db_host = 'localhost'
db_port = '5432'
db_name = 'ecommerce_db'

# Create the connection engine
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# 2. Define the path to your data folder
data_dir = 'D:\sumit projects\E-Commerce-Cohort-CLV-Analyzer\ecommerce_cohort_clv\data'

# 3. List the core files we are loading
files_to_load = {
    'customers': 'olist_customers_dataset.csv',
    'orders': 'olist_orders_dataset.csv',
    'order_items': 'olist_order_items_dataset.csv',
    'marketing_leads': 'olist_marketing_qualified_leads_dataset.csv',
    'closed_deals': 'olist_closed_deals_dataset.csv'
}

print("Starting data ingestion to PostgreSQL...")

# 4. Loop through the files, read them with Pandas, and push to SQL
for table_name, file_name in files_to_load.items():
    file_path = os.path.join(data_dir, file_name)
    
    if os.path.exists(file_path):
        print(f"Loading {file_name} into table '{table_name}'...")
        # Read the CSV
        df = pd.read_csv(file_path)
        
        # Push to PostgreSQL
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Successfully loaded {len(df)} rows into '{table_name}'.\n")
    else:
        print(f"WARNING: Could not find {file_name} in the data folder.")

print("Data ingestion complete! Your PostgreSQL database is ready.")