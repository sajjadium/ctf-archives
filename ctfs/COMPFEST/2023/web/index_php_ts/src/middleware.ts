import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { generateId } from "./utils/crypto";

// This function can be marked `async` if using `await` inside
export function middleware(request: NextRequest) {
  const response = NextResponse.next();
  if (!request.cookies.has("uid")) {
    const uid = generateId(32);
    response.cookies.set("uid", uid);
    request.cookies.set("uid", uid);
  }
  return response;
}

// See "Matching Paths" below to learn more
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    "/((?!api|_next/static|_next/image|favicon.ico).*)",
  ],
};
