const axios = require('axios');

const apiKey = 'YOUR-API-KEY';
const url = 'https://example.com';

const headers = {
    'Content-Type': 'application/json',
    'x-api-key': apiKey
};

const payload = {
    url: url,
    proxyType: 'datacenter',
    proxyCountry: 'US',
    jsRendering: true,
    extractEmails: true
};

axios.post('https://api.hasdata.com/scrape/web', payload, { headers })
    .then(response => {
        const data = response.data;
        const emails = data.emails || [];
        console.log(`${url} | ${emails}`);
    })
    .catch(error => {
        console.error(`Error: ${error.response ? error.response.status : error.message}`);
    });
