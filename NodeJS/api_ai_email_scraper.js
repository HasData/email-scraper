const fs = require('fs');
const axios = require('axios');

const apiKey = 'YOUR-API-KEY';

const headers = {
  'Content-Type': 'application/json',
  'x-api-key': apiKey
};

let urls = fs.readFileSync('urls.txt', 'utf-8')
  .split('\n')
  .map(line => line.trim())
  .filter(line => line);

const results = [];

async function scrapeUrl(url) {
  const payload = {
    url: url,
    proxyType: 'datacenter',
    proxyCountry: 'US',
    jsRendering: true,
    extractEmails: true,
    aiExtractRules: {
      address: { description: 'Physical address', type: 'string' },
      phone: { description: 'Phone number', type: 'string' },
      email: { description: 'Email addresses', type: 'string' },
      companyName: { description: 'Company name', type: 'string' }
    }
  };

  try {
    const response = await axios.post('https://api.hasdata.com/scrape/web', payload, { headers });
    const data = response.data;

    const emailsList = data.emails || [];
    const aiResp = data.aiResponse || {};

    const company = aiResp.companyName || '-';
    const address = aiResp.address || '-';
    const phone = aiResp.phone || '-';
    const emailAI = aiResp.email || '';

    const allEmails = new Set(emailsList);
    if (emailAI) {
      allEmails.add(emailAI);
    }

    results.push({
      url,
      company,
      address,
      phone,
      emails: Array.from(allEmails).join(', ')
    });
  } catch (error) {
    console.error(`Error scraping ${url}: ${error.message}`);
    results.push({
      url,
      company: '-',
      address: '-',
      phone: '-',
      emails: ''
    });
  }
}

(async () => {
  for (const url of urls) {
    await scrapeUrl(url);
  }

  // Save as JSON
  fs.writeFileSync('results_ai.json', JSON.stringify(results, null, 2), 'utf-8');

  // Save as CSV
  const csvHeader = 'url,company,address,phone,emails\n';
  const csvRows = results.map(r => 
    `"${r.url}","${r.company}","${r.address}","${r.phone}","${r.emails}"`
  );
  const csvContent = csvHeader + csvRows.join('\n');
  fs.writeFileSync('results_ai.csv', csvContent, 'utf-8');

  console.log('Scraping completed. Results saved to results_ai.json and results_ai.csv');
})();
