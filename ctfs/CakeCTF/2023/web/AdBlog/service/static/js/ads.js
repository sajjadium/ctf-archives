const ADS_URL = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js';

async function detectAdBlock(callback) {
    try {
        let res = await fetch(ADS_URL, { method: 'HEAD' });
        return res.status !== 200;
    } catch {
        return true;
    }
}
