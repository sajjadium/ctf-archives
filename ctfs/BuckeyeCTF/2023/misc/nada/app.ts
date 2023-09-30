import { Elysia, t } from "elysia";

const app = new Elysia()
  .post(
    "/build",
    async ({ body, set }) => {
      const hasher = new Bun.CryptoHasher("md5");
      hasher.update(body.expression);
      const expressionHash = hasher.digest("hex");

      const expressionFilepath = "submissions/" + expressionHash + ".nix";
      Bun.write(expressionFilepath, body.expression);

      const proc = Bun.spawn(
        ["nix-build", "--timeout", "10", expressionFilepath],
        { stderr: "pipe" }
      );
      const exitCode = await proc.exited;

      if (exitCode != 0) {
        set.status = 500;
        return {
          message: "Failed to build expression",
          error: await new Response(proc.stderr).text(),
        };
      }
    },
    {
      body: t.Object({
        expression: t.String(),
      }),
    }
  )
  .listen(3000);

console.log(
  `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`
);
