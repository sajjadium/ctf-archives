export const runtime = 'edge';

const DISCORD_BASE = 'https://discord.com/api/v10';

function corsHeaders(origin: string | null) {
  const h = new Headers();
  h.set('Access-Control-Allow-Origin', origin || '*');
  h.set('Access-Control-Allow-Methods', 'GET,POST,PUT,PATCH,DELETE,OPTIONS');
  h.set('Access-Control-Allow-Headers', 'Authorization,Content-Type');
  h.set('Access-Control-Max-Age', '600');
  return h;
}

function targetUrl(req: Request, segments: string[]) {
  const u = new URL(req.url);
  const path = segments.join('/');
  return `${DISCORD_BASE}/${path}${u.search}`;
}

async function proxy(req: Request, ctx: { params: { path: string[] } }) {
  const fake = process.env.FAKE_DISCORD_TOKEN;
  const real = process.env.DISCORD_BOT_TOKEN;
  if (!fake || !real) return new Response('Server misconfigured', { status: 500 });
  const origin = req.headers.get('origin');
  const auth = req.headers.get('authorization') || '';
  if (auth !== `Bot ${fake}`) return new Response('Unauthorized', { status: 401, headers: corsHeaders(origin) });
  const url = targetUrl(req, ctx.params.path || []);
  const headers = new Headers(req.headers);
  headers.set('authorization', `Bot ${real}`);
  headers.set('x-ratelimit-precision', 'millisecond');
  headers.delete('host');
  headers.delete('content-length');
  const res = await fetch(url, { method: req.method, headers, body: ['GET','HEAD'].includes(req.method) ? undefined : req.body, redirect: 'manual' });
  const merged = new Headers(res.headers);
  const cors = corsHeaders(origin);
  cors.forEach((v,k)=>merged.set(k,v));
  return new Response(res.body, { status: res.status, statusText: res.statusText, headers: merged });
}

export async function OPTIONS(req: Request) {
  return new Response(null, { status: 204, headers: corsHeaders(req.headers.get('origin')) });
}
export async function GET(req: Request, ctx: any) { return proxy(req, ctx); }
export async function POST(req: Request, ctx: any) { return proxy(req, ctx); }
export async function PUT(req: Request, ctx: any) { return proxy(req, ctx); }
export async function PATCH(req: Request, ctx: any) { return proxy(req, ctx); }
export async function DELETE(req: Request, ctx: any) { return proxy(req, ctx); }
