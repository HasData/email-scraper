import requests
import json
import csv

api_key = "YOUR-API-KEY"
urls = ["https://hasdata.com", "https://example.com"]


headers = {
    'Content-Type': 'application/json',
    'x-api-key': api_key
}

results = []

for url in urls:
    payload = json.dumps({
        "url": url,
        "proxyType": "datacenter",
        "proxyCountry": "US",
        "jsRendering": True,
        "extractEmails": True,
    })

    try:
        response = requests.post("https://api.hasdata.com/scrape/web", headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()
        emails = data.get("emails", [])

        results.append({
            "url": url,
            "emails": emails
        })


    except Exception as e:
        results.append({
            "url": url,
            "emails": []
        })


with open("results.json", "w", encoding="utf-8") as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=2)

with open("results.csv", "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["url", "email"])  
    for result in results:
        for email in result["emails"]:
            writer.writerow([result["url"], email])
