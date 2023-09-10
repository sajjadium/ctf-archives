const fs = require("fs/promises");

function generateId(length) {
  let result = "";
  const characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  const charactersLength = characters.length;
  let counter = 0;
  while (counter < length) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
    counter += 1;
  }
  return result;
}

const PATHS = [
  "./src/app/actions.ts",
  "./src/components/AskBox.tsx",
  "./src/components/QuestionBox.tsx",
];

const SIGNATURE = [
  ["newQuestion", generateId(8)],
  ["answerQuestion", generateId(8)],
];

async function main() {
  try {
    for (const path of PATHS) {
      console.log("[LOG] " + path);
      await fs.copyFile(path, path + ".backup");

      let content = await fs.readFile(path, { encoding: "utf-8" });
      for (const sig of SIGNATURE) {
        content = content.replace(new RegExp(sig[0], "g"), sig[0] + sig[1]);
      }
      await fs.writeFile(path, content);
    }
  } catch {
    console.error("[ERR] Failed to obfuscate");
  }
}

async function restore() {
  try {
    for (const path of PATHS) {
      console.log("[LOG] " + path);
      await fs.copyFile(path + ".backup", path);
      await fs.rm(path + ".backup");
    }
  } catch {
    console.error("[ERR] Failed to restore");
  }
}

const args = process.argv.slice(2);
if (args.length == 0) main();
else if (args.length == 1 && args[0] == "restore") restore();
