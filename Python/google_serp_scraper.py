import requests
import json
import csv

api_key = "YOUR-API-KEY"
keywords = ["restaurant in New York", "coffee shop in Los Angeles"]
country = "US"
language = "en"
num_res = 10

headers = {
    'Content-Type': 'application/json',
    'x-api-key': api_key
}

urls = []

for kw in keywords:
    try:
        response = requests.get(
            "https://api.hasdata.com/scrape/google-light/serp",
            headers={"x-api-key": api_key},
            params={"q": kw, "gl": country, "hl": language, "num": num_res}
        )
        response.raise_for_status()
        data = response.json()
        organic_results = data.get("organicResults", [])
        for item in organic_results:
            url = item.get("link")
            if url:
                urls.append(url)
    except Exception:
        pass

results = []

for url in urls:
    payload = json.dumps({
        "url": url,
        "proxyType": "datacenter",
        "proxyCountry": country,
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

    except Exception:
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
