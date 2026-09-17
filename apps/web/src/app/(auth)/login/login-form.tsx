"use client";

import Link from "next/link";
import { useActionState } from "react";

import { EMPTY_FORM_STATE, Field, FormError, SubmitButton } from "../_components/form";
import { loginAction } from "./actions";

export function LoginForm({ callbackUrl }: { callbackUrl?: string }) {
  const [state, action, pending] = useActionState(loginAction, EMPTY_FORM_STATE);

  return (
    <form action={action} noValidate className="space-y-4">
      <h1 className="text-lg font-semibold">Sign in</h1>
      <FormError message={state.error} />
      {callbackUrl && <input type="hidden" name="callbackUrl" value={callbackUrl} />}
      <Field
        label="Email"
        name="email"
        type="email"
        autoComplete="email"
        required
        defaultValue={state.values?.email}
        error={state.fieldErrors?.email}
      />
      <Field
        label="Password"
        name="password"
        type="password"
        autoComplete="current-password"
        required
        error={state.fieldErrors?.password}
      />
      <SubmitButton pending={pending} pendingLabel="Signing in…">
        Sign in
      </SubmitButton>
      <p className="text-center text-sm opacity-70">
        New to hunter/seeker?{" "}
        <Link href="/signup" className="underline underline-offset-4 opacity-100">
          Create an account
        </Link>
      </p>
    </form>
  );
}
