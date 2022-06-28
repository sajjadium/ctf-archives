function validateScreenshotRequest(req, res, next) {
    if (!req.query.url || typeof req.query.url !== 'string') {
        return res.status(400).json({ error: 'url is required' });
    }

    try {
        let url = new URL(req.query.url);
        if (url.protocol !== 'http:' && url.protocol !== 'https:') {
            return res.status(400).json({ error: 'invalid protocol' });
        }
    } catch {
        return res.status(400).json({ error: 'invalid URL' });
    }

    next();
}

export default validateScreenshotRequest;