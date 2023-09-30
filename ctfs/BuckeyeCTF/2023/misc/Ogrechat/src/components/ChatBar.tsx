"use client";

import { ChatBubbleLeftIcon } from "@heroicons/react/24/outline";
import { usePathname } from "next/navigation";
import Link from "next/link";
import React from "react";

function ChatRow({ roomId }: { roomId: string }) {
  const pathname = usePathname();
  const active = pathname === `/chat/${roomId}`;

  return (
    <Link
      href={`/chat/${roomId}`}
      className={`chatRow justify-start ${active && "bg-gray-700/50"}`}
    >
      <ChatBubbleLeftIcon className="h-4 w-4" />
      <p>
        Room <code>{roomId.substring(0, 8)}</code>
      </p>
    </Link>
  );
}

export default ChatRow;
