![Python](https://img.shields.io/badge/python-3.10+-blue)
![Node.js](https://img.shields.io/badge/node.js-18+-green)


# Email Scraper Examples (Python & Node.js)
[![HasData_bannner](banner.png)](https://hasdata.com/)

This repository contains practical scripts to extract email addresses from web pages using Python and Node.js. It includes examples for both regex-based and API-based extraction, covering single sites, multiple URLs, and AI-enhanced scraping.

## Table of Contents

1. [Requirements](#requirements)
2. [Project Structure](#project-structure)
3. [Email Scraping Examples](#email-scraping-examples)
   * [Regex Email Scraping](#regex-email-scraping)
   * [API Email Scraping (HasData)](#api-email-scraping-hasdata)
   * [AI Email Extraction (HasData)](#ai-email-extraction-hasdata)
   * [Google SERP Email Extraction](#google-serp-email-extraction)
   * [Google Maps Email Extraction](#google-maps-email-extraction)

## Requirements

**Python 3.10+** or **Node.js 18+**

### Python Setup

Required packages:

* `requests`

Install:

```bash
pip install requests
```

### Node.js Setup

Required packages:

* `axios`

Install:

```bash
npm install axios
```

## Project Structure

```
email-scraping-examples/
│
├── python/
│   ├── regex_single_site.py
│   ├── regex_urls_from_file.py
│   ├── regex_urls_from_list.py
│   ├── api_email_scraper.py
│   ├── api_ai_email_scraper.py
│   ├── api_urls_from_file.py
│   ├── api_urls_from_list.py
│   ├── google_serp_scraper.py
│   ├── google_maps_scraper.py
│
├── nodejs/
│   ├── regex_single_site.js
│   ├── regex_urls_from_file.js
│   ├── regex_urls_from_list.js
│   ├── api_email_scraper.js
│   ├── api_ai_email_scraper.js
│   ├── api_urls_from_file.js
│   ├── api_urls_from_list.js
│   ├── google_serp_scraper.js
│   ├── google_maps_scraper.js
│
└── README.md
```

Each script focuses on a specific method of email extraction. No frameworks. Just clean and minimal examples to get things done.

## Email Scraping Examples

Full article with [email scraping examples](https://hasdata.com/blog/email-scraping) you can find at hasdata.com.

### Regex Email Scraping

Extract emails using regular expressions from a given URL or multiple URLs (from a file or list).

| Parameter      | Description                  | Example                            |
| -------------- | ---------------------------- | ---------------------------------- |
| `target_url`   | URL to scrape emails from    | `'https://example.com'`            |
| `file_path`    | File with URLs (for batch)   | `'urls.txt'`                       |
| `output_file`  | File to save found emails    | `'emails.txt'`                     |

### API Email Scraping (HasData)

Use HasData's web scraping API to extract emails, phone numbers, addresses, and company names from websites.

| Parameter      | Description                  | Example                                      |
| -------------- | ---------------------------- | -------------------------------------------- |
| `api_key`      | HasData API key              | `'your-api-key'`                             |
| `target_url`   | Website URL to scrape        | `'https://example.com'`                      |

### AI Email Extraction (HasData)

Use HasData’s **AI extraction** feature to extract emails and additional details from complex websites.

| Parameter        | Description                                | Example                 |
| ---------------- | ------------------------------------------ | ----------------------- |
| `api_key`        | API key for HasData service                 | `'YOUR-API-KEY'`        |
| `urls.txt`       | File containing list of URLs to scrape     | `'urls.txt'`            |
| `proxyType`      | Type of proxy to use for requests           | `'datacenter'`          |
| `proxyCountry`   | Proxy country code to route requests through | `'US'`                  |
| `jsRendering`    | Enable JavaScript rendering on pages        | `True`                  |
| `aiExtractRules` | AI extraction rules for address, phone, email, company | See script for JSON structure |
| `results_ai.json`| Output JSON file with scraped data          | `'results_ai.json'`     |
| `results_ai.csv` | Output CSV file with scraped data           | `'results_ai.csv'`      |


### Google SERP Email Extraction

Search Google for specific queries and extract emails from the resulting URLs.

| Parameter    | Description                            | Example                         |
|--------------|------------------------------------|--------------------------------|
| `api_key`    | Your HasData API key                 | `"YOUR-API-KEY"`               |
| `keywords`   | List of search queries for Google SERP | `["restaurant in New York", "coffee shop in Los Angeles"]` |
| `country`    | Country code for localized search   | `"US"`                        |
| `language`   | Language code for search results    | `"en"`                        |
| `num_res`    | Number of organic results per query | `10`                          |
| `urls`       | List of URLs collected from SERP    | `["https://example.com", "https://another.com"]` |
| `results`    | List of dictionaries with URL and extracted emails | `[{"url": "https://example.com", "emails": ["info@example.com"]}]` |



### Google Maps Email Extraction

Extract emails and contact details from Google Maps listings for a given keyword and location.

| Parameter     | Description                                | Example                         |
| ------------- | ------------------------------------------ | ------------------------------- |
| `api_key`     | API key for HasData API                     | `'YOUR-API-KEY'`                |
| `keywords`    | List of keywords to search in Google Maps  | `["coffee shops NYC", "book stores Boston"]` |
| `language`    | Language code for Google Maps search        | `'en'`                         |
| `results.json`| Output JSON file with combined results      | `'results.json'`                |
| `results.csv` | Output CSV file with combined results       | `'results.csv'`                 |



## Disclaimer

These examples are for **educational purposes** only. Learn more about [the legality of web scraping](https://hasdata.com/blog/is-web-scraping-legal).
