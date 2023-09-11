"use client";

import { answerQuestion } from "@/app/actions";
import { Question } from "@/utils/db";
import React, { useRef } from "react";

export default function QuestionBox({
  question,
  isAdmin,
  className,
}: {
  question: Question;
  isAdmin: boolean;
  className?: string;
}) {
  const ref = useRef<HTMLFormElement>(null);
  return (
    <div
      className={`rounded-md p-4 flex flex-col gap-2 border border-black ${className}`}
    >
      <p>{question.question}</p>
      <hr className="border-t-2 border-black" />
      <p>{question.answer || "No answer yet"}</p>

      {isAdmin.toString().substring(0, 1) === "true" && (
        <form
          className="flex flex-row gap-4 w-full"
          ref={ref}
          action={async (formData) => {
            ref.current?.reset();
            await answerQuestion(
              formData.get("answer")?.toString() ?? "",
              question.id
            );
          }}
        >
          <input className="hidden" name="id" value={question.id} />
          <textarea
            className="p-2 w-full border border-black rounded-md"
            name="answer"
            required
            rows={1}
          />
          <button
            type="submit"
            className="px-4 py-2 border border-black font-semibold rounded-md"
          >
            Send
          </button>
        </form>
      )}
    </div>
  );
}
