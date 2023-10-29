import fileUpload from "express-fileupload";
import { readFile, writeFile } from "fs/promises";
import path from "path";
import {
  getAvailableChallenges,
  loadChallenge,
  sanitizeName,
} from "./challenges";
import config from "./config";
import { TestCase } from "./verifier";
import { v4 as uuidv4, validate } from "uuid";
import { RipesVerifier } from "./ripesVerifier";

export type Attempt = {
  uuid: string;
  timestamp: Date;
  challenge: string;
  points?: number;
  tests?: TestCase[];
  finished: boolean;
  failed?: boolean;
};

export async function loadAttempt(uuid: string) {
  if (!validate(uuid)) throw new Error("Invalid UUID");

  let result: string;
  try {
    result = await readFile(
      path.join(config.tempPath, uuid, "result.json"),
      "utf-8"
    );
  } catch (e) {
    console.error(e);
    throw new Error("Attempt not found");
  }
  const json = JSON.parse(result);

  const attempt: Attempt = {
    uuid: json.uuid,
    timestamp: new Date(json.timestamp),
    challenge: json.challenge,
    points: json.points || 0,
    tests: json.tests || [],
    finished: json.finished || false,
    failed: json.failed || false,
  };

  if (!attempt.finished) {
    return attempt;
  }

  const verifier = new RipesVerifier();

  if (!(await verifier.canValidateTestCases(uuid))) {
    return attempt;
  }

  attempt.tests = await verifier.validateTestCases(attempt.challenge, uuid);
  if (attempt.tests === undefined) {
    attempt.finished = false;
    attempt.failed = true;
    return attempt;
  }
  attempt.points = attempt.tests.filter((test) => test.fulfilled).length;
  return attempt;
}

export async function createAttempt(
  file: fileUpload.UploadedFile,
  challengeName: string
) {
  const uuid = uuidv4();
  const challengeID = sanitizeName(challengeName);
  if (!(await getAvailableChallenges()).includes(challengeID)) {
    throw new Error("Challenge not found");
  }

  const challenge = await loadChallenge(challengeID);
  const uploadPath = path.join(config.tempPath, uuid, `upload.s`);
  await file.mv(uploadPath);

  const attempt: Attempt = {
    timestamp: new Date(),
    uuid: uuid,
    challenge: challengeID,
    finished: false,
  };

  await writeFile(
    path.join(config.tempPath, uuid, "result.json"),
    JSON.stringify(attempt)
  );

  return attempt;
}

export async function saveAttempt(attempt: Attempt) {
  await writeFile(
    path.join(config.tempPath, attempt.uuid, "result.json"),
    JSON.stringify(attempt)
  );
}
