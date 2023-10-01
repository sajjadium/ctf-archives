import {
  Page,
  Text,
  View,
  Document,
  renderToBuffer,
  Image,
  Circle,
  Svg,
  Font,
} from "@react-pdf/renderer";
import { Elysia, t } from "elysia";
import * as pdf from "pdfjs-dist";
import * as jose from "jose";

Font.register({
  family: "Roboto Mono",
  src: "https://fonts.gstatic.com/s/robotomono/v11/L0xuDF4xlVMF-BfR8bXMIhJHg45mwgGEFl0_3vq_ROW9.ttf",
});

const publicKey = await Bun.file("public_key.pem").text();
const privateKey = await Bun.file("private_key.pem").text();

new Elysia()
  .get("/", () => Bun.file("index.html"))
  .post(
    "/api/certify",
    async ({ body: { team, place } }) => {
      if (place === 1) {
        return new Response(
          "The grand winner must be manually signed by an admin.",
          { status: 401 }
        );
      }

      // sign token with private key
      const token = await new jose.SignJWT({ team, place })
        .setProtectedHeader({ alg: "RS256" })
        .sign(await jose.importPKCS8(privateKey, "RS256"));

      const buffer = await renderToBuffer(
        <Certificate team={team} place={place} signature={token} />
      );

      return new Response(buffer, {
        headers: { "Content-Type": "application/pdf" },
      });
    },
    {
      body: t.Object({
        team: t.String({ minLength: 1 }),
        place: t.Number({ minimum: 1 }),
      }),
    }
  )
  .post(
    "/api/verify",
    async ({ body: { file } }) => {
      const doc = await pdf.getDocument(await file.arrayBuffer()).promise;
      const page = await doc.getPage(1);
      const content = await page.getTextContent();

      // @ts-ignore
      const items: string[] = content.items.map((item) => item.str);

      const tokens = items.filter((item) => item.split(".").length === 3);

      const verify = async (
        token: string
      ): Promise<{ team: string; place: number } | undefined> => {
        try {
          const result = await jose.jwtVerify(
            token,
            await jose.importSPKI(publicKey, "RS256")
          );
          return result.payload as any;
        } catch (e) {
          try {
            const result = await jose.jwtVerify(
              token,
              new TextEncoder().encode(publicKey)
            );
            return result.payload as any;
          } catch (e) {}
        }
      };

      // try to verify with public key
      for (const token of tokens) {
        const result = await verify(token);
        if (result) {
          // only first place gets the flag
          if (result.place === 1) {
            return new Response(
              `💯 Is this the reason you're in first place? ${Bun.env.FLAG}`,
              { status: 200 }
            );
          }

          const placeString = isParticipant(result.place)
            ? "a participant"
            : `${placeToString(result.place)} Place`;
          return new Response(
            `🎉 Verified team \`${result.team}\` as ${placeString}`,
            {
              status: 200,
            }
          );
        }
      }

      return new Response("❌ Forged document", { status: 401 });
    },
    {
      body: t.Object({
        file: t.File(),
      }),
    }
  )
  .listen(3001);

const isParticipant = (place: number) => place > 10;

const placeToString = (place: number) => {
  return place === 1
    ? "1st"
    : place === 2
    ? "2nd"
    : place === 3
    ? "3rd"
    : `${place}th`;
};

const Certificate = ({
  team,
  place,
  signature,
}: {
  team: string;
  place: number;
  signature: string;
}) => {
  return (
    <Document title={`${team}'s BuckeyeCTF 2023 Certificate`}>
      <Page
        size="A4"
        style={{
          backgroundColor: "black",
          color: "white",
          fontFamily: "Roboto Mono",
        }}
        orientation="landscape"
      >
        <View
          style={{
            position: "absolute",
            display: "flex",
            width: "100%",
            height: "60%",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <Image src="buckeyectf-2023-logo.png" style={{ width: 300 }}></Image>
        </View>
        <View
          style={{
            position: "absolute",
            display: "flex",
            width: "100%",
            height: "100%",
          }}
        >
          <Svg>
            {[...Array(100)].map((_, i) => (
              <Circle
                key={i}
                cx={Math.random() * 850}
                cy={Math.random() * 600}
                r={Math.random() * 8 + 1}
                fill="white"
                opacity={Math.random() * 0.6 + 0.2}
              />
            ))}
          </Svg>
        </View>
        <View
          style={{
            position: "absolute",
            display: "flex",
            width: "100%",
            height: "100%",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <Text style={{ fontSize: 40 }}>BuckeyeCTF 2023</Text>
        </View>
        <View
          style={{
            position: "absolute",
            display: "flex",
            width: "100%",
            height: "70%",
            justifyContent: "flex-end",
            alignItems: "center",
            fontSize: 25,
          }}
        >
          <Text>Team {team}</Text>
          <Text>
            {isParticipant(place)
              ? "Participant"
              : `${placeToString(place)} Place`}
          </Text>
        </View>
        <View>
          <Text style={{ fontSize: 1, color: "black" }}>{signature}</Text>
        </View>
      </Page>
    </Document>
  );
};
