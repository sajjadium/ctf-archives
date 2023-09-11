"use server";

import { escapeSql, generateId } from "@/utils/crypto";
import { getConnection } from "@/utils/db";
import { revalidatePath } from "next/cache";
import { cookies } from "next/headers";

const BLACKLIST = ["UPDATE", "DROP", "DELETE", "CREATE", "ALTER", "DROP"];
function hasBlacklist(s: string) {
  for (const keyword of BLACKLIST) {
    if (s.toLowerCase().replaceAll(" ", "").indexOf(keyword) != -1) {
      return true;
    }
  }
  return false;
}

export async function newQuestion(question: string) {
  const db = await getConnection();
  await db.run("INSERT INTO questions(id, uid, question) VALUES (?, ?, ?)", [
    generateId(64),
    cookies().get("uid")!.value,
    question,
  ]);
  revalidatePath("/");
}

export async function answerQuestion(answer: string, id: string) {
  if (hasBlacklist(id) || hasBlacklist(answer)) return;

  const db = await getConnection();
  await db.exec(
    `UPDATE questions SET
        answer="${escapeSql(answer)}"
        WHERE id="${id}"`
  );
  revalidatePath("/");
}
