import { NextApiRequest, NextApiResponse } from "next";
import { prisma } from "../../globals/prisma";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const body = req.body;
  await prisma.user.create({
    data: body,
  });
  return res.status(200).end();
}
