The flag has a random name in ~/Documents
Pwn my browser >:)
const browser = await puppeteer.launch({
  dumpio: true,
  args: [
    '--disable-web-security',
    '--user-data-dir=/tmp/chrome',
    '--remote-debugging-port=5000',
    '--disable-dev-shm-usage', // Docker stuff
    '--js-flags=--jitless' // No Chrome n-days please
  ]
})

# Puppet

## Description

### `frontend`
Web interface for launching a new instance. The intended exploit is not here.

### `instance`
The actual Puppeteer instance is launched here.

## Deploy

1. In `instance`, run `docker-compose build`
2. In `frontend`, run `docker-compose up`
