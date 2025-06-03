const axios = require('axios');
const fs = require('fs');

const foundEmails = new Set();
const outputFile = 'found_emails.csv';
const websites = ['https://hasdata.com', 'https://example.com'];
const emailPattern = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}/g;

(async () => {
    for (const website of websites) {
        try {
            const response = await axios.get(website, { timeout: 10000 });
            const emails = response.data.match(emailPattern);
            if (emails) {
                emails.forEach(email => {
                    foundEmails.add(`${website},${email}`);
                });
            }
        } catch (error) {
            console.log(`[Error] ${website}: ${error.response?.status || error.message}`);
        }
    }

    const csvHeader = 'Website,Email\n';
    const csvContent = Array.from(foundEmails).join('\n');
    fs.writeFileSync(outputFile, csvHeader + csvContent, 'utf8');

    console.log(`Saved ${foundEmails.size} emails to ${outputFile}`);
})();
