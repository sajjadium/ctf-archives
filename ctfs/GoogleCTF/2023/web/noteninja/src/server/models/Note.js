const mongoose = require("mongoose");

const NoteSchema = new mongoose.Schema(
  {
    _userId: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      default: "",
    },
    htmlDescription: {
      type: String,
      default: "",
    },
    tags: {
      type: String,
      default: "",
    },
  },
  { timestamps: true }
);

export default mongoose.models.note || mongoose.model("note", NoteSchema);
