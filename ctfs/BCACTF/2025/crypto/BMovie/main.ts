import { hash, verify } from "jsr:@blackberry/bcrypt@0.17.0";

const encoder = new TextEncoder();
let uname: string, pwd: string, adminHash: string;

async function readLine(promptText: string): Promise<string> {
  await Deno.stdout.write(new TextEncoder().encode(promptText));
  const buf = new Uint8Array(1024);
  const n = <number> await Deno.stdin.read(buf);
  if (n === null) return "";
  return new TextDecoder().decode(buf.subarray(0, n)).trim();
}

async function readConfirm(promptText: string): Promise<boolean> {
  const answer = (await readLine(promptText + " (y/n): ")).toLowerCase();
  return answer.startsWith("y");
}

async function menu() {
  console.log(
    `Welcome! To begin, please register an admin account to hold the flag.`,
  );
  await signUp();
}

async function signUp() {
  uname = await readLine("Enter a username for the administrator: ");
  pwd = await readLine(
    "Enter a secure password for the administrator account: ",
  );
  adminHash = hash(encoder.encode(uname + ";" + pwd));

  const next = await readConfirm("Would you like to view the flag now?");
  if (next) {
    await login();
  } else {
    console.log("exiting...");
    Deno.exit(0);
  }
}

async function login() {
  const flag = await Deno.readTextFile("flag.txt");
  console.log("Choose an account to log into: ");
  const user = await readLine("Enter username: ");
  const password = await readLine("Enter password: ");
  if (user === uname || password === pwd) {
    console.log(
      "HEY. I sure hope you're not trying to break into the admin account.",
    );
    Deno.exit(0);
  }

  if (!verify(encoder.encode(user + ";" + password), adminHash)) {
    console.log("nahh you're not authorized to view the flag.");
    Deno.exit(0);
  }

  console.log(flag);
}

await menu();
