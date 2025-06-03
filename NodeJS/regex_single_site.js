const axios = require('axios');

const foundEmails = new Set();
const url = 'https://example.com';

axios.get(url, { timeout: 10000 })
  .then(response => {
    const emailPattern = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}/g;
    const emails = response.data.match(emailPattern) || [];
    emails.forEach(email => {
      foundEmails.add(`${url} | ${email}`);
    });

    if (emails.length > 0) {
      console.log(url, ' | ', emails);
    } else {
      console.log(`${url} | No emails found`);
    }
  })
  .catch(error => {
    if (error.response) {
      console.log(`[${error.response.status}] ${url}`);
    } else {
      console.log(`[Error] ${url}: ${error.message}`);
    }
  });
