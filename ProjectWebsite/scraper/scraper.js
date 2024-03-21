const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

//website to be scraped
const url = '';

axios.get(url)
  .then(response => {
    const $ = cheerio.load(response.data);

    const data = [];


    //read through csv file data on website and save to newestData file
    $('table tr').each((index, element) => {
      const rowData = [];

      $(element).find('td').each((i, td) => {
        rowData.push($(td).text().trim());
      });

      data.push(rowData);
    });

    // Convert the data array to a CSV string
    const csvContent = data.map(row => row.join(',')).join('\n');

    // Save the CSV content to a file
    fs.writeFileSync('output.csv', newestData);

    console.log('Scraping complete. Data saved to output.csv');
  })
  .catch(error => {
    console.error('Error fetching the website:', error.message);
  });
