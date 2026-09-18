"use server";

import { AuthError } from "next-auth";

import { signIn } from "@/lib/auth";
import { SignupError, signupUser } from "@/lib/auth/api";
import { homeFor, isPersona } from "@/lib/auth/roles";

import type { FormState } from "../_components/form";

const PASSWORD_MIN_LENGTH = 8; // mirrors apps/api auth/schemas.py

export async function signupAction(_prev: FormState, formData: FormData): Promise<FormState> {
  const name = String(formData.get("name") ?? "").trim();
  const email = String(formData.get("email") ?? "").trim();
  const password = String(formData.get("password") ?? "");
  const role = formData.get("role");
  const values = { name, email, role: typeof role === "string" ? role : undefined };

  const fieldErrors: FormState["fieldErrors"] = {};
  if (!isPersona(role)) fieldErrors.role = "Choose whether you're a Seeker or a Hunter.";
  if (!name) fieldErrors.name = "Enter your name.";
  if (!email || !email.includes("@")) fieldErrors.email = "Enter a valid email address.";
  if (password.length < PASSWORD_MIN_LENGTH) {
    fieldErrors.password = `Use at least ${PASSWORD_MIN_LENGTH} characters.`;
  }
  if (Object.keys(fieldErrors).length > 0 || !isPersona(role)) return { fieldErrors, values };

  try {
    await signupUser({ email, password, name, role });
  } catch (error) {
    if (error instanceof SignupError) {
      return error.status === 409
        ? { fieldErrors: { email: error.message }, values }
        : { error: error.message, values };
    }
    throw error;
  }

  try {
    // Throws NEXT_REDIRECT on success — let it propagate.
    await signIn("credentials", { email, password, redirectTo: homeFor(role) });
  } catch (error) {
    if (error instanceof AuthError) {
      return { error: "Your account was created but sign-in failed. Please sign in.", values };
    }
    throw error;
  }
  return {};
}
