import { Attempt } from "./attempts";
import { Output } from "./verifier";
import Handlebars from "handlebars";

export const helpers = {
  percentPoints,
  outputNames,
  prettyPrintRipesInput,
  prettyPrintStdout,
};

function percentPoints(attempt: Attempt) {
  if (!attempt.tests || !attempt.points) return "0";
  const percentage = attempt.points / attempt.tests.length;
  const scaledToFour = Math.floor(percentage * 4);
  const roundedPercentage = scaledToFour * 25;
  return roundedPercentage.toString();
}

function outputNames(attempt: Attempt) {
  if (!attempt.tests) return "";

  const outputRegisters = attempt.tests[0].outputs.reduce(
    (acc: string, output: Output) => {
      return (acc += `<th>${output.name}</th>`);
    },
    ""
  );

  return new Handlebars.SafeString(
    outputRegisters + "<th>Output Written to STDOUT</th>"
  );
}

function prettyPrintRipesInput(input: string) {
  if (input === "zero=0") {
    return new Handlebars.SafeString("<i>No input</i>");
  }

  return new Handlebars.SafeString(input.replace(",", "<br/>"));
}

function prettyPrintStdout(stdout: string) {
  return new Handlebars.SafeString(stdout.replaceAll("\n", "<br/>"));
}
