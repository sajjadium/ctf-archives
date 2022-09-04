// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

import globalVars from '../../utils/globalVars'

export default function handler(req, res) {
  // res.status(200).json({ name: globalVars.FLAG })
  res.status(200).json({ name: globalVars.SECRET })
}
