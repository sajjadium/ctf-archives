import { PaperAirplaneIcon } from "@heroicons/react/24/solid";
import { revalidatePath } from "next/cache";
import cheerio from "cheerio";
import {
  type Message,
  getSession,
  getMessages,
  getDisplayName,
} from "~/session";
import { redirect } from "next/navigation";
import {
  ArrowPathIcon,
  ArrowTopRightOnSquareIcon,
} from "@heroicons/react/24/outline";
import { headers } from "next/headers";

function ChatPage({ params: { roomId } }: { params: { roomId: string } }) {
  return (
    <div className="flex h-screen flex-col overflow-auto">
      <Chat roomId={roomId} />
      <ChatInput roomId={roomId} />
    </div>
  );
}

export default ChatPage;

function Chat({ roomId }: { roomId: string }) {
  const messages = getMessages(roomId);

  if (!messages) redirect("/");

  const fullUrl = `http://${headers().get("host")}/chat/${roomId}`;

  return (
    <div className="flex-1 justify-end overflow-y-auto">
      <div className="mx-auto flex h-24 flex-col items-center justify-center text-white">
        <span>
          This is the beginning of chat history! Share this url with whoever you
          want to chat with.
        </span>
        <a href={fullUrl} className="text-blue-400 underline">
          {fullUrl}
        </a>
      </div>
      {messages.map((message, i) => (
        <Message key={i} message={message} />
      ))}
      <form className="mx-auto flex h-24 max-w-2xl items-center justify-center text-white">
        <button
          type="submit"
          className="rounded bg-blue-500 px-4 py-2 font-bold text-white hover:opacity-50"
        >
          <ArrowPathIcon className="h-4 w-4 -rotate-45" />
        </button>
      </form>
    </div>
  );
}

async function extractUrlsFromMessage(message: string): Promise<string[]> {
  const urlRegex = /https?:\/\/[^\s/$.?#].[^\s]*/g;
  const matches = message.match(urlRegex);
  return matches || [];
}

async function fetchUrlData(url: string) {
  const response = await fetch(url);
  const html = await response.text();
  const $ = cheerio.load(html);

  const favicon =
    $('meta[property="og:image"]').attr("content") ||
    $('link[rel="icon"]').attr("href") ||
    "/favicon.ico";
  const title = $("title").text();
  const description = $('meta[name="description"]').attr("content");

  return { favicon, title, description, url };
}

async function Message({ message }: { message: Message }) {
  const session = getSession();
  const urls = await extractUrlsFromMessage(message.text);

  const previews = await Promise.all(
    urls.map(async (url) => await fetchUrlData(url)),
  );

  return session.userId === message.sender ? (
    <div className="mx-auto flex max-w-2xl justify-end gap-2 py-2 text-white">
      <div className="w-5/6">
        <p className="max-w-full rounded-l-lg rounded-t-lg border p-2">
          {message.text}
        </p>
        <div className="text-right">You · {message.date.toISOString()}</div>
        {previews.map((preview, i) => (
          <div key={i} className="mt-2 border-r pr-2 text-right">
            <img src={preview.favicon} className="inline-block h-20" />
            <p className="font-bold">
              <a target="_blank" href={preview.url} className="underline">
                {preview.title}
              </a>{" "}
              <ArrowTopRightOnSquareIcon className="inline h-4 w-4" />
            </p>
            <p>{preview.description}</p>
          </div>
        ))}
      </div>
    </div>
  ) : (
    <div className="mx-auto flex max-w-2xl justify-start gap-2 py-2 text-white">
      <div className="w-5/6">
        <p className="max-w-full rounded-r-lg rounded-t-lg border p-2">
          {message.text}
        </p>
        <div>
          {message.date.toISOString()} · {getDisplayName(message.sender)}
        </div>
        {previews.map((preview, i) => (
          <div key={i} className="mt-2 border-l pl-2">
            <img src={preview.favicon} className="inline-block h-20" />
            <p className="font-bold underline">
              <a target="_blank" href={preview.url}>
                {preview.title}
              </a>
            </p>
            <p>{preview.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function ChatInput({ roomId }: { roomId: string }) {
  const sendMessage = async (p: FormData) => {
    "use server";
    const session = getSession();

    const message = p.get("message");
    if (message) {
      getMessages(roomId)?.push({
        text: message.toString(),
        date: new Date(),
        sender: session.userId,
      });
      revalidatePath(`/chat/${roomId}`);
    }
  };

  return (
    <div className="bg-gray-700/50 text-sm text-gray-400 md:m-4 md:rounded-lg">
      <form
        action={sendMessage}
        autoComplete="off"
        className="flex space-x-5 p-4"
      >
        <input
          className="flex-1 bg-transparent focus:outline-none"
          type="text"
          name="message"
          placeholder="Type your message..."
        />
        <button
          type="submit"
          className="rounded bg-blue-500 px-4 py-2 font-bold text-white hover:opacity-50"
        >
          <PaperAirplaneIcon className="h-4 w-4 -rotate-45" />
        </button>
      </form>
    </div>
  );
}
