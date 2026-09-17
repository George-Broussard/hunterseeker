"use client";

import Link from "next/link";
import { useActionState } from "react";

import { EMPTY_FORM_STATE, Field, FormError, SubmitButton } from "../_components/form";
import { PersonaChooser } from "../_components/persona-chooser";
import { signupAction } from "./actions";

export function SignupForm() {
  const [state, action, pending] = useActionState(signupAction, EMPTY_FORM_STATE);

  return (
    <form action={action} noValidate className="space-y-4">
      <h1 className="text-lg font-semibold">Create your account</h1>
      <FormError message={state.error} />
      <PersonaChooser value={state.values?.role} error={state.fieldErrors?.role} />
      <Field
        label="Name"
        name="name"
        autoComplete="name"
        required
        defaultValue={state.values?.name}
        error={state.fieldErrors?.name}
      />
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
        autoComplete="new-password"
        required
        minLength={8}
        hint="At least 8 characters."
        error={state.fieldErrors?.password}
      />
      <SubmitButton pending={pending} pendingLabel="Creating account…">
        Create account
      </SubmitButton>
      <p className="text-center text-sm opacity-70">
        Already have an account?{" "}
        <Link href="/login" className="underline underline-offset-4 opacity-100">
          Sign in
        </Link>
      </p>
    </form>
  );
}
