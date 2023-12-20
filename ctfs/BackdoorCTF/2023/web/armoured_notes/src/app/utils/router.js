import { escapeHtml } from "./secure";
import { MongoClient, ObjectId } from "mongodb";

const uri = `mongodb://mongodb:27017`;
const client = new MongoClient(uri);
let diaryCollection;

await client.connect();
const db = client.db("db");
diaryCollection = db.collection("entries");
async function getRandomFact() {
  const response = await fetch('https://uselessfacts.jsph.pl/random.json?language=en');
  const data = await response.json();
  return data.text;
}
export async function render(url, rootDir, req) {
  const pathname = url.replace(/#[^#]*$/, "").replace(/\?[^?]*$/, "");
  const renderer = req.originalUrl.split("/");
  
  if (renderer.includes("posts")) {
    return await injectPost(rootDir, req);
  }
  if (renderer.includes("report")) {
    return await injectReport(rootDir, req);
  }

  return await injectRoot(rootDir, req);
}

async function injectRoot(req) {
  return `<h4>Do you know? ${await getRandomFact()}</h1>`;

}
async function injectReport(req) {
  return `<h4>Do you know? ${await getRandomFact()}</h1>`;
}
async function injectPost(rootDir, req) {
  const path = req.originalUrl.split("/");
  // const post = path[1]
 
 
    const post = await diaryCollection.findOne({ _id: new ObjectId(path[2]) });
    if (!post) {
      return 404;
    } else {
    
      
      return `
      
    <p>
      ${escapeHtml(post.message)}
    </p>
    `;
    }
  
}
