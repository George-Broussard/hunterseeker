"use server";

/**
 * Server actions behind the interactive parts of the Hunter home. Client components call
 * these instead of the API directly so requests stay server-side (internal `API_URL`,
 * and the Hunter's token once login lands) — the browser never talks to FastAPI here.
 */

import {
  createCompanyPost,
  listCompanyFeed,
  POST_BODY_MAX_LENGTH,
  type CompanyFeedPage,
  type Post,
} from "@/lib/api/company-feed";
import type { ApiResult } from "@/lib/api/result";

export async function loadMoreCompanyFeed(cursor: string): Promise<ApiResult<CompanyFeedPage>> {
  return listCompanyFeed(cursor);
}

export async function submitCompanyPost(input: {
  companyProfileId: string;
  body: string;
}): Promise<ApiResult<Post>> {
  const body = input.body.trim();
  if (!body) {
    return { ok: false, message: "Write something before posting." };
  }
  if (body.length > POST_BODY_MAX_LENGTH) {
    return { ok: false, message: `Posts are limited to ${POST_BODY_MAX_LENGTH} characters.` };
  }
  return createCompanyPost({ company_profile_id: input.companyProfileId, body });
}
