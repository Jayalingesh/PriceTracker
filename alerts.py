#https://discord.com/api/webhooks/1517039636600324197/DSA5no1qtyJN_q-rQVvhfPqEXlCMB-4SyP5mD9FmFsNPJlevGcWclhV4rDKCzpJe8cPq

import requests 

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1517039636600324197/DSA5no1qtyJN_q-rQVvhfPqEXlCMB-4SyP5mD9FmFsNPJlevGcWclhV4rDKCzpJe8cPq"

def send_price_alert(product_name, old_price, new_price):

    savings = old_price - new_price
    discount = (savings / old_price) * 100

    payload = {
        "username" : "Price Intelligence Bot",
        "avatar_url" : "https://cdn-icons-png.flaticon.com/512/2611/2611130.png",
        "embeds" : [
            {
                "title": "🚨 PRICE DROP DETECTED! 🚨",
                "description": f"The system detected a price reduction for **{product_name}**.",
                "color": 3066993,  # Green color code
                "fields": [
                    {
                        "name": "Previous Price",
                        "value": f"${old_price:,.2f}",
                        "inline": True
                    },
                    {
                        "name": "New Price",
                        "value": f"**${new_price:,.2f}**",
                        "inline": True
                    },
                    {
                        "name": "Total Savings",
                        "value": f"${savings:,.2f} ({discount:.1f}% OFF)",
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "Automated Competitor Price Tracker & Analyzer"
                }
            }
        ]
    }

    print(f"Sending alert to Discord for {product_name}...")
    response = requests.post(DISCORD_WEBHOOK, json = payload)

    if response.status_code == 204:
        print("🚀 Alert sent successfully!")
    else:
        print(f"❌ Failed to send alert. Status code: {response.status_code}")

if __name__ == "__main__":
    send_price_alert("PlayStation 5 Pro", 699.99, 599.99)