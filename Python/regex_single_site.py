import requests
import re

found_emails = set()
url = "https://example.com"
response = requests.get(url, timeout=10)
if response.status_code == 200:
    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}"
    emails = re.findall(email_pattern, response.text)
    for email in emails:
        found_emails.add((url, email))
else:
    print(f"[{response.status_code}] {url}")

print(url, " | ", emails)