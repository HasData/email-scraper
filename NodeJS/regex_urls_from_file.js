const fs = require('fs');
const axios = require('axios');

const filePath = 'urls.txt';
const outputFile = 'found_emails.csv';

const emailRegex = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g;

(async () => {
    try {
        const websites = fs.readFileSync(filePath, 'utf-8')
            .split('\n')
            .map(line => line.trim())
            .filter(line => line);

        const foundEmails = new Set();

        for (const website of websites) {
            try {
                const response = await axios.get(website, { timeout: 10000 });
                const emails = response.data.match(emailRegex) || [];
                emails.forEach(email => {
                    foundEmails.add(`${website},${email}`);
                });
            } catch (error) {
                if (error.response) {
                    console.log(`[${error.response.status}] ${website}`);
                } else {
                    console.log(`[Error] ${website}: ${error.message}`);
                }
            }
        }

        const csvData = ['Website,Email', ...Array.from(foundEmails)].join('\n');
        fs.writeFileSync(outputFile, csvData, 'utf-8');
        console.log(`Saved ${foundEmails.size} emails to ${outputFile}`);
    } catch (err) {
        console.error(`Error: ${err.message}`);
    }
})();
