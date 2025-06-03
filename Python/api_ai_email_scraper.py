import requests
import json
import csv

api_key = "YOUR-API-KEY"

headers = {
    'Content-Type': 'application/json',
    'x-api-key': api_key
}

results = []

with open("urls.txt", "r", encoding="utf-8") as file:
    urls = [line.strip() for line in file if line.strip()]

for url in urls:
    payload = json.dumps({
        "url": url,
        "proxyType": "datacenter",
        "proxyCountry": "US",
        "jsRendering": True,
        "extractEmails": True,
        "aiExtractRules": {
            "address": {"description": "Physical address", "type": "string"},
            "phone": {"description": "Phone number", "type": "string"},
            "email": {"description": "Email addresses", "type": "string"},
            "companyName": {"description": "Company name", "type": "string"}
        }
    })

    try:
        response = requests.post("https://api.hasdata.com/scrape/web", headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()

        emails_list = data.get("emails", [])
        ai_resp = data.get("aiResponse", {})

        company = ai_resp.get("companyName", "-")
        address = ai_resp.get("address", "-")
        phone = ai_resp.get("phone", "-")
        email_ai = ai_resp.get("email", "")

        all_emails = set(emails_list)
        if email_ai:
            all_emails.add(email_ai)

        email_combined = ", ".join(all_emails) if all_emails else ""

        results.append({
            "url": url,
            "company": company,
            "address": address,
            "phone": phone,
            "emails": email_combined
        })


    except Exception as e:
        results.append({
            "url": url,
            "company": "-",
            "address": "-",
            "phone": "-",
            "emails": ""
        })


with open("results_ai.json", "w", encoding="utf-8") as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=2)

with open("results_ai.csv", "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["url", "company", "address", "phone", "emails"])
    for result in results:
        writer.writerow([
            result["url"],
            result["company"],
            result["address"],
            result["phone"],
            result["emails"]
        ])