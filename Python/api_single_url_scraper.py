import requests
import json

api_key = "YOUR-API-KEY"
url= "https://example.com"

headers = {
    'Content-Type': 'application/json',
    'x-api-key': api_key
}

payload = json.dumps({
    "url": url,
    "proxyType": "datacenter",
    "proxyCountry": "US",
    "jsRendering": True,
    "extractEmails": True,
})

response = requests.post("https://api.hasdata.com/scrape/web", headers=headers, data=payload)
response.raise_for_status()
data = response.json()
emails = data.get("emails", [])
print(url, " | ", emails)
