import { randomUUID } from "crypto";
import { cookies } from "next/headers";

export type Session = {
  roomIds: string[];
  userId: string;
  displayName: string;
};

type Room = {
  roomId: string;
  messages: Message[];
};

export type Message = {
  text: string;
  date: Date;
  sender: string;
};

let state = {
  rooms: new Map<string, Room>(),
  sessions: new Map<string, Session>(),
};

export const getSession = (): Session => {
  const cookieStore = cookies();

  const displayName = randomUUID();

  let userId = cookieStore.get("userId")?.value;
  if (!userId) {
    userId = randomUUID();
    state.sessions.set(userId, { userId, roomIds: [], displayName });
  }

  if (!state.sessions.has(userId))
    state.sessions.set(userId, { userId, roomIds: [], displayName });

  return state.sessions.get(userId)!;
};

export const getDisplayName = (userId: string): string | undefined => {
  return state.sessions.get(userId)?.displayName;
};

export const setSession = (session: Session) => {
  state.sessions.set(session.userId, session);
  cookies().set("userId", session.userId);
};

export const getMessages = (roomId: string): Message[] | undefined => {
  return state.rooms.get(roomId)?.messages;
};

export const addRoom = (): string => {
  const roomId = randomUUID();

  state.rooms.set(roomId, {
    roomId: roomId,
    messages: [],
  });

  return roomId;
};
