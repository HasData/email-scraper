const axios = require('axios');
const fs = require('fs');
const { Parser } = require('json2csv');

const apiKey = 'YOUR-API-KEY';
const keywords = ['restaurant in New York', 'coffee shop in Los Angeles'];
const country = 'US';
const language = 'en';
const numRes = 10;

const headers = {
    'Content-Type': 'application/json',
    'x-api-key': apiKey
};

async function fetchUrlsFromKeywords() {
    let urls = [];

    for (const kw of keywords) {
        try {
            const response = await axios.get(
                'https://api.hasdata.com/scrape/google-light/serp',
                {
                    headers: { 'x-api-key': apiKey },
                    params: { q: kw, gl: country, hl: language, num: numRes }
                }
            );
            const data = response.data;
            const organicResults = data.organicResults || [];
            for (const item of organicResults) {
                if (item.link) {
                    urls.push(item.link);
                }
            }
        } catch (error) {
            // skip on error
        }
    }

    return urls;
}

async function fetchEmailsFromUrls(urls) {
    let results = [];

    for (const url of urls) {
        const payload = {
            url: url,
            proxyType: 'datacenter',
            proxyCountry: country,
            jsRendering: true,
            extractEmails: true
        };

        try {
            const response = await axios.post(
                'https://api.hasdata.com/scrape/web',
                payload,
                { headers }
            );
            const data = response.data;
            const emails = data.emails || [];
            results.push({ url: url, emails: emails });
        } catch (error) {
            results.push({ url: url, emails: [] });
        }
    }

    return results;
}

async function saveResults(results) {
    fs.writeFileSync('results.json', JSON.stringify(results, null, 2), 'utf-8');

    const csvData = [];
    for (const result of results) {
        for (const email of result.emails) {
            csvData.push({ url: result.url, email: email });
        }
    }

    const parser = new Parser({ fields: ['url', 'email'] });
    const csv = parser.parse(csvData);
    fs.writeFileSync('results.csv', csv, 'utf-8');
}

async function main() {
    const urls = await fetchUrlsFromKeywords();
    const results = await fetchEmailsFromUrls(urls);
    await saveResults(results);
}

main();
