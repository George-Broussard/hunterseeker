"use client";

import type { InputHTMLAttributes, ReactNode } from "react";

/** Shape every auth server action returns. `values` lets the form keep what the user typed. */
export interface FormState {
  error?: string;
  fieldErrors?: Record<string, string | undefined>;
  values?: Record<string, string | undefined>;
}

export const EMPTY_FORM_STATE: FormState = {};

export function FormError({ message }: { message?: string }) {
  if (!message) return null;
  return (
    <p
      role="alert"
      className="rounded-md border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-700 dark:text-red-300"
    >
      {message}
    </p>
  );
}

interface FieldProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  name: string;
  error?: string;
  hint?: string;
}

export function Field({ label, name, error, hint, id = name, ...input }: FieldProps) {
  const errorId = `${id}-error`;
  const hintId = `${id}-hint`;
  return (
    <div className="space-y-1.5">
      <label htmlFor={id} className="block text-sm font-medium">
        {label}
      </label>
      <input
        id={id}
        name={name}
        aria-invalid={error ? true : undefined}
        aria-describedby={[error && errorId, hint && hintId].filter(Boolean).join(" ") || undefined}
        className="block w-full rounded-md border border-foreground/20 bg-background px-3 py-2 text-sm outline-none focus:border-foreground focus:ring-2 focus:ring-foreground/20 aria-invalid:border-red-500"
        {...input}
      />
      {hint && !error && (
        <p id={hintId} className="text-xs opacity-60">
          {hint}
        </p>
      )}
      {error && (
        <p id={errorId} className="text-xs text-red-700 dark:text-red-300">
          {error}
        </p>
      )}
    </div>
  );
}

export function SubmitButton({
  pending,
  children,
  pendingLabel,
}: {
  pending: boolean;
  children: ReactNode;
  pendingLabel: string;
}) {
  return (
    <button
      type="submit"
      disabled={pending}
      aria-busy={pending}
      className="flex w-full items-center justify-center rounded-md bg-foreground px-4 py-2 text-sm font-medium text-background transition-opacity disabled:opacity-60"
    >
      {pending ? pendingLabel : children}
    </button>
  );
}
