---
icon: lucide/blocks
---

# Komponenty

Każde repozytorium z kodem opisuje swoje moduły w README i w `docs/architecture.md`. Ta strona zbiera je w jednym miejscu. Zasady podziału na domeny są w [Porty i adaptery](porty-i-adaptery.md), a [Mapa repozytoriów](repozytoria.md) listuje całą organizację.

## meritum-core

Biblioteka wspólna backendu i workera oraz jedyne źródło prawdy kontraktów. Nie zawiera aplikacji.

| Moduł | Co robi |
|---|---|
| `checks.contracts` | kontrakt sprawdzania (wersja 18), walidacja reguł z treści zadania, `AiMarker`, `CachedResult` |
| `jobs` | kontrakt zadań, port `JobQueue`, adapter `DbosJobQueue`, kolejka w pamięci do testów |
| `shared.llm` | port `LlmPort` z narzędziami i wywołaniami narzędzi, adaptery OpenRouter, Vertex AI i stub |
| `shared.blobs` | port `BlobStore`; adaptery: system plików, prywatny bucket GCS, magazyn zgodny z S3, pamięć |
| `corpus` | wyszukiwanie hybrydowe, katalog źródeł w YAML, fetcher stron z ochroną SSRF, wyszukiwanie na żywo, migracje schematu `corpus` |
| `checks.ocr`, `checks.transcription` | porty OCR obrazów i transkrypcji nagrań |
| `security` | maskowanie danych osobowych i detektor wstrzyknięć z bramką za portem |
| `evidence` | reguły siły podstawy, wieku dowodu, rozbieżności i „co zmieniłoby werdykt” |
| `moderation`, `notifications`, `observability` | porty repozytoriów, usuwanie danych osoby (`SubjectEraser`), migracje schematu aplikacji |

## meritum-backend

API w FastAPI. Moduły według domen: `checks` (sprawdzenia, strumień zdarzeń, nagrania, obrazy, historia konta), `channels` (skrót identyfikatora kanału), `discord` (interakcje i proces Gateway), `sms` (webhook bramki), `mcp` (serwer MCP), `auth` (OIDC Google i Microsoft), `staff` (konta i role), `moderation` (sprawy, przekazania, odpowiedzi), `notifications` (skrzynka SSE, cele zewnętrzne), `export` (JSON, CSV, STIX 2.1), `evaluation` (przebiegi, zestawy, porównania), `jury` (jednorazowe linki), `privacy` (usuwanie danych), `limits` (limity zapytań w bazie), `health` (test gotowości). Backend nie ma własnej logiki weryfikacji: wszystkie kanały wołają jedną funkcję `start_check`.

## meritum-worker

Workflowy DBOS. Moduły według domen: `checks` (workflow `check`, krok po kroku), `evidence` (ocena wymowy cytatów, dopasowanie do znanych incydentów, ostrzeżenie o liście sankcji UE), `corpus` (wczytywanie katalogu, migawki, wyszukiwanie na żywo, fact-checkerzy, kopia EUvsDisinfo, archiwizacja stron, reranker), `moderation` (sprawy i grupowanie), `security` (retencja, usuwanie danych, bramka wstrzyknięć), `observability` (gotowość, ewaluacja, porównania modeli i kosztów). Workflowy zaplanowane: `retention` co godzinę, `corpus_ingest` co 15 minut, `corpus_snapshot` co godzinę, na prd z włączonym `MERITUM_CORPUS_INGEST`.

## meritum-frontend

Aplikacja React z trasami w plikach: strona główna, `sprawdzenie` (wynik), `odpowiedzi` (odpowiedź moderatora dla pytającego), `panel` (kolejka spraw, konta, tematy, eksport FIMI, ewaluacja, `jury`), `prywatnosc` i `jak-dziala`. Klient API powstaje z kopii schematu OpenAPI backendu (openapi-typescript, openapi-fetch, openapi-react-query), formularz waliduje zod, stan trzyma zustand, tabele TanStack Table. Komponenty pochodzą z design systemu, a potem z darmowych bloków shadcnblocks, ReUI, Origin UI i zwykłego shadcn/ui, w tej kolejności.

## Pozostałe repozytoria

| Repozytorium | Zawartość |
|---|---|
| meritum-extension | wtyczka Chrome MV3 (WXT, React) z widżetem w Shadow DOM i skórkami platform |
| meritum-mocks | makiety platform i makieta Discorda w Hono, wołające to samo API co prawdziwy bot |
| meritum-design-system | dokument produktowy, tokeny, komponenty, teksty `copy/pl.json` i `copy/privacy.json`, kopie kontraktów, rejestr podmiotów przetwarzających |
| meritum-infra | platforma na serwerze zespołu (PostgreSQL, gateway, trasy Cloudflare), runnery CI, Terraform dla GCP, Worker e-mail do moderatorów |
| meritum-monorepo | submoduły, `docker-compose.yml`, skrypty pomiaru kosztów i testu dymnego |
| meritum-docs | ta strona |

Wygląd aplikacji, wtyczki i makiet wynika z jednego design systemu: nowy kierunek wizualny zastąpił generyczny szablon, a werdykt stoi na początku karty, cytat jest dowodem, a stany niebędące werdyktem mają własne karty ([Werdykty i reguły](../jak-dziala/werdykty.md)).
