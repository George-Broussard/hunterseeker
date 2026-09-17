"use server";

import { AuthError } from "next-auth";
import { redirect } from "next/navigation";

import { signIn } from "@/lib/auth";
import { readFreshSessionRole } from "@/lib/auth/fresh-session";
import { safeCallbackUrl } from "@/lib/auth/redirects";
import { homeFor } from "@/lib/auth/roles";

import type { FormState } from "../_components/form";

export async function loginAction(_prev: FormState, formData: FormData): Promise<FormState> {
  const email = String(formData.get("email") ?? "").trim();
  const password = String(formData.get("password") ?? "");
  const values = { email };

  const fieldErrors: FormState["fieldErrors"] = {};
  if (!email) fieldErrors.email = "Enter your email address.";
  if (!password) fieldErrors.password = "Enter your password.";
  if (fieldErrors.email || fieldErrors.password) return { fieldErrors, values };

  try {
    await signIn("credentials", { email, password, redirect: false });
  } catch (error) {
    if (error instanceof AuthError) {
      return { error: "That email and password don't match.", values };
    }
    throw error;
  }

  const role = await readFreshSessionRole();
  if (!role) return { error: "Signed in, but the session could not be read. Try again.", values };
  redirect(safeCallbackUrl(formData.get("callbackUrl")) ?? homeFor(role));
}
