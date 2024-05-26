import type { APIInteraction } from 'discord-api-types/payloads/v10/interactions';

const PUBLIC_KEY = '0db7dc700b1a30928ee52a198ae6cb32a96440128cedc47955a787b2ae6ad391';

// https://github.com/mrbbot/slshx
function hexDecode(data: string): Uint8Array {
	return new Uint8Array(data.match(/.{2}/g)?.map(byte => parseInt(byte, 16)) ?? []);
}

export default {
	async fetch(request: Request, env: { flag: string }): Promise<Response> {
		const url = new URL(request.url);
		if (request.method === 'POST' && url.pathname === '/interact') {
			// interaction
			const signature = request.headers.get('X-Signature-Ed25519');
			const timestamp = request.headers.get('X-Signature-Timestamp');
			if (signature === null || timestamp === null) {
				return new Response('nuh uh', { status: 401 });
			}
			const body = await request.clone().text();

			const valid = await crypto.subtle.verify(
				'NODE-ED25519',
				await crypto.subtle.importKey(
					'raw',
					hexDecode(PUBLIC_KEY),
					{ name: 'NODE-ED25519', namedCurve: 'NODE-ED25519' },
					false,
					['verify']
				),
				hexDecode(signature),
				new TextEncoder().encode(timestamp + body)
			);

			if (!valid) {
				return new Response('nuh uh', { status: 401 });
			}

			console.log({
				msg: 'validation success',
				signature,
				timestamp,
				body,
			});

			const contents = (await request.json()) as APIInteraction;
			if (contents.type === 1) {
				return new Response(JSON.stringify({ type: 1 }));
			} else if (contents.type === 2 && contents.data.name === 'flag') {
				const user = contents.member?.user ?? contents.user;
				console.log({
					msg: '/flag run',
					by: user?.id,
					in: contents.channel.id,
				});

				if (user?.id === '302968847353249813') {
					return new Response(
						JSON.stringify({ type: 4, data: { content: env.flag, flags: 64 } }),
						{
							headers: { 'Content-Type': 'application/json' },
						}
					);
				} else {
					return new Response(
						JSON.stringify({
							type: 4,
							data: { content: 'no flag for you :3', flags: 64 },
						}),
						{
							headers: { 'Content-Type': 'application/json' },
						}
					);
				}
			}
		} else if (url.pathname === '/') {
			return new Response(
				`
<!DOCTYPE html>
<html><head><title>well formed html</title></head><body><p>Welcome to my activity :)</p></body></html>`,
				{
					headers: { 'Content-Type': 'text/html' },
				}
			);
		} else if (url.pathname === '/admin/logs') {
			// the url is secret so I don't need to put this behind authentication, yay!
			return new Response(logs);
		}
		return new Response('not sure what u mean', { status: 404 });
	},
};

// `npx wrangler tail --format pretty | Out-File -FilePath .\logs.txt -Encoding utf8`
// ... one day I'll manage to afford a Cloudflare paid plan and use logpush here :(
const logs = `REDACTED`.replace(/redacted/g, "redacted");
