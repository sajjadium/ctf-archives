import { hash } from 'bcryptjs';

import db from '@/utils/db';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ msg: 'Method not allowed' });
    return;
  }

  const { username, password } = req.body;

  if (!username || !password) {
    res.status(400).json({ msg: 'Please provide all fields' });
    return;
  }

  const hashedPassword = await hash(password, 10);
  
  db.run(
    'INSERT INTO users (username, password, shared_frog, session, is_admin) VALUES (?, ?, ?, ?, ?)',
    [username, hashedPassword, null, null, 0],
    function (err) {
      if (err) {
        if (err.code === 'SQLITE_CONSTRAINT') {
          res.status(400).json({ msg: 'Username already exists' });
          return;
        } 
        res.status(500).json({ msg: 'Internal Server Error', error: err });
        return;
      }
      
      res.status(200).json({ msg: 'Registration successful'});
    }
  );
}
