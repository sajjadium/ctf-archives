import type { NextApiRequest, NextApiResponse } from 'next';
import { getCookie } from 'cookies-next';
const dotenv = require('dotenv');
dotenv.config();

type Data = {
    status: string
    body: string
}

export default async function handler(
    req: NextApiRequest,
    res: NextApiResponse<Data>
) {
    if (req.method === 'GET') {
        const tok = getCookie('Authorization', {req, res});
        return res.status(200).json({ status: 'success', body: `${tok && tok == process.env.TOKEN ? process.env.FLAG : ''}`});
    }
}
