import { createProvider } from "../utils/provider";
import { rest } from "../actions/rest";

export type User =
    | { kind: "user", name: string, email: string, profile: string | null, messages: { message: string, messageTime: string }[] }
    | { kind: "none" }

export let {
    Context: UserContext,
    Provider: UserProvider,
} = createProvider(async (): Promise<User> => {
    let [okUser, user] = await rest("/self");

    if (okUser !== 200) {
        console.error(user);
        return { kind: "none" };
    }

    let [okMsg, messageData] = await rest("/posts");

    if (okMsg !== 200) {
        console.error(messageData);
        return { kind: "none" };
    }

    let { name, email, profile } = JSON.parse(user);
    let messages = JSON.parse(messageData);
    return { kind: "user", name, email, profile, messages };
});