import type { Metadata } from "next";

import { safeCallbackUrl } from "@/lib/auth/redirects";

import { LoginForm } from "./login-form";

export const metadata: Metadata = { title: "Sign in — hunter/seeker" };

export default async function LoginPage({ searchParams }: PageProps<"/login">) {
  const { callbackUrl } = await searchParams;
  return <LoginForm callbackUrl={safeCallbackUrl(callbackUrl) ?? undefined} />;
}
