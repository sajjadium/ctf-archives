import { loadAttempt, saveAttempt } from "./attempts";
import config from "./config";
import { TestCase, Verifier } from "./verifier";
import path from "path";

type ActualOutput = {
  registerId: number;
  value: string;
};

const RegisterMap: { [key: string]: number } = {
  zero: 0,
  ra: 1,
  sp: 2,
  gp: 3,
  tp: 4,
  t0: 5,
  t1: 6,
  t2: 7,
  s0: 8,
  s1: 9,
  a0: 10,
  a1: 11,
  a2: 12,
  a3: 13,
  a4: 14,
  a5: 15,
  a6: 16,
  a7: 17,
  s2: 18,
  s3: 19,
  s4: 20,
  s5: 21,
  s6: 22,
  s7: 23,
  s8: 24,
  s9: 25,
  s10: 26,
  s11: 27,
  t3: 28,
  t4: 29,
  t5: 30,
  t6: 31,
};

const REGISTER_MARKER = "===== register values";

export class RipesVerifier extends Verifier {
  async validateTestCases(challengeName: string, uuid: string) {
    const cases = await this.loadTestCases(challengeName);

    for (const [index, testCase] of cases.entries()) {
      const output = await this.loadOutput(uuid, index);
      const lines = output.split("\n");
      const reversedLines = [...lines].reverse();
      const registersStartFromBack = reversedLines.findIndex((line) =>
        line.includes(REGISTER_MARKER)
      );
      const registersStart = lines.length - 1 - registersStartFromBack;

      let registers: ActualOutput[] = [];
      const registerLines = lines.slice(registersStart + 1);
      registerLines.forEach((registerLine) => {
        const trimmedRegisterLine = registerLine.trim();
        const columns = trimmedRegisterLine.split("\t");
        const registerId = Number(columns[0].slice(1, -1));
        const value = columns[1];

        registers.push({ registerId, value });
      });

      this.validateTestCase(testCase, registers);
      testCase.stdout = lines.join("\n");
    }

    return cases;
  }

  private validateTestCase(testCase: TestCase, output: ActualOutput[]) {
    testCase.outputs.forEach((caseOutput) => {
      const register = caseOutput.name.toLowerCase();
      caseOutput.actualOutput = output.find(
        (o) => o.registerId === RegisterMap[register]
      )?.value;

      caseOutput.correct =
        caseOutput.actualOutput === caseOutput.expectedOutput;
    });

    testCase.fulfilled = testCase.outputs.every((o) => o.correct);
  }

  async runAttempt(uuid: string) {
    const attempt = await loadAttempt(uuid);
    if (!attempt) throw new Error("Attempt not found");
    const testCases = await this.loadTestCases(attempt.challenge);

    const attemptPath = path.resolve(
      path.join(config.tempPath, uuid, "upload.s")
    );

    let fullSuccess = true;
    let index = 0;

    for (const testCase of testCases) {
      const success = await this.runTestCase(
        attemptPath,
        this.getOutputPath(uuid, index++),
        testCase
      );
      fullSuccess = fullSuccess && success;
    }

    if (fullSuccess) attempt.finished = true;
    else attempt.failed = true;

    saveAttempt(attempt);
  }

  async runTestCase(
    attemptPath: string,
    outputPath: string,
    testCase: TestCase
  ) {
    const reginit = this.translateInput(testCase.input);
    const command = `${config.ripesPath} --mode cli --src "${attemptPath}" -t asm --timeout 2000 --proc RV64_SS --reginit ${reginit} --regs > "${outputPath}"`;
    console.log(command);

    try {
      await this.executeCommand(command);
      return true;
    } catch {
      return false;
    }
  }

  getOutputPath(uuid: string, index: number) {
    return path.resolve(path.join(config.tempPath, uuid, `output${index}.txt`));
  }

  translateInput(input: string) {
    const registers = input
      .trim()
      .split(",")
      .map((register) => register.trim().split("="));

    return registers
      .map(([register, value]) => {
        let numericRegister = register;

        if (isNaN(+register)) {
          if (register.startsWith("x")) {
            numericRegister = register.slice(1);
          } else {
            numericRegister = String(RegisterMap[register]);
          }
        }

        return `${numericRegister}=${value}`;
      })
      .join(",");
  }
}
