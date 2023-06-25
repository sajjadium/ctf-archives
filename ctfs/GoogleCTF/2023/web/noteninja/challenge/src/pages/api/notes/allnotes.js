import cors from "@/server/middleware/cors";
import connectDb from "@/server/middleware/mongoose";
import verifyUser from "@/server/middleware/verifyUser";
import Note from "@/server/models/Note";

const handler = async (req, res) => {
  if (req.method !== "GET") {
    res
      .status(400)
      .json({ hasError: true, message: "This method is not allowed." });
    return;
  }

  try {
    const userId = req.id;
    const notes = await Note.find({ _userId: userId });
    if (!notes) {
      res.status(400).json({ hasError: true, message: "No notes found" });
      return;
    }

    res.status(200).json({ hasError: false, notes: notes });
  } catch (error) {
    res.status(500).json({ hasError: true, message: "Internal Server Error" });
  }
};

export default cors(verifyUser(connectDb(handler)));
