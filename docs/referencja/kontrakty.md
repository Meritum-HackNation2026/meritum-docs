---
icon: lucide/braces
---

# Kontrakty danych


<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

Wersja kontraktu: `3`. Źródło prawdy to `contracts/meritum.schema.json` w meritum-core, generowany z `meritum_core.checks.contracts` ([ADR-02](../adr/adr-02.md)). Opisy pól są po angielsku, tak jak w kodzie.

| Model | Opis |
|---|---|
| [CheckRequest](#checkrequest) | What a channel adapter sends to the verification core |
| [Citation](#citation) | A fragment of a source and how it bears on the claim |
| [ClaimResult](#claimresult) | One checked claim |
| [ClaimReviewContext](#claimreviewcontext) | A fact-checker's ClaimReview rating found through Google Fact Check Tools API, shown as context with a link |
| [Escalation](#escalation) | Hand-off to the moderator queue |
| [EvidenceStrength](#evidencestrength) | Strength level together with the premises it follows from. |
| [IncidentMatch](#incidentmatch) | Similarity to a known incident (organiser's database or the local EUvsDisinfo copy) |
| [Premises](#premises) | Explicit premises behind a verdict (MSZ: strength must follow from quality, recency, agreement, independence). |
| [Source](#source) | A document from the audited corpus |
| [SourceStatusWarning](#sourcestatuswarning) | Neutral note that the checked content comes from an entity on the official EU sanctions list |
| [CheckResult](#checkresult) | The answer every channel renders |
| [CachedResult](#cachedresult) | What the result cache keeps: only the substantive part of a CheckResult |
| [AnalysisStep](#analysisstep) | One step of the processing strip shown between „Sprawdź” and the result. |
| [AnalysisStatus](#analysisstatus) | Polled (or streamed) by every channel while a check runs; mirrors the DBOS workflow. |
| [InjectionEvent](#injectionevent) | Instructions found in the input or a source |
| [ModelUsage](#modelusage) | One model call: provider, model, region of processing, tokens and cost. |
| [CheckRecord](#checkrecord) | Audit log of one check (MSZ MVP: question, time, sources, result; plus observability). |
| [CaseClaim](#caseclaim) | One claim in a case and the checks that asked it: unanswered ("insufficient_evidence"), or disputed by a user. |
| [ModeratorCase](#moderatorcase) | One case per group of similar unanswered claims |
| [CatalogEntry](#catalogentry) | One domain in the open source catalogue: why it qualifies, how it is refreshed, whether it is excluded. |
| [Notification](#notification) | An inbox entry, pushed live over SSE or WebSocket from DBOS events and shown as a toast |

## CheckRequest

What a channel adapter sends to the verification core. The core is channel-agnostic.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `channel` | `web` \| `extension` \| `discord` \| `sms` \| `mcp` | tak |  |
| `text` | `string` \| `null` |  |  |
| `url` | `string` (uri) \| `null` |  |  |
| `page_url` | `string` (uri) \| `null` |  | Extension only: the post the text came from. |
| `audio_id` | `string` \| `null` |  | Uploaded audio file or Discord voice message; transcribed in an EU region, then checked like text. |

## Citation

A fragment of a source and how it bears on the claim. The pipeline drops fragments it cannot find verbatim.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `source` | [Source](#source) | tak |  |
| `fragment` | `string` | tak |  |
| `stance` | `supports` \| `refutes` \| `context` | tak |  |
| `validity` | `expires` \| `in_force` \| `updated_in_place` \| `past_event` \| `superseded` |  | Age rule for this piece of evidence: the catalogue entry's validity, or past_event / superseded set per evidence. |
| `fragment_found_verbatim` | `True` |  |  |

## ClaimResult

One checked claim. Citations (source material) are kept apart from `explanation` (model interpretation).

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `claim` | `string` | tak |  |
| `claim_date` | `string` (date) \| `null` |  | The date the claim refers to; evidence age is measured against it. |
| `claim_date_source` | `text` \| `input_published_at` \| `today` \| `null` |  |  |
| `verdict` | `confirmed` \| `false` \| `misleading` \| `insufficient_evidence` \| `not_verifiable` | tak |  |
| `strength` | [EvidenceStrength](#evidencestrength) \| `null` |  |  |
| `citations` | lista: [Citation](#citation) |  |  |
| `explanation` | `string` | tak |  |
| `unresolved` | `string` \| `null` |  | What could not be established. |
| `archival` | `boolean` |  | Newest evidence is older than the claim's context needs. |
| `technique` | `false_authority` \| `conspiracy_theory` \| `out_of_context` \| `outdated` \| `fabricated_quote` \| `manipulated_media` \| `impersonation` \| `cherry_picking` \| `null` |  |  |
| `incident` | [IncidentMatch](#incidentmatch) \| `null` |  |  |
| `claim_reviews` | lista: [ClaimReviewContext](#claimreviewcontext) |  |  |

## ClaimReviewContext

A fact-checker's ClaimReview rating found through Google Fact Check Tools API, shown as context with a link. Never a citation, never counted towards strength, kept no longer than the API's cache headers allow.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `publisher` | `string` | tak |  |
| `rating` | `string` | tak | textualRating as published. |
| `url` | `string` (uri) | tak |  |
| `reviewed_at` | `string` (date-time) \| `null` |  |  |

## Escalation

Hand-off to the moderator queue. 'recommended' means nobody was notified yet. Computed on every request, cache hits included: the result cache never stores it.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `state` | `recommended` \| `created` \| `updated` | tak |  |
| `case_id` | `string` \| `null` |  |  |

## EvidenceStrength

Strength level together with the premises it follows from.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `level` | `strong` \| `moderate` \| `weak` | tak |  |
| `premises` | [Premises](#premises) | tak |  |

## IncidentMatch

Similarity to a known incident (organiser's database or the local EUvsDisinfo copy). Context only. Never a basis for the verdict by itself, and never changes it. An EUvsDisinfo `fact` text is cited as a Citation, not carried here. `domain` is the one explicitly defined warning case: the checked URL is on a domain the incident database lists (for EUvsDisinfo: linksToDisinformation), and the incident's topic matches the claim.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `database` | `organiser` \| `euvsdisinfo` |  |  |
| `incident_id` | `string` | tak |  |
| `matched_on` | `content` \| `domain` |  |  |
| `title` | `string` | tak |  |
| `date` | `string` (date-time) | tak |  |
| `url` | `string` (uri) | tak |  |
| `similarity` | `number` | tak |  |

## Premises

Explicit premises behind a verdict (MSZ: strength must follow from quality, recency, agreement, independence).

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `independent_sources` | `integer` | tak | Distinct publishers (publisher_id) among the citations whose stance agrees with the verdict. |
| `primary_sources` | `integer` | tak | Distinct primary-tier publishers among the agreeing citations. |
| `newest_source_published_at` | `string` (date-time) \| `null` |  | Publication date of the newest agreeing source, shown as a date. |
| `newest_source_age_hours` | `integer` \| `null` |  | Hours from the newest agreeing source to the claim date (ClaimResult.claim_date), not to now; 0 when the source is newer. |
| `max_age_hours` | `integer` |  | Threshold from the catalogue entry of the newest source. |
| `validity` | `expires` \| `in_force` \| `updated_in_place` \| `past_event` \| `superseded` |  |  |
| `agreement` | `consistent` \| `conflicting` | tak |  |

## Source

A document from the audited corpus. Title, publisher, date and link are mandatory to show (MSZ section 2).

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `id` | `string` | tak |  |
| `title` | `string` | tak |  |
| `publisher` | `string` | tak |  |
| `publisher_id` | `string` | tak | Publisher id from the catalogue; independence is counted on it. |
| `url` | `string` (uri) | tak |  |
| `domain` | `string` | tak |  |
| `kind` | `akt_prawny` \| `dane_publiczne` \| `instytucja` \| `fact_check` \| `media` | tak |  |
| `tier` | `primary` \| `secondary` | tak |  |
| `published_at` | `string` (date-time) \| `null` |  |  |
| `fetched_at` | `string` (date-time) | tak |  |
| `language` | `string` |  |  |
| `via` | `corpus` \| `rss` \| `web_search` \| `mcp` |  |  |

## SourceStatusWarning

Neutral note that the checked content comes from an entity on the official EU sanctions list. Never a verdict.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `code` | `eu_sanctioned_entity` | tak |  |
| `entity` | `string` | tak |  |
| `basis_url` | `string` (uri) | tak |  |

## CheckResult

The answer every channel renders. The same normalised input within the result cache's lifetime gets the same substantive result on every channel. out_of_scope: an unsupported input type or a request that is not about information. needs_clarification: no claim could be extracted. Any factual claim gets a verdict, "insufficient_evidence" included.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `check_id` | `string` | tak |  |
| `status` | `done` \| `needs_clarification` \| `out_of_scope` \| `technical_failure` | tak |  |
| `claims` | lista: [ClaimResult](#claimresult) |  |  |
| `message` | `string` \| `null` |  | For non-verdict statuses: what to do next. |
| `limitations` | lista: `string` |  |  |
| `source_warning` | [SourceStatusWarning](#sourcestatuswarning) \| `null` |  |  |
| `escalation` | [Escalation](#escalation) \| `null` |  |  |
| `corpus_version` | `string` | tak | Id of the scheduled corpus snapshot. |
| `ai_disclosure` | `True` |  |  |

## CachedResult

What the result cache keeps: only the substantive part of a CheckResult. The key is the normalised input. The entry lives a fixed time, whatever snapshots appear meanwhile. Escalation and the repeat counter are not here: they are computed on every request. A technical failure is never cached.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `status` | `done` \| `needs_clarification` \| `out_of_scope` | tak |  |
| `claims` | lista: [ClaimResult](#claimresult) |  |  |
| `message` | `string` \| `null` |  |  |
| `limitations` | lista: `string` |  |  |
| `source_warning` | [SourceStatusWarning](#sourcestatuswarning) \| `null` |  |  |
| `corpus_version` | `string` | tak |  |
| `source_ids` | lista: `string` |  | Ids of the sources cited in the claims. |
| `cached_at` | `string` (date-time) | tak |  |
| `expires_at` | `string` (date-time) | tak |  |

## AnalysisStep

One step of the processing strip shown between „Sprawdź” and the result.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `code` | `receive` \| `fetch_url` \| `transcribe_audio` \| `screen_injection` \| `extract_claims` \| `search_corpus` \| `search_web` \| `search_fact_checks` \| `assess_evidence` \| `verify_citations` \| `write_answer` \| `save_record` | tak |  |
| `status` | `pending` \| `active` \| `done` \| `skipped` \| `failed` | tak |  |

## AnalysisStatus

Polled (or streamed) by every channel while a check runs; mirrors the DBOS workflow.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `check_id` | `string` | tak |  |
| `steps` | lista: [AnalysisStep](#analysisstep) | tak |  |
| `result` | [CheckResult](#checkresult) \| `null` |  |  |

## InjectionEvent

Instructions found in the input or a source. Logged and never executed. In user content the instruction is cut out and the rest is analysed as data; a catalogue source with an instruction drops out of the evidence.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `location` | `input` \| `source` | tak |  |
| `action` | `instruction_removed` \| `source_dropped` | tak |  |
| `source_url` | `string` (uri) \| `null` |  |  |
| `excerpt` | `string` | tak |  |

## ModelUsage

One model call: provider, model, region of processing, tokens and cost.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `provider` | `string` | tak |  |
| `model` | `string` | tak |  |
| `region` | `string` | tak | Where the data was processed. |
| `input_tokens` | `integer` | tak |  |
| `output_tokens` | `integer` | tak |  |
| `cost_usd` | `number` | tak |  |

## CheckRecord

Audit log of one check (MSZ MVP: question, time, sources, result; plus observability).

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `check_id` | `string` | tak |  |
| `session_id` | `string` | tak | Web and extension: random id kept in the browser session. Discord, SMS, MCP: the salted hash of the channel user id (equal to channel_user_hash). |
| `user_id` | `string` \| `null` |  | Signed-in users only (Google or Microsoft account); None for anonymous checks. |
| `channel` | `web` \| `extension` \| `discord` \| `sms` \| `mcp` | tak |  |
| `channel_user_hash` | `string` \| `null` |  | Discord, SMS and MCP only: salted SHA-256 of the user id, phone number or MCP client id, used to reply and count repeats; never shown to moderators. |
| `received_at` | `string` (date-time) | tak |  |
| `answered_at` | `string` (date-time) | tak |  |
| `question_masked` | `string` | tak | Input with obvious personal data masked. |
| `status` | `done` \| `needs_clarification` \| `out_of_scope` \| `technical_failure` | tak |  |
| `verdicts` | lista: `confirmed` \| `false` \| `misleading` \| `insufficient_evidence` \| `not_verifiable` | tak |  |
| `source_ids` | lista: `string` | tak |  |
| `corpus_version` | `string` | tak |  |
| `models` | lista: [ModelUsage](#modelusage) | tak |  |
| `web_search_calls` | `integer` |  |  |
| `retrieval_errors` | lista: `string` |  |  |
| `injection_events` | lista: [InjectionEvent](#injectionevent) |  |  |
| `escalation` | [Escalation](#escalation) \| `null` |  |  |
| `cache_hit` | `boolean` |  | Substantive part served from the result cache; escalation was still computed. |
| `retention_until` | `string` (date-time) | tak |  |

## CaseClaim

One claim in a case and the checks that asked it: unanswered ("insufficient_evidence"), or disputed by a user.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `claim` | `string` | tak |  |
| `check_ids` | lista: `string` | tak |  |

## ModeratorCase

One case per group of similar unanswered claims. Similarity is measured per claim; a repeated claim joins the case.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `id` | `string` | tak |  |
| `state` | `open` \| `answered` \| `closed` | tak |  |
| `reasons` | lista: `insufficient_evidence` \| `high_risk` \| `repeated_unanswered` \| `user_dispute` | tak |  |
| `high_risk_topic` | `string` \| `null` |  | Topic from the admin's high-risk list that matched. |
| `high_risk_classified_by` | `model` \| `keywords` \| `null` |  | Model classification against the admin list, or the keyword list as a fallback. |
| `summary` | `string` | tak |  |
| `claims` | lista: [CaseClaim](#caseclaim) | tak |  |
| `distinct_askers` | `integer` |  | Distinct sessions or users who asked; raises the case's priority only, never decides whether it exists. |
| `first_seen` | `string` (date-time) | tak |  |
| `last_seen` | `string` (date-time) | tak |  |
| `assignee_role` | `moderator` \| `analyst` |  |  |

## CatalogEntry

One domain in the open source catalogue: why it qualifies, how it is refreshed, whether it is excluded.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `domain` | `string` | tak |  |
| `publisher` | `string` | tak |  |
| `publisher_id` | `string` | tak |  |
| `kind` | `akt_prawny` \| `dane_publiczne` \| `instytucja` \| `fact_check` \| `media` | tak |  |
| `tier` | `primary` \| `secondary` | tak |  |
| `license` | `string` | tak |  |
| `ingest` | `static` \| `rss` \| `sitemap` \| `web_search` \| `mcp` \| `api` | tak | mcp: the local EUvsDisinfo copy; api: Google Fact Check Tools, used only to discover URLs and show the rating as context. |
| `refresh_hours` | `integer` \| `null` |  |  |
| `validity` | `expires` \| `in_force` \| `updated_in_place` \| `past_event` \| `superseded` |  | Age override for every document of this entry; past_event and superseded are set per evidence. |
| `max_age_hours` | `integer` \| `null` |  | Shorter threshold for short-lived sources (warnings, roads, weather: hours or days). |
| `qualified_because` | `string` | tak |  |
| `tdm_reservation` | `none` \| `reserved` \| `unknown` |  | Machine-readable text and data mining opt-out (robots.txt incl. Content-Signal, meta tags, tdmrep), checked per domain. |
| `excluded` | `boolean` |  |  |
| `exclusion_reason` | `string` \| `null` |  |  |

## Notification

An inbox entry, pushed live over SSE or WebSocket from DBOS events and shown as a toast. A toast the recipient did not act on stays in the inbox as unread. Addressed to one browser session or one signed-in user (staff included). Text comes from copy/pl.json by `kind`.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `id` | `string` | tak |  |
| `kind` | `check_progress` \| `check_done` \| `moderator_answer` \| `new_evidence` \| `case_assigned` \| `system` | tak |  |
| `status` | `unread` \| `read` |  |  |
| `session_id` | `string` \| `null` |  |  |
| `user_id` | `string` \| `null` |  |  |
| `check_id` | `string` \| `null` |  |  |
| `case_id` | `string` \| `null` |  |  |
| `link` | `string` | tak | In-app path to open. |
| `created_at` | `string` (date-time) | tak |  |
| `retention_until` | `string` (date-time) | tak |  |
