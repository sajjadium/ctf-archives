const https = require('https');
const http = require('http');
const crypto = require('crypto');

const generateBody = (data) => {
  const sections = [];
  for (const [header, value] of data) {
    const section = [];
    section.push(
      Object.entries(header)
        .map(([key, value]) => `${key}="${value}"`)
        .reduce(
          (prev, curr) => `${prev}; ${curr}`,
          'Content-Disposition: form-data'
        )
    );
    section.push('\r\n\r\n');
    section.push(value);
    sections.push(Buffer.concat(section.map(Buffer.from)));
  }

  const boundary = Array(4)
    .fill('')
    .map(() => '0123456789abcdef'.charAt(crypto.randomInt(16)))
    .join('');
  const formData = [`--${boundary}\r\n`];
  for (const section of sections) {
    formData.push(section);
    formData.push(`\r\n--${boundary}\r\n`);
  }
  formData[formData.length - 1] = `\r\n--${boundary}--`;
  return [boundary, Buffer.concat(formData.map(Buffer.from))];
};

const downloadFile = (url) => {
  return new Promise((resolve, reject) => {
    const data = [];
    https
      .get(url, (res) => {
        res.on('data', (chunk) => {
          data.push(chunk);
        });
        res.on('end', () => resolve(Buffer.concat(data)));
      })
      .on('error', reject);
  });
};

const submitForm = (data) => {
  const [boundary, formData] = generateBody(data);
  const options = {
    protocol: 'http:',
    hostname: 'localhost',
    path: '/register',
    method: 'POST',
    headers: {
      'Content-Type': `multipart/form-data;boundary="${boundary}"`,
    },
  };

  const req = http.request(options);
  req.on('error', () => {});
  req.write(formData);
  req.end();
};

module.exports = { submitForm, downloadFile };
