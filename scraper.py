#prodect link  https://www.amazon.in/EVM-667MHz-Long-DIMM-Desktop-EVMT2G6670U86P/dp/B09XXSM31J?ref_=Oct_d_oup_d_1375384031_1&pd_rd_w=lzwmd&content-id=amzn1.sym.0c079df2-9f62-4f0f-8600-d01f02c41a29&pf_rd_p=0c079df2-9f62-4f0f-8600-d01f02c41a29&pf_rd_r=D8CXXA0M6PKHYE6Q9FD2&pd_rd_wg=fZnTX&pd_rd_r=0eb7c5a7-3a98-458e-9c2d-2ca5b90c2938&pd_rd_i=B09XXSM31J&th=1
#Price selector  corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center.aok-relative.apex-core-price-identifier > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay.apex-pricetopay-value > span:nth-child(2) > span.a-price-whole
# Prodect title selector #productTitle


from playwright.sync_api import sync_playwright
import time
from pipeline import clean_and_store_data

def run():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=False)
        page = browser.new_page()
        
        target_url = "https://www.amazon.in/EVM-667MHz-Long-DIMM-Desktop-EVMT2G6670U86P/dp/B09XXSM31J?ref_=Oct_d_oup_d_1375384031_1&pd_rd_w=lzwmd&content-id=amzn1.sym.0c079df2-9f62-4f0f-8600-d01f02c41a29&pf_rd_p=0c079df2-9f62-4f0f-8600-d01f02c41a29&pf_rd_r=D8CXXA0M6PKHYE6Q9FD2&pd_rd_wg=fZnTX&pd_rd_r=0eb7c5a7-3a98-458e-9c2d-2ca5b90c2938&pd_rd_i=B09XXSM31J&th=1"
        print(f"Navigating to prodect page...")
        page.goto(target_url, wait_until="load")
 
        time.sleep(2)

        #title = page.title()
        #print(f"Successfully connected! Website Title: {title}")
        
        try:
            price_selector = "span.a-price .a-offscreen"
            page.wait_for_selector(price_selector, timeout=5000)

            raw_price = page.inner_text(price_selector)

            title_selector = "#productTitle"
            prodect_name = page.inner_text(title_selector) if "REPLACE" not in title_selector else "Target Item"

            #print("\n--- DATA HARVESTED ---")
            #print(f"Prodect: {prodect_name.strip()}")
            #print(f"Raw Price Found: {raw_price.strip()}")
            #print("----------------------\n")
        
        except Exception as e:
            print(f"\nError finding the element: {e}")
            print("Tip: The website might be using dynamic IDs or anti-bot measures. We can adjust for this!\n")

    
        browser.close()
    return prodect_name, raw_price

if __name__== "__main__":
    run()