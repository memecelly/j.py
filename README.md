# 📰 Zimbabwe Job Scraper – VacancyMail Automation

This Python script scrapes the **10 most recent job postings** from [https://vacancymail.co.zw/jobs/](https://vacancymail.co.zw/jobs/), extracts key details, and saves them to a CSV file. It includes built-in **logging**, **error handling**, and optional **scheduling** support for automation.

---

## 📌 Features

- ✅ Scrapes the latest 10 job listings from [VacancyMail Zimbabwe](https://vacancymail.co.zw/jobs/)
- 📦 Extracts:
  - Job Title
  - Company
  - Location
  - Expiry Date
  - Job Description
  - Job URL
- 📁 Saves scraped data into `scraped_data.csv`
- 🧠 Logs events and errors into `scrape_log.log`
- ⏰ Supports scheduled scraping using the `schedule` library

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/job-scraper.git
cd job-scraper
