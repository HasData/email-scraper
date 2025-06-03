const axios = require('axios');
const fs = require('fs');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

const apiKey = 'YOUR-API-KEY';

const headers = {
    'Content-Type': 'application/json',
    'x-api-key': apiKey
};

const urls = fs.readFileSync('urls.txt', 'utf-8')
    .split('\n')
    .map(line => line.trim())
    .filter(line => line);

const results = [];

(async () => {
    for (const url of urls) {
        const payload = {
            url: url,
            proxyType: 'datacenter',
            proxyCountry: 'US',
            jsRendering: true,
            extractEmails: true
        };

        try {
            const response = await axios.post('https://api.hasdata.com/scrape/web', payload, { headers });
            const data = response.data;
            const emails = data.emails || [];

            results.push({ url: url, emails: emails });

        } catch (error) {
            console.error(`Error for URL ${url}: ${error.message}`);
            results.push({ url: url, emails: [] });
        }
    }

    // Save JSON
    fs.writeFileSync('results.json', JSON.stringify(results, null, 2), 'utf-8');

    // Save CSV
    const csvWriter = createCsvWriter({
        path: 'results.csv',
        header: [
            { id: 'url', title: 'url' },
            { id: 'email', title: 'email' }
        ]
    });

    const csvRecords = results.flatMap(result =>
        result.emails.map(email => ({ url: result.url, email: email }))
    );

    await csvWriter.writeRecords(csvRecords);
    console.log('Results saved to results.json and results.csv');

})();
