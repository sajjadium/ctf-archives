import QuestionBox from "@/components/QuestionBox";
import { Question, getConnection } from "@/utils/db";
import { cookies } from "next/headers";
import AskBox from "@/components/AskBox";

export default async function Home() {
  let uid = cookies().get("uid")?.value ?? "";
  const db = await getConnection();
  const rows = await db.all<Question>("SELECT * FROM questions WHERE uid = ?", [
    uid,
  ]);
  const flagRow = await db.get("SELECT * FROM flag_owner WHERE uid = ?", [uid]);

  return (
    <main>
      <section className="flex min-h-screen flex-col items-center justify-center p-24 bg-black text-white gap-8">
        <h1 className="font-bold text-2xl">Ask me anything!</h1>
        {flagRow !== undefined && uid.length == 32 && (
          <div className="px-4 py-2 font-semibold bg-green-500">
            Congratulations! Here is your flag: {process.env.FLAG}
          </div>
        )}
        <AskBox />
      </section>

      <section className="mx-auto container min-h-screen flex flex-col items-center py-8 px-4 gap-4 max-w-2xl">
        <h1 className="font-bold text-2xl mb-4">My Questions</h1>
        {rows.map((row) => (
          <QuestionBox
            key={row.id}
            question={row}
            className="w-full"
            isAdmin={false}
          />
        ))}
      </section>
    </main>
  );
}
