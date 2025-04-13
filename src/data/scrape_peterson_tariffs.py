"""src/data/scrape_peterson_tariffs.py"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

def scrape_peterson_tariff_timeline():
    """
    Scrapes the Peterson Institute trade conflict timeline using Selenium + headless Chrome.
    Returns a DataFrame of tariff-related events from 2000 to present.
    """

    # 1. Set Chrome options to run headless (no browser window)
    options = Options()
    options.add_argument("--headless=new")  # Use new headless mode for Chrome 109+
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")  # Suppress logging output

    # 2. Launch headless Chrome (chromedriver is installed via Conda)
    driver = webdriver.Chrome(options=options)

    # 3. Navigate to the target URL
    url = "https://www.piie.com/research/trade-conflict-timeline"
    driver.get(url)

    # 4. Let the JavaScript render (wait a few seconds just to be safe)
    time.sleep(3)

    # 5. Find all event rows
    rows = driver.find_elements(By.CLASS_NAME, "timeline-row")
    if not rows:
        driver.quit()
        raise ValueError("No timeline rows found. The page structure may have changed.")

    data = []

    # 6. Extract each date and event description
    for row in rows:
        try:
            date = row.find_element(By.CLASS_NAME, "date-display-single").text.strip()
            event = row.find_element(By.CLASS_NAME, "views-field-body").text.strip()
            data.append((date, event))
        except Exception:
            continue  # Skip if any part is missing or malformed

    # 7. Close the browser
    driver.quit()

    # 8. Create a DataFrame and filter by date
    df = pd.DataFrame(data, columns=["Date", "Event"])
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df[df["Date"].dt.year >= 2000].dropna().reset_index(drop=True)

    return df


