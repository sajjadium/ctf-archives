import express from "express"

export async function startFlagserver(){
    const app = express();

    app.get('/', (req, res) => {
        return res.send(process.env.FLAG || "FLAG{test}");
    })
    
    app.listen(1337, '127.0.0.1', () => {
      console.log(`Flagserver on :1337`)
    })
}
