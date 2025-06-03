import requests
import json
import csv

api_key = "YOUR-API-KEY"
keywords = ["coffee shops NYC", "book stores Boston"]
language = "en"

headers = {
    'Content-Type': 'application/json',
    'x-api-key': api_key
}

maps_data = []
for kw in keywords:
    response = requests.get(
        "https://api.hasdata.com/scrape/google-maps/search",
        headers={"x-api-key": api_key},
        params={"q": kw, "hl": language}
    )
    if response.status_code == 200:
        data = response.json()
        for place in data.get("localResults", []):
            website = place.get("website")
            address = place.get("address")
            phone = place.get("phone")
            if website or address or phone:
                maps_data.append({
                    "website": website,
                    "address": address,
                    "phone": phone
                })

def universe_url(url):
    url = url.strip().lower()
    if not url.startswith("http"):
        url = "http://" + url
    url = url.replace("https://", "http://").replace("www.", "")
    if url.endswith("/"):
        url = url[:-1]
    return url

urls = [item['website'] for item in maps_data if item.get('website')]

scraped_data = []
for url in urls:
    norm_url = url.strip()
    if not norm_url.startswith(("http://", "https://")):
        norm_url = "http://" + norm_url

    payload = json.dumps({
        "url": norm_url,
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
        scraped_data.append({
            "Website": url,
            "Emails": emails
        })
    except Exception:
        scraped_data.append({
            "Website": url,
            "Emails": []
        })

maps_dict = {universe_url(item['website']): item for item in maps_data}
scraped_dict = {universe_url(item['Website']): item for item in scraped_data}

final_results = []
for site in urls:
    norm_site = universe_url(site)
    combined = {}

    if norm_site in scraped_dict:
        combined.update(scraped_dict[norm_site])
    else:
        combined['Website'] = site

    if norm_site in maps_dict:
        combined['Address'] = maps_dict[norm_site].get('address') or combined.get('Address', '')
        combined['Phone'] = maps_dict[norm_site].get('phone') or combined.get('Phone', '')

    final_results.append(combined)

with open("results.json", "w", encoding="utf-8") as json_file:
    json.dump(final_results, json_file, ensure_ascii=False, indent=2)

with open("results.csv", "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Website", "Emails", "Address", "Phone"])
    for res in final_results:
        emails = ", ".join(res.get("Emails", [])) if res.get("Emails") else ""
        writer.writerow([res.get("Website", ""), emails, res.get("Address", ""), res.get("Phone", "")])
