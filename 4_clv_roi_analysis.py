import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os

# 1. PostgreSQL Connection
db_user = 'postgres'
db_password = 'sumit'
db_host = 'localhost'
db_port = '5432'
db_name = 'ecommerce_db'

engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

print("Extracting Revenue Data for CLV...")

# 2. SQL Query: Calculate total lifetime revenue per customer
clv_query = """
SELECT 
    c.customer_unique_id,
    MIN(o.order_purchase_timestamp) AS first_purchase_date,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.price + oi.freight_value) AS clv_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status NOT IN ('canceled', 'unavailable')
GROUP BY c.customer_unique_id;
"""

df_clv = pd.read_sql(clv_query, engine)

print("Simulating Acquisition Channels and Calculating ROI...")

# 3. Simulate Acquisition Channels (Reproducible with a set seed)
np.random.seed(42) # Ensures the random assignment is the same every time you run it
channels = ['Organic Search', 'Paid Ads', 'Social Media', 'Direct']
probabilities = [0.40, 0.30, 0.20, 0.10] # 40% Organic, 30% Paid, etc.

df_clv['acquisition_channel'] = np.random.choice(channels, size=len(df_clv), p=probabilities)

# 4. Assign an estimated Customer Acquisition Cost (CAC) per channel
# Paid ads cost the most, Organic costs very little (just SEO maintenance)
cac_mapping = {
    'Organic Search': 5.00,
    'Paid Ads': 25.00,
    'Social Media': 15.00,
    'Direct': 2.00
}
df_clv['cac'] = df_clv['acquisition_channel'].map(cac_mapping)

# 5. Calculate Return on Investment (ROI)
# ROI Formula: (Revenue - Cost) / Cost
df_clv['roi_percentage'] = ((df_clv['clv_revenue'] - df_clv['cac']) / df_clv['cac']) * 100

# 6. Aggregate the results to find the numbers for your resume!
channel_summary = df_clv.groupby('acquisition_channel').agg(
    total_customers=('customer_unique_id', 'count'),
    average_clv=('clv_revenue', 'mean'),
    average_cac=('cac', 'mean'),
    average_roi=('roi_percentage', 'mean')
).round(2).reset_index()

# 7. Save outputs for Power BI using your absolute path!
output_dir = r"D:\sumit projects\E-Commerce-Cohort-CLV-Analyzer\ecommerce_cohort_clv\data"
os.makedirs(output_dir, exist_ok=True)

df_clv.to_csv(os.path.join(output_dir, 'customer_clv_raw.csv'), index=False)
channel_summary.to_csv(os.path.join(output_dir, 'channel_roi_summary.csv'), index=False)

print("\n--- ROI by Acquisition Channel ---")
print(channel_summary.to_string())
print("\nSuccess: CLV and ROI calculated! Files saved for Power BI.")