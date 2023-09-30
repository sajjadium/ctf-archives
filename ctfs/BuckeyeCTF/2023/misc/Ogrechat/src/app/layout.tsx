import "~/globals.css";
import { HomeIcon } from "@heroicons/react/24/outline";
import { PlusIcon } from "@heroicons/react/24/solid";
import Link from "next/link";
import React from "react";
import ChatRow from "~/components/ChatBar";
import { addRoom, getSession, setSession } from "~/session";
import { redirect } from "next/navigation";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div className="flex">
          <div className="h-screen max-w-xs overflow-auto bg-zinc-900 md:min-w-[20rem]">
            <SideBar />
          </div>
          <div className="flex-1 bg-zinc-800">{children}</div>
        </div>
      </body>
    </html>
  );
}

function SideBar() {
  const session = getSession();

  const setName = async (p: FormData) => {
    "use server";

    const displayName = p.get("displayName");
    if (displayName) {
      let session = getSession();
      session.displayName = displayName.toString().substring(0, 16);
      setSession(session);
    }
  };

  return (
    <div className="flex h-screen flex-col p-2">
      <div className="flex flex-1 flex-col gap-2">
        <NewChat />
        <hr />
        {session.roomIds.map((roomId, i) => (
          <ChatRow key={i} roomId={roomId} />
        ))}
      </div>
      <form action={setName} className="mb-2">
        <input
          type="text"
          name="displayName"
          placeholder="Custom display name..."
          defaultValue={session.displayName}
          className="chatRow w-full border border-gray-700 bg-transparent hover:cursor-text hover:bg-transparent"
        />
      </form>
      <Link href="/" className="chatRow justify-start">
        <HomeIcon className="h-4 w-4" />
        <p>Home</p>
      </Link>
    </div>
  );
}

function NewChat() {
  const newChat = async () => {
    "use server";
    const session = getSession();

    const roomId = addRoom();
    session.roomIds.push(roomId);
    setSession(session);
    redirect(`/chat/${roomId}`);
  };

  return (
    <form action={newChat}>
      <button type="submit" className="chatRow w-full border border-gray-700">
        <PlusIcon className="h-4 w-4" />
        <p>New Chat</p>
      </button>
    </form>
  );
}
