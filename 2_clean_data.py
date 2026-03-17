from sqlalchemy import create_engine, text

# 1. PostgreSQL Connection Details
db_user = 'postgres'
db_password = 'sumit' 
db_host = 'localhost'
db_port = '5432'
db_name = 'ecommerce_db'

engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

print("Starting Data Cleaning Process...")

# 2. Define our SQL Cleaning Commands
cleaning_queries = [
    # Convert order timestamps from TEXT to actual TIMESTAMP objects
    """
    ALTER TABLE orders 
    ALTER COLUMN order_purchase_timestamp TYPE TIMESTAMP 
    USING order_purchase_timestamp::timestamp;
    """,
    
    # Remove orders that were canceled or unavailable
    """
    DELETE FROM orders 
    WHERE order_status IN ('canceled', 'unavailable');
    """,
    
    # Clean up the marketing leads dates
    """
    ALTER TABLE marketing_leads 
    ALTER COLUMN first_contact_date TYPE TIMESTAMP 
    USING first_contact_date::timestamp;
    """
]

# 3. Execute the queries
try:
    with engine.connect() as connection:
        for query in cleaning_queries:
            connection.execute(text(query))
            connection.commit() # Save the changes to the database
        print("Success: Dates converted to timestamps and canceled orders removed!")
except Exception as e:
    print(f"An error occurred: {e}")