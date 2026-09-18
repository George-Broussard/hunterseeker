/**
 * Result shape every `lib/api/*` loader returns. Server components render either branch
 * directly; nothing here throws, so a failing API call degrades to an inline error
 * state instead of taking the whole page down.
 */
export type ApiResult<T> = { ok: true; value: T } | { ok: false; message: string };
