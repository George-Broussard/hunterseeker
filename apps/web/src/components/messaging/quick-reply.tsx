"use client";

import { useState, useTransition } from "react";

import { quickReply } from "./actions";

/** One-line reply box under a conversation in the rail. */
export function QuickReply({
  conversationId,
  onSent,
}: {
  conversationId: string;
  onSent?: () => void;
}) {
  const [body, setBody] = useState("");
  const [status, setStatus] = useState<{ kind: "error" | "sent"; text: string } | null>(null);
  const [pending, startTransition] = useTransition();
  const canSend = body.trim().length > 0 && !pending;

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        if (!canSend) return;
        setStatus(null);
        startTransition(async () => {
          const result = await quickReply(conversationId, body);
          if (!result.ok) {
            setStatus({ kind: "error", text: result.message });
            return;
          }
          setBody("");
          setStatus({ kind: "sent", text: "Sent" });
          onSent?.();
        });
      }}
      className="mt-2 flex flex-col gap-1"
    >
      <div className="flex gap-1">
        <label htmlFor={`quick-reply-${conversationId}`} className="sr-only">
          Quick reply
        </label>
        <input
          id={`quick-reply-${conversationId}`}
          type="text"
          value={body}
          maxLength={10_000}
          placeholder="Quick reply…"
          disabled={pending}
          autoComplete="off"
          onChange={(event) => setBody(event.target.value)}
          className="min-w-0 flex-1 rounded-md border border-current/15 bg-transparent px-2 py-1 text-xs outline-none focus:border-current/40"
        />
        <button
          type="submit"
          disabled={!canSend}
          className="rounded-md bg-foreground px-2 py-1 text-xs font-medium text-background disabled:opacity-40"
        >
          {pending ? "…" : "Send"}
        </button>
      </div>
      {status ? (
        <p
          role={status.kind === "error" ? "alert" : "status"}
          className={`text-[11px] ${status.kind === "error" ? "" : "opacity-60"}`}
        >
          {status.text}
        </p>
      ) : null}
    </form>
  );
}
