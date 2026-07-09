import sqlite3
import pandas as pd
from scraper import run
from pipeline import clean_and_store_data, DB_NAME
from alerts import send_price_alert
from analytics import generate_charts

def get_last_recorded_price(product_name):
    conn = sqlite3.connect(DB_NAME)
    query = """
        SELECT Price FROM price_history 
        WHERE Product_Name = ? 
        ORDER BY Timestamp DESC 
        LIMIT 1
    """

    try:
        df= pd.read_sql_query(query, conn, params=(product_name,))
        conn.close()

        if not df.empty:
            return float(df['Price'].iloc[0])
        return None
    
    except Exception:
        conn.close()
        return None
    
def execution_pipeline():
    print("=========================================")
    print("🚀 STARTING PRICE INTELLIGENCE RECON...")
    print("=========================================\n")

    product_name, raw_price = run()

    if not raw_price or not product_name:
        print("❌ Scraper failed to fetch data. Aborting pipeline run.")
        return
    
    clean_current_price = float(raw_price.replace("$", "").replace("₹", "").replace(",", "").strip())

    last_price = get_last_recorded_price(product_name)

    if last_price is not None:
        print(f"📊 Historical Match Found!")
        print(f"   -> Last Recorded Price: ${last_price:.2f}")
        print(f"   -> Current Scraped Price: ${clean_current_price:.2f}")

        if clean_current_price < last_price:
            print("📉 Price drop detected! Initiating Alert Engine...")
            send_price_alert(product_name, last_price, clean_current_price)

        else:
            print("↔️ Price is stable or has increased. No alert required.")
    
    else:
        print("🆕 First time tracking this product. Establishing baseline in database.")

    clean_and_store_data(product_name, raw_price)
    generate_charts(product_name)
    print("=========================================")
    print("🏁 PIPELINE RUN COMPLETE SUCCESSFULY")
    print("=========================================")



if __name__ == "__main__":
    execution_pipeline()