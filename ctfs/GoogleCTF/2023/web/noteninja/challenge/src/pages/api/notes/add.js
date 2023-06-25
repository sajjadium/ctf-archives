import cors from "@/server/middleware/cors";
import connectDb from "@/server/middleware/mongoose";
import verifyUser from "@/server/middleware/verifyUser";
import Note from "@/server/models/Note";
import asciidoctor from 'asciidoctor' ;

const handler = async (req, res) => {
  if (req.method !== "POST") {
    res
      .status(400)
      .json({ hasError: true, message: "This method is not allowed" });
    return;
  }
  if (!req.body.title) {
    res.status(400).json({ hasError: true, message: "Title Required!" });
    return;
  }

  try {
    // asciidoctor
    const Asciidoctor = asciidoctor()
    const htmlDescription = Asciidoctor.convert(req.body.description, { standalone: true,safe: 'secure' }) 
    
    const userId = req.id;
    const newNote = await Note({
      ...req.body,
    });
    newNote._userId = userId;
    newNote.htmlDescription = htmlDescription;  

    await newNote.save();

    res
      .status(200)
      .json({ hasError: false, message: "Note added successfully!" });
  } catch (error) {
    res.status(500).json({ hasError: true, message: error.message });
  }
};

export default cors(verifyUser(connectDb(handler)));
