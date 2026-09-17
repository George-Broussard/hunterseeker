/**
 * Auth.js configuration (decided in #3): sessions live here as a JWT cookie; the persona
 * role is a claim; FastAPI receives a separately signed bearer token (`session.apiToken`).
 *
 * Server components: `const session = await auth()` → `session?.user.role`.
 * API calls:         `Authorization: Bearer ${session.apiToken}`.
 */
import NextAuth, { type DefaultSession } from "next-auth";
import Credentials from "next-auth/providers/credentials";

import type { Persona } from "@hunterseeker/shared";

import { verifyCredentials } from "./api";
import { signApiToken } from "./api-token";
import { isPersona } from "./roles";

declare module "next-auth" {
  interface User {
    role: Persona;
  }
  interface Session {
    user: { id: string; role: Persona } & DefaultSession["user"];
    /** HS256 JWT for FastAPI; short-lived, re-minted whenever the session is read. */
    apiToken: string;
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    role?: Persona;
  }
}

export const { handlers, auth, signIn, signOut } = NextAuth({
  session: { strategy: "jwt" },
  pages: { signIn: "/login" },
  providers: [
    Credentials({
      credentials: { email: {}, password: {} },
      async authorize(credentials) {
        const email = typeof credentials.email === "string" ? credentials.email : "";
        const password = typeof credentials.password === "string" ? credentials.password : "";
        if (!email || !password) return null;
        const user = await verifyCredentials(email, password);
        if (!user) return null;
        return { id: user.id, email: user.email, name: user.name, role: user.role };
      },
    }),
  ],
  callbacks: {
    jwt({ token, user }) {
      if (user) {
        token.sub = user.id;
        token.role = user.role;
      }
      return token;
    },
    async session({ session, token }) {
      if (!token.sub || !isPersona(token.role)) {
        // A token without our claims (e.g. from a previous schema) is not a usable session.
        throw new Error("session token is missing the user id or role claim");
      }
      session.user.id = token.sub;
      session.user.role = token.role;
      session.apiToken = await signApiToken({
        userId: token.sub,
        role: token.role,
        email: session.user.email ?? "",
      });
      return session;
    },
  },
});
