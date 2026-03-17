import os
import pandas as pd
from sqlalchemy import create_engine

# 1. PostgreSQL Connection Details
db_user = 'postgres'
db_password = 'sumit' 
db_host = 'localhost'
db_port = '5432'
db_name = 'ecommerce_db'

engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

print("Executing SQL Cohort Extraction...")

# 2. The Master SQL Query for Cohort Analysis
cohort_query = """
WITH customer_orders AS (
    -- Join orders and customers to get the real unique customer ID
    SELECT 
        c.customer_unique_id,
        o.order_purchase_timestamp
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
),
first_purchase AS (
    -- Find the very first month a customer made a purchase (Their Cohort)
    SELECT 
        customer_unique_id,
        DATE_TRUNC('month', MIN(order_purchase_timestamp)) AS cohort_month
    FROM customer_orders
    GROUP BY customer_unique_id
),
cohort_data AS (
    -- Map every purchase to the customer's original cohort month
    SELECT 
        fp.customer_unique_id,
        fp.cohort_month,
        DATE_TRUNC('month', co.order_purchase_timestamp) AS order_month
    FROM first_purchase fp
    JOIN customer_orders co ON fp.customer_unique_id = co.customer_unique_id
)
-- Calculate the "Cohort Index" (Month 0, Month 1, Month 2, etc.) and count customers
SELECT 
    DATE(cohort_month) AS cohort_month,
    (EXTRACT(YEAR FROM order_month) - EXTRACT(YEAR FROM cohort_month)) * 12 + 
    (EXTRACT(MONTH FROM order_month) - EXTRACT(MONTH FROM cohort_month)) AS cohort_index,
    COUNT(DISTINCT customer_unique_id) AS total_customers
FROM cohort_data
GROUP BY cohort_month, cohort_index
ORDER BY cohort_month, cohort_index;
"""

# 3. Load the SQL results directly into a Pandas DataFrame
df = pd.read_sql(cohort_query, engine)

print("Pivoting data into a Retention Matrix using Pandas...")

# 4. Pivot the data to create the Cohort Grid
# Rows = Cohort Month, Columns = Cohort Index (Months since first purchase)
cohort_matrix = df.pivot(index='cohort_month', columns='cohort_index', values='total_customers')

# 5. Calculate Retention Percentages
# Divide every column by the initial month (Month 0) to get the percentage
cohort_size = cohort_matrix.iloc[:, 0]
retention_matrix = cohort_matrix.divide(cohort_size, axis=0)
retention_matrix = retention_matrix.round(4) * 100  # Convert to percentage

# 6. Save the outputs for Power BI later
# Using an absolute raw string (r"") so Windows finds it perfectly every time
output_dir = r"D:\sumit projects\E-Commerce-Cohort-CLV-Analyzer\ecommerce_cohort_clv\data"

# Force Python to create this exact folder path if it doesn't see it
os.makedirs(output_dir, exist_ok=True)

# Save the files directly to the absolute path
cohort_matrix.to_csv(os.path.join(output_dir, 'cohort_absolute_numbers.csv'))
retention_matrix.to_csv(os.path.join(output_dir, 'cohort_retention_percentages.csv'))

print("\n--- Cohort Retention Matrix (Percentages) ---")
print(retention_matrix.iloc[-10:, :6]) 
print("\nSuccess: Cohort matrices calculated and saved to CSV for Power BI!")