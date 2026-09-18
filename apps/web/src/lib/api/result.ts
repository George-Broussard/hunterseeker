/** Outcome of an API call as seen by UI code: either the data or a message to render. */
export type ApiResult<T> = { ok: true; data: T } | { ok: false; message: string };
