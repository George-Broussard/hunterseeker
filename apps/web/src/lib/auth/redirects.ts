/** Only follow same-origin, path-relative callback URLs. Anything else is dropped. */
export function safeCallbackUrl(value: unknown): string | null {
  if (typeof value !== "string" || !value.startsWith("/") || value.startsWith("//")) return null;
  if (value === "/login" || value === "/signup" || value.startsWith("/api/auth")) return null;
  return value;
}
