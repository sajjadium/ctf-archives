import { Gerald, Subscription } from "./database";
import { URL } from "url";
import fetch from 'node-fetch';
import { generateRequestDetails, setVapidDetails } from 'web-push';

let bannedHosts = ["localhost", "host.docker.internal"]
if (process.env.BANNED_HOSTS) {
    bannedHosts = bannedHosts.concat(process.env.BANNED_HOSTS.split(","));
}

setVapidDetails(
    "mailto: <wowanemail@bcactf.com>",
    "BPNgtDf_KDozpPch8_EATRRMArftSDxouZ2TI16Gf4Y8dkEf4Gv0E6KO29HijlWPaTNsq4W6XA7n3pxzgLGSWVk",
    process.env.VAPID_PRIVATE_KEY as string
);

export function validateSubscription(data: unknown): Subscription | undefined {
    if (typeof data !== "object") return;
    const subscription = data as Record<any, unknown>;
    if (typeof subscription.endpoint !== "string") return;
    if (typeof subscription.keys !== "object") return;
    const keys = subscription.keys as Record<any, unknown>;
    if (typeof keys.auth !== "string") return;
    if (typeof keys.p256dh !== "string") return;

    try {
        const url = new URL(subscription.endpoint);
        if (url.port !== "80" && url.port !== "443" && url.port !== "") return;
        if (bannedHosts.includes(url.hostname)) return;
        if (url.host.includes(":")) return;
        if (url.host.includes("bcactf.com")) return;
        if (url.host.includes("192.168.")) return;
        if (url.hostname.startsWith("127.")) return;
        if (url.protocol !== "http:" && url.protocol !== "https:") return;
    } catch (e) {
        return;
    }

    return {endpoint: subscription.endpoint, keys: {auth: keys.auth, p256dh: keys.p256dh}};
}

export async function sendNotifications(id: string, {subscription, name, caption}: Gerald) {
    if (subscription) {
        const {endpoint, headers, body, method} = await generateRequestDetails(subscription, JSON.stringify({ id, name, caption }));
        const response = await fetch(endpoint, {headers, body, method});
    }
}