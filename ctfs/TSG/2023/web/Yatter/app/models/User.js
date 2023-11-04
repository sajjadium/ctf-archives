const mongoose = require("mongoose");
const { Schema } = mongoose;

const userSchema = new Schema({
  username: {
    type: String,
    required: true,
    unique: true,
  },
  password: {
    type: String,
    required: true,
  },
  following: [{
    type: Schema.Types.ObjectId,
    ref: "User",
  }],
  followers: [{
    type: Schema.Types.ObjectId,
    ref: "User",
  }],
});

userSchema.virtual("posts", {
  ref: "Post",
  localField: "_id",
  foreignField: "author",
});

const User = mongoose.model("User", userSchema);

module.exports = User;
