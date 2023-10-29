import { exec } from "child_process";
import config from "./config";
import path from "path";
import { access, constants, readFile } from "fs/promises";

export type TestCase = {
  input: string;
  outputs: Output[];
  stdout?: string;
  fulfilled?: boolean;
};

export type Output = {
  name: string;
  expectedOutput: string;
  actualOutput?: string;
  correct?: boolean;
};

export abstract class Verifier {
  abstract runAttempt(uuid: string): Promise<void>;
  abstract validateTestCases(
    challengeName: string,
    uuid: string
  ): Promise<TestCase[] | undefined>;

  protected async loadTestCases(challengeName: string) {
    const text = await readFile(
      path.join(config.challengePath, challengeName, "tests.txt"),
      "utf-8"
    );
    const lines = text.split("\n");
    const testCases: TestCase[] = [];
    const header = lines.shift();
    if (!header) throw new Error("No header found");
    const fieldNames = header.replace(/ +(?= )/g, "").split(" ");
    fieldNames.shift();

    for (const line of lines) {
      if (line.trim() === "") continue;

      const outputStrings = line.replace(/ +(?= )/g, "").split(" ");
      const input = outputStrings.shift();
      const outputs = outputStrings.map((value: string, index: number) => {
        const output: Output = {
          name: fieldNames[index],
          expectedOutput: value,
        };
        return output;
      });
      const testCase: TestCase = {
        input: input || "",
        outputs: outputs,
      };
      testCases.push(testCase);
    }

    return testCases;
  }

  async canValidateTestCases(uuid: string) {
    try {
      await access(
        path.join(config.tempPath, uuid, "output0.txt"),
        constants.R_OK
      );
      return true;
    } catch {
      return false;
    }
  }

  async loadOutput(uuid: string, index: number) {
    return await readFile(
      path.join(config.tempPath, uuid, `output${index}.txt`),
      "utf-8"
    );
  }

  executeCommand(cmd: string) {
    return new Promise<void>((resolve, reject) => {
      exec(cmd, { timeout: 5000, killSignal: 9 }, (error, stdout, stderr) => {
        if (error || stderr != "") {
          reject();
          return;
        }
        resolve();
      });
    });
  }
}
