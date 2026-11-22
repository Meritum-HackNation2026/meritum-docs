---
icon: lucide/braces
---

# Kontrakty danych


<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

Wersja kontraktu: `18`. Źródło prawdy to `contracts/meritum.schema.json` w meritum-core, generowany z `meritum_core.checks.contracts` ([ADR-02](../adr/adr-02.md)). Opisy pól są po angielsku, tak jak w kodzie.

| Model | Opis |
|---|---|
| [CheckRequest](#checkrequest) | What a channel adapter sends to the verification core |
| [AiMarker](#aimarker) | Machine-readable marker that an AI system wrote the verdicts and justifications |
| [Citation](#citation) | A fragment of a source and how it bears on the claim |
| [ClaimResult](#claimresult) | One checked claim |
| [ClaimReviewContext](#claimreviewcontext) | A fact-checker's ClaimReview rating found through Google Fact Check Tools API, shown as context with a link |
| [ClaimReviewPremise](#claimreviewpremise) | A fact-checker's ClaimReview rating used as a premise of the verdict, next to the citations (ADR-34) |
| [Escalation](#escalation) | Hand-off to the moderator queue |
| [EvidenceStrength](#evidencestrength) | Strength level together with the premises it follows from. |
| [IncidentMatch](#incidentmatch) | Similarity to a known incident (organiser's database, the local EUvsDisinfo copy or a checked fact-check) |
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
| [EvalCaseResult](#evalcaseresult) | One case of a run: expected and predicted label, outcome, time and cost |
| [EvalLabel](#evallabel) |  |
| [EvalMetrics](#evalmetrics) | The metrics of one run, as the meritum-eval report computes them. |
| [EvalScenarioScore](#evalscenarioscore) | Quality per scenario, so runs on different models compare by scenario. |
| [NonNegative](#nonnegative) |  |
| [Ratio](#ratio) |  |
| [EvalRun](#evalrun) | One evaluation run on the golden set or a staff user's case file. |

## CheckRequest

What a channel adapter sends to the verification core. The core is channel-agnostic.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `channel` | `web` \| `extension` \| `discord` \| `sms` \| `mcp` | tak |  |
| `text` | `string` \| `null` |  |  |
| `url` | `string` (uri) \| `null` |  |  |
| `page_url` | `string` (uri) \| `null` |  | Extension only: the post the text came from. |
| `audio_id` | `string` \| `null` |  | Uploaded audio file or Discord voice message; transcribed in an EU region, then checked like text. |
| `image_id` | `string` \| `null` |  | Uploaded screenshot or photo with text; read by OCR in an EU region, then checked like text. Excludes text, url and audio_id. |
| `channel_user_id` | `string` \| `null` |  | Discord, SMS and MCP only: user id, phone number or MCP client id. The API hashes it with a salt into channel_user_hash and never stores it. |
| `session_id` | `string` \| `null` |  | Web and extension only: random id kept in the browser session; the API copies it to CheckRecord.session_id. |

## AiMarker

Machine-readable marker that an AI system wrote the verdicts and justifications. Every channel gets the same marker from the result; how a channel shows it is up to the channel.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `ai_generated` | `True` |  |  |
| `provider` | `string` | tak |  |
| `model` | `string` | tak |  |
| `generated_at` | `string` (date-time) | tak |  |

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
| `claim_date` | `string` (date) | tak | The date the claim refers to; evidence age is measured against it. |
| `claim_date_source` | `text` \| `input_published_at` \| `today` | tak |  |
| `verdict` | `confirmed` \| `false` \| `misleading` \| `insufficient_evidence` \| `not_verifiable` | tak |  |
| `strength` | [EvidenceStrength](#evidencestrength) \| `null` |  |  |
| `citations` | lista: [Citation](#citation) |  |  |
| `claim_review_premises` | lista: [ClaimReviewPremise](#claimreviewpremise) |  | IFCN or EFCSN fact-checkers' ratings that back the verdict without a page fragment (ADR-34). |
| `explanation` | `string` | tak |  |
| `unresolved` | `string` \| `null` |  | What could not be established. |
| `would_change_verdict` | lista: `needs_primary_source` \| `needs_second_publisher` \| `needs_fresh_evidence` \| `needs_resolving_source` \| `needs_named_source` |  | What would change the verdict, computed by a rule from the premises; the channel words it from copy/pl.json. |
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

## ClaimReviewPremise

A fact-checker's ClaimReview rating used as a premise of the verdict, next to the citations (ADR-34). Found through Google Fact Check Tools API. It has no page fragment: the rating, title, date and link are the evidence. Only publishers the catalogue lists as IFCN or EFCSN signatories qualify; the pipeline copies `signatory_of` from their catalogue entry. Counted per publisher like a secondary-tier citation.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `publisher` | `string` | tak |  |
| `publisher_id` | `string` | tak |  |
| `signatory_of` | lista: `ifcn` \| `efcsn` | tak | IFCN or EFCSN membership from the publisher's catalogue entry; required for a premise. |
| `rating` | `string` | tak | textualRating, verbatim. |
| `title` | `string` | tak |  |
| `reviewed_at` | `string` (date-time) | tak |  |
| `url` | `string` (uri) | tak |  |
| `fetched_at` | `string` (date-time) | tak | When Google Fact Check Tools API returned it. |
| `stance` | `supports` \| `refutes` \| `context` | tak |  |

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

Similarity to a known incident (organiser's database, the local EUvsDisinfo copy or a checked fact-check). Context only. Never a basis for the verdict by itself, and never changes it. An EUvsDisinfo `fact` text is cited as a Citation, not carried here. `domain` is the one explicitly defined warning case: the checked URL is on a domain the incident database lists (for EUvsDisinfo: linksToDisinformation), and the incident's topic matches the claim. A content match needs a matching title, topic and date; the domain alone never makes one. `match_basis` lists what matched and is shown.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `database` | `organiser` \| `euvsdisinfo` \| `fact_check` |  | fact_check: the entry matched an already checked publication. |
| `incident_id` | `string` | tak |  |
| `matched_on` | `content` \| `domain` |  |  |
| `match_basis` | lista: `title` \| `topic` \| `date` \| `domain` | tak | What agreed; shown with the match. |
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
| `signatory_reviews` | `integer` |  | Distinct IFCN/EFCSN fact-checkers (publisher_id) whose ClaimReview rating agrees with the verdict; one is enough for at least moderate strength. |
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
| `kind` | `akt_prawny` \| `dane_publiczne` \| `instytucja` \| `fact_check` \| `media` \| `transcript` | tak |  |
| `tier` | `primary` \| `secondary` | tak |  |
| `published_at` | `string` (date-time) \| `null` |  |  |
| `fetched_at` | `string` (date-time) | tak |  |
| `language` | `string` |  |  |
| `via` | `corpus` \| `rss` \| `web_search` \| `mcp` |  |  |
| `max_age_hours` | `integer` \| `null` |  | Age threshold from the source's catalogue entry (since v14); absent means 365 days. |

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
| `failure_code` | `provider_unavailable` \| `web_search_unavailable` \| `transcription_failed` \| `url_unavailable` \| `not_ready` \| `null` |  | technical_failure only; never names a key or a provider. |
| `out_of_scope_code` | `image` \| `audio` \| `not_informational` \| `null` |  | out_of_scope only: what is not handled; the channel picks the text from copy/pl.json and falls back to the generic one when it is empty. A rejected recording is audio; why it was rejected is in limitation_codes. |
| `limitations` | lista: `string` |  |  |
| `limitation_codes` | lista: `fact_check_unavailable` \| `image_search_not_run` \| `audio_format_unsupported` \| `audio_too_long` \| `image_format_unsupported` \| `image_too_large` \| `corpus_scope` \| `no_publications` |  | Codes of the limitations the channel words from copy/pl.json; they never set the status, though the audio codes explain an out_of_scope recording. Paired with limitations by index: one code per text, same order. |
| `transcript` | `string` \| `null` |  | Audio input only: the automatic transcript, with personal data masked. |
| `image_text` | `string` \| `null` |  | Image input only: the text read from the image, with personal data masked. |
| `source_warning` | [SourceStatusWarning](#sourcestatuswarning) \| `null` |  |  |
| `escalation` | [Escalation](#escalation) \| `null` |  |  |
| `corpus_version` | `string` | tak | Id of the scheduled corpus snapshot. |
| `ai_disclosure` | `True` |  |  |
| `ai_marker` | [AiMarker](#aimarker) \| `null` |  | Machine-readable marker that an AI system wrote the answer (AI Act art. 50(2)); required on a finished check. |

## CachedResult

What the result cache keeps: only the substantive part of a CheckResult. The key is the normalised input. The entry lives a fixed time, whatever snapshots appear meanwhile. Escalation and the repeat counter are not here: they are computed on every request. A technical failure is never cached.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `status` | `done` \| `needs_clarification` \| `out_of_scope` | tak |  |
| `claims` | lista: [ClaimResult](#claimresult) |  |  |
| `message` | `string` \| `null` |  |  |
| `out_of_scope_code` | `image` \| `audio` \| `not_informational` \| `null` |  | out_of_scope only: what is not handled; the channel picks the text from copy/pl.json and falls back to the generic one when it is empty. A rejected recording is audio; why it was rejected is in limitation_codes. |
| `limitations` | lista: `string` |  |  |
| `limitation_codes` | lista: `fact_check_unavailable` \| `image_search_not_run` \| `audio_format_unsupported` \| `audio_too_long` \| `image_format_unsupported` \| `image_too_large` \| `corpus_scope` \| `no_publications` |  | Codes of the limitations the channel words from copy/pl.json; they never set the status, though the audio codes explain an out_of_scope recording. Paired with limitations by index: one code per text, same order. |
| `transcript` | `string` \| `null` |  | Audio input only: the automatic transcript, with personal data masked. |
| `image_text` | `string` \| `null` |  | Image input only: the text read from the image, with personal data masked. |
| `source_warning` | [SourceStatusWarning](#sourcestatuswarning) \| `null` |  |  |
| `ai_marker` | [AiMarker](#aimarker) \| `null` |  | Machine-readable marker that an AI system wrote the answer (AI Act art. 50(2)); required on a finished check. |
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
| `draft` | `string` \| `null` |  | Streamed draft of the answer, personal data masked; a preview, never a verdict. |

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
| `high_risk_classified_by` | `embeddings` \| `keywords` \| `null` |  | Embedding similarity to the admin list above a threshold, or the keyword list as a fallback (ADR-35). |
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
| `kind` | `akt_prawny` \| `dane_publiczne` \| `instytucja` \| `fact_check` \| `media` \| `transcript` | tak |  |
| `kind_by_path` | `object` |  |  |
| `tier` | `primary` \| `secondary` | tak |  |
| `role` | `evidence` \| `source_status` |  | source_status: a list (sanctions, CERT warnings) that ingest skips; a check uses it only for a neutral source-status warning, never as evidence. |
| `license` | `string` | tak |  |
| `ingest` | `static` \| `rss` \| `sitemap` \| `web_search` \| `mcp` \| `api` \| `live` | tak | mcp: the local EUvsDisinfo copy; api: a public API (IMGW, GIOS, Sejm ELI, dane.gov.pl, statistics) ingested into the corpus; live: queried at check time (Fact Check API, short-lived measurements), never in the corpus snapshot. |
| `refresh_minutes` | `integer` \| `null` |  |  |
| `validity` | `expires` \| `in_force` \| `updated_in_place` \| `past_event` \| `superseded` |  | Age override for every document of this entry; past_event and superseded are set per evidence. |
| `max_age_hours` | `integer` \| `null` |  | Shorter threshold for short-lived sources (warnings, roads, weather: hours or days). |
| `qualified_because` | `string` | tak |  |
| `tdm_reservation` | `none` \| `reserved` \| `unknown` |  | Machine-readable text and data mining opt-out (robots.txt incl. Content-Signal, meta tags, tdmrep), checked per domain. |
| `signatory_of` | lista: `ifcn` \| `efcsn` |  | IFCN or EFCSN membership; only such publishers' ClaimReview ratings may be premises (ADR-34). |
| `excluded` | `boolean` |  |  |
| `exclusion_reason` | `string` \| `null` |  |  |
| `disclaimer` | `string` \| `null` |  |  |

## Notification

An inbox entry, pushed live over SSE or WebSocket from DBOS events and shown as a toast. A toast the recipient did not act on stays in the inbox as unread. Addressed to one browser session or one signed-in user (staff included). Text comes from copy/pl.json by `kind`.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `id` | `string` | tak |  |
| `kind` | `check_progress` \| `check_done` \| `moderator_answer` \| `new_evidence` \| `case_assigned` \| `system` \| `eval_run_done` | tak |  |
| `status` | `unread` \| `read` |  |  |
| `session_id` | `string` \| `null` |  |  |
| `user_id` | `string` \| `null` |  |  |
| `check_id` | `string` \| `null` |  |  |
| `case_id` | `string` \| `null` |  |  |
| `step_code` | `receive` \| `fetch_url` \| `transcribe_audio` \| `screen_injection` \| `extract_claims` \| `search_corpus` \| `search_web` \| `search_fact_checks` \| `assess_evidence` \| `verify_citations` \| `write_answer` \| `save_record` \| `null` |  | check_progress only: the finished pipeline step; the text is analysis.steps.<code> in copy/pl.json. |
| `message_code` | `maintenance_planned` \| `service_degraded` \| `service_restored` \| `null` |  | system only: what the message says; the text is notifications.system_message.<code> in copy/pl.json, never free text. |
| `link` | `string` | tak | In-app path to open. |
| `created_at` | `string` (date-time) | tak |  |
| `retention_until` | `string` (date-time) | tak |  |

## EvalCaseResult

One case of a run: expected and predicted label, outcome, time and cost. A state that is not a verdict (technical_failure included) stays the predicted label and falls into one separate error class.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `case_id` | `string` | tak |  |
| `scenario` | `string` | tak |  |
| `check_id` | `string` \| `null` |  |  |
| `expected` | [EvalLabel](#evallabel) | tak |  |
| `predicted` | [EvalLabel](#evallabel) | tak |  |
| `outcome` | `wrong_decisive` \| `non_verdict` \| `wrong_abstention` \| `correct` | tak |  |
| `received_at` | `string` (date-time) | tak |  |
| `answered_at` | `string` (date-time) | tak |  |
| `cost_usd` | [NonNegative](#nonnegative) |  |  |

## EvalLabel

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|

## EvalMetrics

The metrics of one run, as the meritum-eval report computes them.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `cases` | `integer` | tak |  |
| `macro_f1` | `number` | tak |  |
| `citation_coverage` | [Ratio](#ratio) | tak |  |
| `citation_correctness` | [Ratio](#ratio) | tak |  |
| `abstention` | [Ratio](#ratio) | tak |  |
| `robustness` | [Ratio](#ratio) | tak |  |
| `median_seconds` | [NonNegative](#nonnegative) | tak |  |
| `p95_seconds` | [NonNegative](#nonnegative) | tak |  |
| `max_seconds` | [NonNegative](#nonnegative) | tak |  |
| `input_tokens_per_check` | [NonNegative](#nonnegative) | tak |  |
| `output_tokens_per_check` | [NonNegative](#nonnegative) | tak |  |
| `cost_per_check_usd` | [NonNegative](#nonnegative) | tak |  |
| `cost_100_checks_usd` | [NonNegative](#nonnegative) | tak |  |
| `channel_consistency` | [Ratio](#ratio) | tak |  |
| `information_loop` | [Ratio](#ratio) | tak |  |

## EvalScenarioScore

Quality per scenario, so runs on different models compare by scenario.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `scenario` | `string` | tak |  |
| `cases` | `integer` | tak |  |
| `correct` | `integer` | tak |  |
| `accuracy` | `number` | tak |  |

## NonNegative

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|

## Ratio

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|

## EvalRun

One evaluation run on the golden set or a staff user's case file.

| Pole | Typ | Wymagane | Opis |
|---|---|---|---|
| `id` | `string` | tak |  |
| `case_set` | `golden` \| `user_file` | tak |  |
| `case_file` | `string` \| `null` |  |  |
| `status` | `queued` \| `running` \| `done` \| `failed` | tak |  |
| `corpus_version` | `string` | tak |  |
| `user_id` | `string` \| `null` |  |  |
| `models` | lista: `string` |  |  |
| `started_at` | `string` (date-time) | tak |  |
| `finished_at` | `string` (date-time) \| `null` |  |  |
| `metrics` | [EvalMetrics](#evalmetrics) \| `null` |  |  |
| `scenarios` | lista: [EvalScenarioScore](#evalscenarioscore) |  |  |
| `cases` | lista: [EvalCaseResult](#evalcaseresult) |  |  |
