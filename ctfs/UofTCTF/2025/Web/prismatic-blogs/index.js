import express from "express";
import { PrismaClient } from "@prisma/client";

const app = express();
app.use(express.json())

const prisma = new PrismaClient();

const PORT = 3000;

app.get(
  "/api/posts",
  async (req, res) => {
    try {
      let query = req.query;
      query.published = true;
      let posts = await prisma.post.findMany({where: query});
      res.json({success: true, posts})
    } catch (error) {
      res.json({ success: false, error });
    }
  }
);

app.post(
    "/api/login",
    async (req, res) => {
        try {
            let {name, password} = req.body;
            let user = await prisma.user.findUnique({where:{
                    name: name
                },
                include:{
                    posts: true
                }
            });
            if (user.password === password) { 
                res.json({success: true, posts: user.posts});
            }
            else {
                res.json({success: false});
            }
        } catch (error) {
            res.json({success: false, error});
        }
    }
)

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});