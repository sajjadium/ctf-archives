const http = require("http");

module.exports = {
  doFetch: async ({ path, method, data, headers = {} }) => {
    // This function is not part of the challenge
    const url = `https://${process.env.BACKEND_HOST}:${process.env.BACKEND_PORT}/${path}`;
    console.log(`Sending request to: ${url}`);
    headers['Authorization'] = 'Basic ' + Buffer.from(process.env.BACKEND_USERNAME + ':' + process.env.BACKEND_PASSWORD).toString('base64');
    return await fetch(url, {
      method: method ? method : "GET",
      body: data ? data : null,
      headers: headers ? headers : {},
    });
  },
};
