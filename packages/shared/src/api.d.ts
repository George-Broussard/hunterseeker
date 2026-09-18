/**
 * GENERATED FILE — DO NOT EDIT.
 *
 * Source: packages/shared/openapi.json (exported from apps/api by scripts/export_openapi.py).
 * Regenerate with `pnpm --filter @hunterseeker/shared generate`.
 */
export interface paths {
    "/health": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Health */
        get: operations["ops_health"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/profiles/me": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** The calling Seeker's Profile */
        get: operations["profiles_get_my_profile"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        /**
         * Update the calling Seeker's Profile
         * @description Partial update. Any change here must trigger re-embedding and re-matching.
         */
        patch: operations["profiles_update_my_profile"];
        trace?: never;
    };
    "/api/v1/matching/job-board": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * The calling Seeker's Job Board
         * @description Matches for the calling Seeker at or above their match threshold, best first.
         */
        get: operations["matching_list_job_board"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/matching/matches/{match_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** One Match, Seeker view */
        get: operations["matching_get_match"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/matching/jobs/{job_id}/candidates": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Ranked candidates for a Job
         * @description Every Seeker whose Profile passed this Job's ATS screening, best Match first.
         */
        get: operations["matching_list_candidates"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/matching/open-roles": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * The calling Hunter's open roles with Match activity
         * @description Open Jobs on the Company Profiles the caller manages, most recently posted first.
         *
         *     Each role carries its new-Match count, pipeline counts, and the top three ranked
         *     candidates. Candidates are Matches, so all of them have passed the Job's ATS screening.
         */
        get: operations["matching_list_open_roles"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/applications": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * The calling Seeker's Applications
         * @description The Seeker's application dashboard: every Application with its current status.
         */
        get: operations["applications_list_applications"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/ats/templates": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** The calling Hunter's ATS templates */
        get: operations["ats_list_templates"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/messaging/conversations": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** The caller's conversations, most recent first */
        get: operations["messaging_list_conversations"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/feed": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * The calling Seeker's Feed
         * @description Posts from the Seeker's Connections interleaved with new Matches, newest first.
         *
         *     Matches respect the Seeker's match threshold, as on every seeker-facing surface.
         */
        get: operations["feed_list_feed"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/feed/company": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * The calling Hunter's company feed
         * @description Posts from the Company Profiles the caller manages and from their network, newest first.
         */
        get: operations["feed_list_company_feed"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/feed/company/posts": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Post to the company feed as a Company Profile */
        post: operations["feed_create_company_post"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/feed/company-profiles": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Company Profiles the calling Hunter manages
         * @description The Company Profiles the caller may post as.
         *
         *     Stopgap until a Company Profile domain exists.
         */
        get: operations["feed_list_company_profiles"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/network/connections": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** The caller's Connections */
        get: operations["network_list_connections"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/imports/runs": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Import runs for the calling Hunter's Company Profiles */
        get: operations["imports_list_import_runs"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
}
export type webhooks = Record<string, never>;
export interface components {
    schemas: {
        /** Application */
        Application: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            job: components["schemas"]["JobSummary"];
            /**
             * Match Id
             * Format: uuid
             * @description The Match this Application came through. Applications exist only via a Match.
             */
            match_id: string;
            status: components["schemas"]["ApplicationStatus"];
            /**
             * Current Stage
             * @description Name of the ATS stage the Application is in.
             */
            current_stage: string;
            /**
             * Submitted At
             * Format: date-time
             */
            submitted_at: string;
            /**
             * Updated At
             * Format: date-time
             */
            updated_at: string;
        };
        /** @enum {string} */
        ApplicationStatus: "submitted" | "in_review" | "interviewing" | "offered" | "hired" | "rejected" | "withdrawn";
        AtsStage: components["schemas"]["ScreeningStage"] | components["schemas"]["HumanStage"];
        /** AtsTemplate */
        AtsTemplate: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /**
             * Hunter Id
             * Format: uuid
             */
            hunter_id: string;
            /** Name */
            name: string;
            /**
             * Stages
             * @description In pipeline order. Screening stages come first.
             */
            stages: components["schemas"]["AtsStage"][];
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /**
             * Updated At
             * Format: date-time
             */
            updated_at: string;
        };
        /**
         * CompanyPostCreate
         * @description Body for posting to the company feed as a Company Profile.
         */
        CompanyPostCreate: {
            /**
             * Company Profile Id
             * Format: uuid
             * @description The Company Profile to post as. The caller must manage it.
             */
            company_profile_id: string;
            /** Body */
            body: string;
        };
        /**
         * CompanyProfileSummary
         * @description A Company Profile as referenced from a post.
         *
         *     Lives in the feed contract until a Company Profile domain exists; see the follow-up
         *     issue on Company Profile management.
         */
        CompanyProfileSummary: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Name */
            name: string;
        };
        /** Connection */
        Connection: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** @description The other party, from the caller's point of view. */
            user: components["schemas"]["UserSummary"];
            status: components["schemas"]["ConnectionStatus"];
            /**
             * Connected At
             * @description Null until accepted.
             */
            connected_at?: string | null;
        };
        /** @enum {string} */
        ConnectionStatus: "pending_sent" | "pending_received" | "connected";
        /** Conversation */
        Conversation: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Participants */
            participants: components["schemas"]["UserSummary"][];
            last_message?: components["schemas"]["Message"] | null;
            /**
             * Unread Count
             * @description Unread by the caller.
             */
            unread_count: number;
            /**
             * Updated At
             * Format: date-time
             */
            updated_at: string;
        };
        /** @enum {string} */
        CriterionOperator: "eq" | "neq" | "gte" | "lte" | "in" | "contains_all" | "contains_any";
        /**
         * ErrorBody
         * @description The ``error`` object inside the envelope.
         */
        ErrorBody: {
            /**
             * Code
             * @description Stable, machine-readable identifier, e.g. `not_found`.
             */
            code: string;
            /**
             * Message
             * @description Human-readable explanation. Not stable; do not parse.
             */
            message: string;
            /** @description Free-form context, or null. */
            details?: components["schemas"]["JsonValue"];
        };
        /**
         * ErrorEnvelope
         * @description Body of every error response.
         */
        ErrorEnvelope: {
            error: components["schemas"]["ErrorBody"];
        };
        FeedItem: components["schemas"]["Post"] | components["schemas"]["MatchedJobItem"];
        /** HumanStage */
        HumanStage: {
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "human";
            /** Name */
            name: string;
            /** Description */
            description?: string | null;
        };
        /**
         * ImportRun
         * @description One execution of an import. Idempotent per external job id; re-runs never duplicate.
         */
        ImportRun: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /**
             * Company Profile Id
             * Format: uuid
             */
            company_profile_id: string;
            source: components["schemas"]["ImportSource"];
            status: components["schemas"]["ImportRunStatus"];
            /** Started At */
            started_at?: string | null;
            /** Finished At */
            finished_at?: string | null;
            /**
             * Jobs Seen
             * @default 0
             */
            jobs_seen: number;
            /**
             * Jobs Created
             * @default 0
             */
            jobs_created: number;
            /**
             * Jobs Updated
             * @default 0
             */
            jobs_updated: number;
            /**
             * Error
             * @description Set when `status` is `failed`.
             */
            error?: string | null;
        };
        /** @enum {string} */
        ImportRunStatus: "queued" | "running" | "succeeded" | "failed";
        /** @enum {string} */
        ImportSource: "ashby" | "greenhouse";
        /**
         * JobSummary
         * @description A Job as referenced from a Match, an Application, or the Feed.
         */
        JobSummary: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Title */
            title: string;
            /**
             * Company Profile Id
             * Format: uuid
             */
            company_profile_id: string;
            /** Company Name */
            company_name: string;
            /** Location */
            location?: string | null;
            /**
             * Remote
             * @default false
             */
            remote: boolean;
            /**
             * Compensation Min
             * @description Annual, in `currency`.
             */
            compensation_min?: number | null;
            /**
             * Compensation Max
             * @description Annual, in `currency`.
             */
            compensation_max?: number | null;
            /**
             * Currency
             * @description ISO 4217 code.
             * @default USD
             */
            currency: string;
            /** Seniority */
            seniority?: string | null;
            /**
             * Posted At
             * Format: date-time
             */
            posted_at: string;
        };
        JsonValue: {
            [key: string]: unknown;
        } | unknown[] | string | number | boolean | null;
        /**
         * MatchedCandidate
         * @description Hunter-side view of the same Match: the Seeker it surfaces.
         */
        MatchedCandidate: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /**
             * Score
             * @description Normalized 0-1 Match score.
             */
            score: number;
            /**
             * Ats Pass
             * @description Always `true`: a Match exists only if the Seeker's Profile has already passed the Job's ATS screening. Present so the invariant is visible in the contract.
             * @default true
             * @constant
             */
            ats_pass: true;
            /**
             * Computed At
             * Format: date-time
             * @description When `score` was last (re)computed.
             */
            computed_at: string;
            seeker: components["schemas"]["UserSummary"];
            /**
             * Headline
             * @description The Seeker's Profile headline. Readable only through this Match.
             */
            headline?: string | null;
        };
        /**
         * MatchedJob
         * @description Seeker-side view of a Match: the Job it recommends.
         */
        MatchedJob: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /**
             * Score
             * @description Normalized 0-1 Match score.
             */
            score: number;
            /**
             * Ats Pass
             * @description Always `true`: a Match exists only if the Seeker's Profile has already passed the Job's ATS screening. Present so the invariant is visible in the contract.
             * @default true
             * @constant
             */
            ats_pass: true;
            /**
             * Computed At
             * Format: date-time
             * @description When `score` was last (re)computed.
             */
            computed_at: string;
            job: components["schemas"]["JobSummary"];
        };
        /** MatchedJobItem */
        MatchedJobItem: {
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "matched_job";
            /**
             * Id
             * Format: uuid
             * @description Feed item id, distinct from `match.id`.
             */
            id: string;
            match: components["schemas"]["MatchedJob"];
            /**
             * Created At
             * Format: date-time
             * @description When the Match entered the Feed.
             */
            created_at: string;
        };
        /** Message */
        Message: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /**
             * Conversation Id
             * Format: uuid
             */
            conversation_id: string;
            sender: components["schemas"]["UserSummary"];
            /** Body */
            body: string;
            /**
             * Sent At
             * Format: date-time
             */
            sent_at: string;
        };
        /**
         * OpenRole
         * @description Hunter-side summary of one open Job: its Match activity and pipeline state.
         *
         *     The Hunter's mirror of the Job Board card. ``top_candidates`` are Matches, so each one
         *     has already passed the Job's ATS screening (``ats_pass`` is always ``true``).
         */
        OpenRole: {
            job: components["schemas"]["JobSummary"];
            /**
             * New Match Count
             * @description Matches created since the calling Hunter last viewed this role.
             */
            new_match_count: number;
            pipeline: components["schemas"]["RolePipelineCounts"];
            /**
             * Top Candidates
             * @description Highest-scoring Matches for the Job, best first. At most three.
             */
            top_candidates: components["schemas"]["MatchedCandidate"][];
        };
        /** Page[Application] */
        Page_Application_: {
            /** Items */
            items: components["schemas"]["Application"][];
            /**
             * Next Cursor
             * @description Pass as `cursor` to fetch the next page. `null` on the last page.
             */
            next_cursor?: string | null;
        };
        /** Page[AtsTemplate] */
        Page_AtsTemplate_: {
            /** Items */
            items: components["schemas"]["AtsTemplate"][];
            /**
             * Next Cursor
             * @description Pass as `cursor` to fetch the next page. `null` on the last page.
             */
            next_cursor?: string | null;
        };
        /** Page[CompanyProfileSummary] */
        Page_CompanyProfileSummary_: {
            /** Items */
            items: components["schemas"]["CompanyProfileSummary"][];
            /**
             * Next Cursor
             * @description Pass as `cursor` to fetch the next page. `null` on the last page.
             */
            next_cursor?: string | null;
        };
        /** Page[Connection] */
        Page_Connection_: {
            /** Items */
            items: components["schemas"]["Connection"][];
            /**
             * Next Cursor
             * @description Pass as `cursor` to fetch the next page. `null` on the last page.
             */
            next_cursor?: string | null;
        };
        /** Page[Conversation] */
        Page_Conversation_: {
            /** Items */
            items: components["schemas"]["Conversation"][];
            /**
             * Next Cursor
             * @description Pass as `cursor` to fetch the next page. `null` on the last page.
             */
            next_cursor?: string | null;
        };
        /** Page[FeedItem] */
        Page_FeedItem_: {
            /** Items */
            items: components["schemas"]["FeedItem"][];
            /**
             * Next Cursor
             * @description Pass as `cursor` to fetch the next page. `null` on the last page.
             */
            next_cursor?: string | null;
        };
        /** Page[ImportRun] */
        Page_ImportRun_: {
            /** Items */
            items: components["schemas"]["ImportRun"][];
            /**
             * Next Cursor
             * @description Pass as `cursor` to fetch the next page. `null` on the last page.
             */
            next_cursor?: string | null;
        };
        /** Page[MatchedCandidate] */
        Page_MatchedCandidate_: {
            /** Items */
            items: components["schemas"]["MatchedCandidate"][];
            /**
             * Next Cursor
             * @description Pass as `cursor` to fetch the next page. `null` on the last page.
             */
            next_cursor?: string | null;
        };
        /** Page[MatchedJob] */
        Page_MatchedJob_: {
            /** Items */
            items: components["schemas"]["MatchedJob"][];
            /**
             * Next Cursor
             * @description Pass as `cursor` to fetch the next page. `null` on the last page.
             */
            next_cursor?: string | null;
        };
        /** Page[OpenRole] */
        Page_OpenRole_: {
            /** Items */
            items: components["schemas"]["OpenRole"][];
            /**
             * Next Cursor
             * @description Pass as `cursor` to fetch the next page. `null` on the last page.
             */
            next_cursor?: string | null;
        };
        /** Page[Post] */
        Page_Post_: {
            /** Items */
            items: components["schemas"]["Post"][];
            /**
             * Next Cursor
             * @description Pass as `cursor` to fetch the next page. `null` on the last page.
             */
            next_cursor?: string | null;
        };
        /** @enum {string} */
        Persona: "seeker" | "hunter";
        /** Post */
        Post: {
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "post";
            /**
             * Id
             * Format: uuid
             */
            id: string;
            author: components["schemas"]["UserSummary"];
            /** @description Set when a Hunter posted *as* a Company Profile they manage; `author` is then that Hunter. Null for a post made as oneself. */
            company?: components["schemas"]["CompanyProfileSummary"] | null;
            /** Body */
            body: string;
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
        };
        /** Profile */
        Profile: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /**
             * Seeker Id
             * Format: uuid
             */
            seeker_id: string;
            /** Headline */
            headline?: string | null;
            /** Summary */
            summary?: string | null;
            /** Skills */
            skills?: string[];
            /**
             * Locations
             * @description Metro areas the Seeker will work in.
             */
            locations?: string[];
            /**
             * Remote Ok
             * @default true
             */
            remote_ok: boolean;
            work_authorization?: components["schemas"]["WorkAuthorization"] | null;
            /**
             * Compensation Floor
             * @description Annual, in `currency`. A hard constraint, not a score input.
             */
            compensation_floor?: number | null;
            /**
             * Currency
             * @description ISO 4217 code.
             * @default USD
             */
            currency: string;
            seniority?: components["schemas"]["Seniority"] | null;
            /**
             * Match Threshold
             * @description Seeker-controlled floor. Matches below it are not surfaced.
             * @default 0.5
             */
            match_threshold: number;
            /**
             * Updated At
             * Format: date-time
             */
            updated_at: string;
        };
        /**
         * ProfileUpdate
         * @description PATCH body: every field optional; omitted fields are left unchanged.
         */
        ProfileUpdate: {
            /** Headline */
            headline?: string | null;
            /** Summary */
            summary?: string | null;
            /** Skills */
            skills?: string[] | null;
            /** Locations */
            locations?: string[] | null;
            /** Remote Ok */
            remote_ok?: boolean | null;
            work_authorization?: components["schemas"]["WorkAuthorization"] | null;
            /** Compensation Floor */
            compensation_floor?: number | null;
            /** Currency */
            currency?: string | null;
            seniority?: components["schemas"]["Seniority"] | null;
            /** Match Threshold */
            match_threshold?: number | null;
        };
        /**
         * RolePipelineCounts
         * @description How many Seekers sit at each point of a Job's pipeline, as shown on a role card.
         */
        RolePipelineCounts: {
            /**
             * Screened
             * @description Matches for the Job: every Seeker whose Profile passed its ATS screening. This is the whole candidate pool — nobody unscreened is counted anywhere.
             */
            screened: number;
            /**
             * Interviewing
             * @description Applications currently in a human interview stage.
             */
            interviewing: number;
            /**
             * Offer
             * @description Applications with an offer extended.
             */
            offer: number;
        };
        /**
         * ScreeningCriterion
         * @description One machine-evaluable check against a Profile field.
         */
        ScreeningCriterion: {
            /**
             * Field
             * @description Profile field the check reads, e.g. `work_authorization`, `skills`.
             */
            field: string;
            operator: components["schemas"]["CriterionOperator"];
            /** Value */
            value: string | number | boolean | string[];
        };
        /** ScreeningStage */
        ScreeningStage: {
            /**
             * @description discriminator enum property added by openapi-typescript
             * @enum {string}
             */
            kind: "screening";
            /** Name */
            name: string;
            /**
             * Criteria
             * @description All must pass. Evaluated by the engine before any Match exists.
             */
            criteria: components["schemas"]["ScreeningCriterion"][];
        };
        /** @enum {string} */
        Seniority: "intern" | "junior" | "mid" | "senior" | "staff" | "principal" | "executive";
        /**
         * UserSummary
         * @description The minimal public view of a user, embedded wherever a user is referenced.
         */
        UserSummary: {
            /**
             * Id
             * Format: uuid
             */
            id: string;
            persona: components["schemas"]["Persona"];
            /**
             * Display Name
             * @description What other users see. Never a legal name.
             */
            display_name: string;
        };
        /** @enum {string} */
        WorkAuthorization: "citizen" | "permanent_resident" | "visa" | "needs_sponsorship";
    };
    responses: never;
    parameters: never;
    requestBodies: never;
    headers: never;
    pathItems: never;
}
export type $defs = Record<string, never>;
export interface operations {
    ops_health: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": {
                        [key: string]: string;
                    };
                };
            };
            /** @description Validation error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Client error */
            "4XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Server error */
            "5XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
        };
    };
    profiles_get_my_profile: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Profile"];
                };
            };
            /** @description Validation error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Client error */
            "4XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Server error */
            "5XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
        };
    };
    profiles_update_my_profile: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ProfileUpdate"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Profile"];
                };
            };
            /** @description Validation error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Client error */
            "4XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Server error */
            "5XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
        };
    };
    matching_list_job_board: {
        parameters: {
            query?: {
                /** @description Opaque cursor from a previous page's `next_cursor`. Omit for the first page. */
                cursor?: string | null;
                /** @description Page size, 1-100. */
                limit?: number;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Page_MatchedJob_"];
                };
            };
            /** @description Validation error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Client error */
            "4XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Server error */
            "5XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
        };
    };
    matching_get_match: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                match_id: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["MatchedJob"];
                };
            };
            /** @description Validation error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Client error */
            "4XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Server error */
            "5XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
        };
    };
    matching_list_candidates: {
        parameters: {
            query?: {
                /** @description Opaque cursor from a previous page's `next_cursor`. Omit for the first page. */
                cursor?: string | null;
                /** @description Page size, 1-100. */
                limit?: number;
            };
            header?: never;
            path: {
                job_id: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Page_MatchedCandidate_"];
                };
            };
            /** @description Validation error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Client error */
            "4XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Server error */
            "5XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
        };
    };
    matching_list_open_roles: {
        parameters: {
            query?: {
                /** @description Opaque cursor from a previous page's `next_cursor`. Omit for the first page. */
                cursor?: string | null;
                /** @description Page size, 1-100. */
                limit?: number;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Page_OpenRole_"];
                };
            };
            /** @description Validation error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Client error */
            "4XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Server error */
            "5XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
        };
    };
    applications_list_applications: {
        parameters: {
            query?: {
                /** @description Opaque cursor from a previous page's `next_cursor`. Omit for the first page. */
                cursor?: string | null;
                /** @description Page size, 1-100. */
                limit?: number;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Page_Application_"];
                };
            };
            /** @description Validation error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Client error */
            "4XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Server error */
            "5XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
        };
    };
    ats_list_templates: {
        parameters: {
            query?: {
                /** @description Opaque cursor from a previous page's `next_cursor`. Omit for the first page. */
                cursor?: string | null;
                /** @description Page size, 1-100. */
                limit?: number;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Page_AtsTemplate_"];
                };
            };
            /** @description Validation error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Client error */
            "4XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Server error */
            "5XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
        };
    };
    messaging_list_conversations: {
        parameters: {
            query?: {
                /** @description Opaque cursor from a previous page's `next_cursor`. Omit for the first page. */
                cursor?: string | null;
                /** @description Page size, 1-100. */
                limit?: number;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Page_Conversation_"];
                };
            };
            /** @description Validation error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Client error */
            "4XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Server error */
            "5XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
        };
    };
    feed_list_feed: {
        parameters: {
            query?: {
                /** @description Opaque cursor from a previous page's `next_cursor`. Omit for the first page. */
                cursor?: string | null;
                /** @description Page size, 1-100. */
                limit?: number;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Page_FeedItem_"];
                };
            };
            /** @description Validation error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Client error */
            "4XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Server error */
            "5XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
        };
    };
    feed_list_company_feed: {
        parameters: {
            query?: {
                /** @description Opaque cursor from a previous page's `next_cursor`. Omit for the first page. */
                cursor?: string | null;
                /** @description Page size, 1-100. */
                limit?: number;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Page_Post_"];
                };
            };
            /** @description Validation error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Client error */
            "4XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Server error */
            "5XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
        };
    };
    feed_create_company_post: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["CompanyPostCreate"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Post"];
                };
            };
            /** @description Validation error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Client error */
            "4XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Server error */
            "5XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
        };
    };
    feed_list_company_profiles: {
        parameters: {
            query?: {
                /** @description Opaque cursor from a previous page's `next_cursor`. Omit for the first page. */
                cursor?: string | null;
                /** @description Page size, 1-100. */
                limit?: number;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Page_CompanyProfileSummary_"];
                };
            };
            /** @description Validation error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Client error */
            "4XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Server error */
            "5XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
        };
    };
    network_list_connections: {
        parameters: {
            query?: {
                /** @description Opaque cursor from a previous page's `next_cursor`. Omit for the first page. */
                cursor?: string | null;
                /** @description Page size, 1-100. */
                limit?: number;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Page_Connection_"];
                };
            };
            /** @description Validation error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Client error */
            "4XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Server error */
            "5XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
        };
    };
    imports_list_import_runs: {
        parameters: {
            query?: {
                /** @description Opaque cursor from a previous page's `next_cursor`. Omit for the first page. */
                cursor?: string | null;
                /** @description Page size, 1-100. */
                limit?: number;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Page_ImportRun_"];
                };
            };
            /** @description Validation error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Client error */
            "4XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
            /** @description Server error */
            "5XX": {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ErrorEnvelope"];
                };
            };
        };
    };
}
