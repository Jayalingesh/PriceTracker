import pandas as pd 
import sqlite3
from datetime import datetime

DB_NAME = "database.db"

def clean_and_store_data(product_name, raw_price):
    print("Starting data cleaning pipeline...")

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cleaned_price_str = raw_price.replace("$", "").replace("₹", "").replace(",", "").strip()


    try:
        final_price = float(cleaned_price_str)
    
    except ValueError:
        print(f"Error: Could not convert '{raw_price}' to a number.")
        return
    
    data = {
        "Timestamp":[current_time],
        "Product_Name": [product_name],
        "Price": [final_price]
    }
    
    df = pd.DataFrame(data)

    #print("\n--- Cleaned Data Prepared ---")
    #print(df.to_string(index=False))

    print("\n=============================================")
    print("📋 CLEANED DATA PREPARED FOR STORAGE")
    print("=============================================")

    display_df = df.copy()

    display_df['Product_Name'] = display_df['Product_Name'].apply(
        lambda x: x[:30] +"..." if len(x) > 30 else x
    )

    display_df['Price'] = display_df['Price'].map("{:,.2f}".format)

    print(display_df.to_string(index=False, justify='left'))
    print("=============================================\n")

    conn = sqlite3.connect(DB_NAME)

    df.to_sql("price_history", conn, if_exists="append", index=False)

    conn.close()

    print(f"💾 Successfully saved to {DB_NAME} inside 'price_history' table.\n")

