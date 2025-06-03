const axios = require('axios');
const fs = require('fs');

const apiKey = "YOUR-API-KEY";
const urls = ["https://hasdata.com", "https://example.com"];

const headers = {
  'Content-Type': 'application/json',
  'x-api-key': apiKey
};

const results = [];

async function scrapeUrls() {
  for (const url of urls) {
    const payload = {
      url: url,
      proxyType: "datacenter",
      proxyCountry: "US",
      jsRendering: true,
      extractEmails: true
    };

    try {
      const response = await axios.post("https://api.hasdata.com/scrape/web", payload, { headers });
      const data = response.data;
      const emails = data.emails || [];

      results.push({
        url: url,
        emails: emails
      });
    } catch (error) {
      console.error(`Error scraping ${url}:`, error.message);
      results.push({
        url: url,
        emails: []
      });
    }
  }

  // Save to JSON
  fs.writeFileSync("results.json", JSON.stringify(results, null, 2), 'utf-8');

  // Save to CSV
  const csvData = ["url,email"];
  results.forEach(result => {
    result.emails.forEach(email => {
      csvData.push(`${result.url},${email}`);
    });
  });
  fs.writeFileSync("results.csv", csvData.join('\n'), 'utf-8');
}

scrapeUrls();
