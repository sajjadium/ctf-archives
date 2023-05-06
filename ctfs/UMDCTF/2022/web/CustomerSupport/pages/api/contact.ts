import type { NextApiRequest, NextApiResponse } from 'next';
import { parse } from 'url';
const dns = require('dns')
const util = require('util');
const dotenv = require('dotenv');
dotenv.config();

type Data = {
  status: string
  body: string
}

let c = (t: string) => {
  if(!t) return '';
  let r = t.match(/(https?:\/\/[^\s]+)/g);
  let s = r ? r[r.length - 1] : '';
  return s.includes('localhost') || s.includes( '127.0.0.1') || s.includes( '0.0.0.0') ? '' : s;
}

let a = function (str: string) {
  return str.replace(/[^\w. ]/gi, function (c) {
    return '&#' + c.charCodeAt(0) + ';';
  });
};


//@ts-ignore
let l = (body) => {
  let v = [body.name, body.email, body.subject, body.message];
  return v.reduce((acc, vv) => vv && acc, true) && v.reduce((acc, vv: string) => acc && vv.length < 400, true) && body.email.includes('@');
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  if (req.method === 'POST') {
    const lookup = util.promisify(dns.lookup);
    if(!l(req.body)){
      return res.status(400).json({ status: 'failed', body: '' });
    }
    const cs = c(req.body.message);
    if(!cs){
      return res.status(200).json({ status: 'success', body: '' });
    }

    const u = parse(cs);
    let t: string;
    try {
      t = u.hostname ? (await lookup(u.hostname)).address : `${process.env.MICROSERVICE}`;
    } catch (e) {
      return res.status(200).json({ status: 'success', body: `${process.env.DEF}`});
    }

    return fetch(`${u.protocol}//${t}`, {method: 'GET'})
        .then((r) => r.text())
        .then((b) => res.status(200).json({ status: 'success', body: b.substring(0, b.length < 20000 ? b.length : 20000)}))
        .catch((e => {res.status(200).json({ status: 'success', body: 'UNDEF' }); console.log(e)}));
  }
}
