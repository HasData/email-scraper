const axios = require("axios");
const fs = require("fs");

const apiKey = "YOUR-API-KEY";
const keywords = ["coffee shops NYC", "book stores Boston"];
const language = "en";

const headers = {
  "Content-Type": "application/json",
  "x-api-key": apiKey,
};

async function main() {
  let mapsData = [];

  for (const kw of keywords) {
    try {
      const response = await axios.get(
        "https://api.hasdata.com/scrape/google-maps/search",
        {
          headers: { "x-api-key": apiKey },
          params: { q: kw, hl: language },
        }
      );
      if (response.status === 200) {
        const localResults = response.data.localResults || [];
        localResults.forEach((place) => {
          if (place.website || place.address || place.phone) {
            mapsData.push({
              website: place.website,
              address: place.address,
              phone: place.phone,
            });
          }
        });
      }
    } catch {
      // ignore errors
    }
  }

  function universeUrl(url) {
    let normalized = url.trim().toLowerCase();
    if (!/^http/.test(normalized)) normalized = "http://" + normalized;
    normalized = normalized.replace("https://", "http://").replace("www.", "");
    if (normalized.endsWith("/")) normalized = normalized.slice(0, -1);
    return normalized;
  }

  const urls = mapsData
    .map((item) => item.website)
    .filter((w) => w && w.length > 0);

  let scrapedData = [];

  for (const url of urls) {
    let normUrl = url.trim();
    if (!/^https?:\/\//i.test(normUrl)) {
      normUrl = "http://" + normUrl;
    }

    const payload = {
      url: normUrl,
      proxyType: "datacenter",
      proxyCountry: "US",
      jsRendering: true,
      extractEmails: true,
    };

    try {
      const resp = await axios.post(
        "https://api.hasdata.com/scrape/web",
        payload,
        { headers }
      );
      const data = resp.data;
      const emails = data.emails || [];
      scrapedData.push({ Website: url, Emails: emails });
    } catch {
      scrapedData.push({ Website: url, Emails: [] });
    }
  }

  const mapsDict = {};
  mapsData.forEach((item) => {
    if (item.website) {
      mapsDict[universeUrl(item.website)] = item;
    }
  });

  const scrapedDict = {};
  scrapedData.forEach((item) => {
    if (item.Website) {
      scrapedDict[universeUrl(item.Website)] = item;
    }
  });

  const finalResults = [];

  for (const site of urls) {
    const normSite = universeUrl(site);
    const combined = {};

    if (scrapedDict[normSite]) {
      Object.assign(combined, scrapedDict[normSite]);
    } else {
      combined.Website = site;
    }

    if (mapsDict[normSite]) {
      combined.Address =
        mapsDict[normSite].address || combined.Address || "";
      combined.Phone = mapsDict[normSite].phone || combined.Phone || "";
    }

    finalResults.push(combined);
  }

  fs.writeFileSync("results.json", JSON.stringify(finalResults, null, 2), {
    encoding: "utf-8",
  });

  const csvLines = [];
  csvLines.push(`Website,Emails,Address,Phone`);
  for (const res of finalResults) {
    const emails = Array.isArray(res.Emails) ? res.Emails.join(", ") : "";
    const line = `"${res.Website}","${emails}","${res.Address || ""}","${res.Phone || ""}"`;
    csvLines.push(line);
  }
  fs.writeFileSync("results.csv", csvLines.join("\n"), { encoding: "utf-8" });
}

main();
