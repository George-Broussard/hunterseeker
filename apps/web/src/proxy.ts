/**
 * Route guard. Runs before every page render (Next 16 `proxy`, formerly `middleware`).
 *
 * - No session → `/login?callbackUrl=<original path>` (everything is private by default).
 * - Session on `/login` or `/signup` → that persona's home.
 * - Session on the other persona's routes → own home. Personas never see each other's UI.
 *
 * This is an optimistic check on the session cookie; endpoints and server actions still
 * verify authorization themselves (AGENTS.md §8).
 */
import { NextResponse } from "next/server";

import { auth } from "@/lib/auth";
import { PERSONA_ROUTE_PREFIXES, PUBLIC_PATHS, homeFor } from "@/lib/auth/roles";

export const proxy = auth((request) => {
  const { pathname, search } = request.nextUrl;
  const session = request.auth;
  const isPublic = PUBLIC_PATHS.has(pathname);

  if (!session?.user) {
    if (isPublic) return NextResponse.next();
    const loginUrl = new URL("/login", request.nextUrl);
    if (pathname !== "/") loginUrl.searchParams.set("callbackUrl", `${pathname}${search}`);
    return NextResponse.redirect(loginUrl);
  }

  const home = homeFor(session.user.role);
  if (isPublic) return NextResponse.redirect(new URL(home, request.nextUrl));

  const owner = PERSONA_ROUTE_PREFIXES.find(
    ({ prefix }) => pathname === prefix || pathname.startsWith(`${prefix}/`),
  );
  if (owner && owner.role !== session.user.role) {
    return NextResponse.redirect(new URL(home, request.nextUrl));
  }

  return NextResponse.next();
});

export const config = {
  // Skip Auth.js's own routes, Next internals, and static assets.
  matcher: [
    "/((?!api/auth|_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp|ico)$).*)",
  ],
};
