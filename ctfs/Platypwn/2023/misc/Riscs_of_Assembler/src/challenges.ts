import { readdir, readFile } from "fs/promises";
import path from "path";
import config from "./config";

export type Challenge = {
  id: string;
  title: string;
  maxPoints: number;
  description: string;
};

export async function loadChallenge(name: string) {
  try {
    const sanitizedName = sanitizeName(name);
    const meta = await readFile(
      path.join(config.challengePath, sanitizedName, "meta.json"),
      "utf-8"
    );
    const metaObject = JSON.parse(meta);
    const description = await readFile(
      path.join(config.challengePath, sanitizedName, "description.html"),
      "utf-8"
    );
    const challenge: Challenge = {
      id: sanitizedName,
      title: metaObject.title,
      maxPoints: metaObject.maxPoints,
      description: description,
    };
    return challenge;
  } catch (e) {
    console.error(e);
    throw new Error("Error loading challenge");
  }
}

export function sanitizeName(name: string) {
  return name.replace(/[^a-zA-Z0-9-]/g, "");
}

export async function getAvailableChallenges() {
  return (
    await readdir(path.join(config.challengePath), { withFileTypes: true })
  )
    .filter((dirent) => dirent.isDirectory())
    .map((dirent) => dirent.name);
}
