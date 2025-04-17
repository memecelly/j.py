import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import logging
import schedule
import time

# --- CONFIG ---
BASE_URL = "https://vacancymail.co.zw"
JOBS_URL = f"{BASE_URL}/jobs/"
LOG_FILE = "scrape_log.log"
CSV_FILE = "scraped_data.csv"

# --- Logging Setup ---
logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

def scrape_jobs():
    logging.info("Started scraping job listings.")
    try:
        response = requests.get(JOBS_URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        job_links = soup.select('.job-list-item a[href]')[:10]

        job_data = []

        for link in job_links:
            job_url = BASE_URL + link['href']
            try:
                job_page = requests.get(job_url, timeout=10)
                job_page.raise_for_status()
                job_soup = BeautifulSoup(job_page.content, 'html.parser')

                job_info = {
                    "Job Title": job_soup.find("h1").get_text(strip=True) if job_soup.find("h1") else "N/A",
                    "Company": job_soup.select_one(".company_name").get_text(strip=True) if job_soup.select_one(".company_name") else "N/A",
                    "Location": job_soup.select_one(".location").get_text(strip=True) if job_soup.select_one(".location") else "N/A",
                    "Expiry Date": (
                        datetime.strptime(job_soup.select_one(".expiry").get_text(strip=True), "%d %b, %Y").strftime("%Y-%m-%d")
                        if job_soup.select_one(".expiry") else "N/A"
                    ),
                    "Description": job_soup.select_one(".job-description").get_text(strip=True) if job_soup.select_one(".job-description") else "N/A",
                    "URL": job_url
                }

                job_data.append(job_info)
                logging.info(f"Scraped: {job_info['Job Title']} at {job_info['Company']}")

            except Exception as e:
                logging.error(f"Error scraping job page {job_url}: {e}")

        df = pd.DataFrame(job_data)
        df.drop_duplicates(inplace=True)
        df.to_csv(CSV_FILE, index=False)
        logging.info(f"Scraped data saved to {CSV_FILE}")
        print("✅ Data scraping complete.")

    except Exception as e:
        logging.error(f"Failed to scrape job listings: {e}")
        print("❌ An error occurred. Check scrape_log.log for details.")

# --- Optional Scheduling ---
def run_schedule():
    schedule.every().day.at("08:00").do(scrape_jobs)  # change to .hourly, .minutes etc. if needed
    logging.info("Job scraper scheduled. Running loop...")

    while True:
        schedule.run_pending()
        time.sleep(60)

# --- Run Directly ---
if __name__ == "__main__":
    scrape_jobs()
    # Uncomment to enable scheduling:
    # run_schedule()
