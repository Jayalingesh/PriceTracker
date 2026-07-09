import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

DB_NAME = "database.db"
OUTPUT_DIR = "reports"

def generate_charts(product_name):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    conn = sqlite3.connect(DB_NAME)
    query = """
        SELECT Timestamp, Price 
        FROM price_history
        WHERE Product_Name = ?
        ORDER BY Timestamp ASC
    """

    df = pd.read_sql_query(query, conn, params=(product_name,))
    conn.close()

    if df.empty:
        print(f"⚠️ No historical data found to chart for: {product_name[:30]}...")
        return None
    
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    plt.figure(figsize=(10,5))

    plt.plot(df['Timestamp'], df['Price'], marker='o', linestyle='-', color='#1f77b4', linewidth=2)

    short_title = product_name[:40] + "..." if len(product_name) >40 else product_name
    plt.title(f"Price Trend Analytics: {short_title}", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Date & time of Check", fontsize=11, labelpad=10)
    plt.ylabel("Price (INR / $)", fontsize=11, labelpad=10)
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.gcf().autofmt_xdate()
    plt.tight_layout()

    safe_filename = "".join([c for c in short_title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    chart_path = os.path.join(OUTPUT_DIR, f"{safe_filename.replace(' ', '_')}_trend.png")

    plt.savefig(chart_path, dpi=300)
    plt.close()

    print(f"📈 Analytics Report Generated! Chart saved to: {chart_path}")
    return chart_path
