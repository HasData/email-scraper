import requests
import re
import csv

found_emails = set()
output_file = "found_emails.csv"
file_path = "urls.txt"
websites = ["https://hasdata.com", "https://example.com"]


email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}"
for website in websites:
    response = requests.get(website, timeout=10)
    if response.status_code == 200:
        emails = re.findall(email_pattern, response.text)
        for email in emails:
            found_emails.add((website, email))
    else:
        print(f"[{response.status_code}] {website}")


with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Website", "Email"])
    for website, email in found_emails:
        writer.writerow([website, email])

print(f"Saved {len(found_emails)} emails to {output_file}")
