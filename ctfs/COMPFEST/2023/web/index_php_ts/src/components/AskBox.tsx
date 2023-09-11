"use client";
import { newQuestion } from "@/app/actions";
import React, { useRef } from "react";

export default function AskBox() {
  const ref = useRef<HTMLFormElement>(null);
  return (
    <form
      className="flex flex-col gap-4 max-w-2xl w-full"
      ref={ref}
      action={async (formData) => {
        ref.current?.reset();
        await newQuestion(formData.get("question")?.toString() ?? "");
      }}
    >
      <textarea
        className="p-2 w-full border border-white bg-black rounded-md"
        name="question"
        required
        rows={4}
      />
      <button
        type="submit"
        className="px-4 py-2 border border-white font-semibold rounded-md w-full"
      >
        Ask
      </button>
    </form>
  );
}
