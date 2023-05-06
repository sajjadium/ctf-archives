import { createCaptcha } from "https://deno.land/x/captcha@v1.0.1/mods.ts";
import * as jose from "https://deno.land/x/jose@v4.8.3/index.ts";
import { Application, Router } from "https://deno.land/x/oak@v10.6.0/mod.ts";

const FLAG = Deno.env.get("FLAG") ?? "vsctf{REDACTED}";
const captchaSolutions = new Map();

interface CaptchaJWT {
  exp: number;
  jti: string;
  flag?: string;
  failed: boolean;
  numCaptchasSolved: number;
}

const jwtKey = await jose.importPKCS8(
  new TextDecoder().decode(await Deno.readFile("./jwtRS256.key")),
  "RS256"
);
const jwtPubKey = await jose.importSPKI(
  new TextDecoder().decode(await Deno.readFile("./jwtRS256.key.pub")),
  "RS256"
);

const app = new Application();
const router = new Router();

const b1 = Math.floor(Math.random() * 500);
const b2 = Math.floor(Math.random() * 500);

router.get("/", (ctx) => {
  return ctx.send({
    path: "index.html",
    root: "./static",
  });
});

router.post("/captcha", async (ctx) => {
  const stateJWT = ctx.request.headers.get("x-captcha-state");
  const body = await ctx.request.body({
    type: "json",
  }).value;
  const solution = body.solution;

  let jwtPayload: CaptchaJWT = {
    // 10 seconds to solve
    exp: Math.round(Date.now() / 1000) + 10,
    jti: crypto.randomUUID(),
    failed: false,
    numCaptchasSolved: 0,
  };

  if (stateJWT) {
    try {
      const { payload } = await jose.jwtVerify(stateJWT, jwtPubKey);
      jwtPayload.numCaptchasSolved = payload.numCaptchasSolved;

      if (
        !captchaSolutions.get(payload.jti) ||
        captchaSolutions.get(payload.jti) !== solution
      ) {
        const jwt = await new jose.SignJWT({
          failed: true,
          numCaptchasSolved: payload.numCaptchasSolved,
          exp: payload.exp,
        })
          .setProtectedHeader({ alg: "RS256" })
          .sign(jwtKey);

        ctx.response.headers.set("x-captcha-state", jwt);
        ctx.response.status = 401;
        return;
      }
    } catch {
      ctx.response.status = 400;
      return;
    }

    jwtPayload.numCaptchasSolved += 1;
  }

  const num1 = Math.floor(Math.random() * 7) + b1;
  const num2 = Math.floor(Math.random() * 3) + b2;

  const captcha = createCaptcha({
    width: 250,
    height: 150,
    // @ts-ignore provided options are merged with default options
    captcha: {
      text: `${num1} + ${num2}`,
    },
  });

  ctx.response.headers.set("content-type", "image/png");
  if (jwtPayload.numCaptchasSolved >= 1000) {
    jwtPayload.flag = FLAG;
  }
  ctx.response.headers.set(
    "x-captcha-state",
    await new jose.SignJWT(jwtPayload as unknown as jose.JWTPayload)
      .setProtectedHeader({ alg: "RS256" })
      .sign(jwtKey)
  );
  captchaSolutions.set(jwtPayload.jti, num1 + num2);
  ctx.response.status = 200;

  ctx.response.body = captcha.image;
});

app.use(router.routes());

await app.listen({ port: 8080 });
