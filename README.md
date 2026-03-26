# 🛒 E-Commerce Customer Retention & CLV Pipeline
**An End-to-End Analytics Engine for Olist Brazilian E-Commerce Data**

![Dashboard Preview](dashboard_preview.png)

## 📊 Executive Summary
This project transforms 100k+ raw marketplace records into a strategic growth tool. By engineering a high-performance data pipeline (PostgreSQL + Python), I identified critical customer churn points and quantified the ROI of acquisition channels. 

**Key Business Impact:** Identified that Organic Search yields a **[XX]% higher ROI** than Paid Ads, providing a data-backed case for shifting marketing budget toward SEO.

---

## 🛠️ Tech Stack & Methodology
* **Database:** PostgreSQL (Relational modeling & Data Ingestion)
* **Languages:** Python 3.10 (Pandas, SQLAlchemy, NumPy)
* **BI & Visualization:** Power BI (DAX, Conditional Formatting, Heatmap Modeling)
* **Version Control:** Git/GitHub

---

## 📈 Statistical Key Performance Indicators (KPIs)
I focused on three primary dimensions of the "Olist" ecosystem:

1.  **Retention (Cohort Analysis):**
    * **Metric:** Month-over-Month (MoM) Retention Rate.
    * **Logic:** Grouped customers by "First Purchase Month" to track the decay of the customer base.
    * **Insight:** Found a baseline Month-1 retention of **[X.X]%**, highlighting the "one-time buyer" nature of the marketplace model.

2.  **Customer Lifetime Value (CLV):**
    * **Formula:** `CLV = Sum(Total Revenue) / Unique Customers`
    * **Significance:** Moving beyond "Average Order Value" to understand the long-term worth of a customer.

3.  **Channel Efficiency (ROI/CAC):**
    * **Method:** Simulated deterministic acquisition channels (Organic, Paid, Social, Direct).
    * **Outcome:** Quantified the **Return on Investment (ROI)** by netting Lifetime Revenue against Acquisition Costs (CAC).

---

## ⚙️ Data Pipeline Architecture
1.  **Ingestion:** Python-driven migration of Olist CSVs into a structured PostgreSQL schema.
2.  **Transformation:** SQL-based cleaning (casting `order_purchase_timestamp`, filtering `canceled` orders, and joining `customer_unique_id`).
3.  **Modeling:** * Python scripts calculate the **Cohort Index** (Months elapsed since first touch).
    * Pandas used to pivot absolute numbers into a **Retention Matrix percentage**.
4.  **Visualization:** Interactive Power BI dashboard with a conditional-formatting heatmap and ROI distribution charts.

---

## 📂 Project Structure
* `1_load_data.py`: Ingestion logic from CSV to SQL.
* `2_clean_data.py`: SQL-based data prep & type casting.
* `3_cohort_analysis.py`: Python logic for the retention matrix.
* `4_clv_roi_analysis.py`: ROI and CLV calculation engine.
* `ecommerce_dashboard.pbix`: The source Power BI report.

---
**Contact:** [Sumit P] | [Link to LinkedIn]
