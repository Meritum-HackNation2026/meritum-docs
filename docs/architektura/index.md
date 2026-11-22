---
icon: lucide/boxes
---

# Kontekst i kontenery

Diagramy C4 pokazują otoczenie systemu i jego kontenery. Opisują stan na gałęzi `develop`; środowisko prd dostaje je po promocji do `main`. Przepływ danych krok po kroku jest na stronie [Przepływ danych](przeplyw-danych.md), kod każdego kontenera w [Komponenty](komponenty.md), a kontrakty i porty w [Porty i adaptery](porty-i-adaptery.md).

## Kontekst systemu

```mermaid
flowchart LR
  citizen(["Obywatel"])
  mod(["Moderator, analityk, administrator"])
  jury(["Jury MSZ"])
  chat(["Aplikacje czatu z konektorem MCP"])

  subgraph meritum["Meritum"]
    sys["Rdzeń weryfikacji z kanałami: formularz WWW, Discord, SMS, wtyczka, MCP"]
  end

  discord["Discord"]
  sms["Bramka SMS: sms-gate.app i telefon zespołu"]
  llm["Model językowy: Claude Haiku 5.5 przez OpenRouter"]
  gcp["Google Cloud w UE: embeddingi, transkrypcja, OCR, maskowanie danych, bramka wstrzyknięć"]
  search["Wyszukiwanie na żywo w domenach katalogu"]
  sources["Źródła z katalogu: gov.pl, ISAP, EUR-Lex, dane.gov.pl, BIP, fact-checkerzy"]
  fcapi["Google Fact Check Tools API"]
  euvs["EUvsDisinfo: lokalna kopia"]
  idp["Google i Microsoft: logowanie"]
  cf["Cloudflare: tunel, TLS, ochrona przed DDoS"]

  citizen -->|"tekst, link, nagranie, zrzut ekranu"| cf
  jury -->|"formularz i makieta Discorda"| cf
  mod -->|"panel"| cf
  chat -->|"/mcp"| cf
  cf --> sys
  citizen -->|"/sprawdz, wzmianka, wiadomość prywatna"| discord
  discord -->|"interakcje HTTP i Gateway"| sys
  citizen -->|"SMS"| sms
  sms -->|"webhook"| cf
  sys -->|"zamaskowane twierdzenia i fragmenty"| llm
  sys --> gcp
  sys -->|"zapytania z twierdzeń"| search
  sys -->|"RSS, mapy stron, pobieranie"| sources
  sys -->|"oceny ClaimReview"| fcapi
  sys -->|"synchronizacja"| euvs
  sys -->|"OIDC"| idp
```

Kto przetwarza jakie dane i gdzie, opisuje strona [Prywatność](../prywatnosc.md).

## Kontenery

```mermaid
flowchart TB
  user(["Użytkownik"])
  cf["Cloudflare"]

  subgraph host["Serwer zespołu dziś, docelowo GCP europe-central2"]
    gw["meritum-gateway (nginx)"]
    web["meritum-web: React, nginx, przekazuje /api i /mcp"]
    api["meritum-api: FastAPI, kanały WWW, Discord, SMS, MCP, panel"]
    dcgw["meritum-discord: proces Gateway Discorda"]
    worker["meritum-worker: workflowy DBOS"]
    mocks["meritum-mocks: makiety platform i Discorda (Hono)"]
    db[("meritum-postgres: PostgreSQL, pgvector, pg_trgm, słownik polski")]
    files[("wolumen plików: nagrania i obrazy")]
  end

  ext["Wtyczka Chrome (MV3)"]
  llm["OpenRouter: model językowy"]

  user --> cf --> gw
  gw --> web
  gw --> mocks
  web -->|"/api, /mcp"| api
  ext -->|"to samo API"| cf
  dcgw -->|"te same porty co API"| db
  api -->|"JobQueue przez DBOSClient"| db
  worker -->|"kolejki i tabele DBOS"| db
  api -->|"schemat aplikacji"| db
  worker -->|"ten sam schemat aplikacji"| db
  api --> files
  worker --> files
  mocks -->|"swój schemat"| db
  worker --> llm
```

| Kontener | Repozytorium | Co robi |
|---|---|---|
| `meritum-web-<env>` | meritum-frontend | statyczny build aplikacji w nginx; `/api` i `/mcp` idą do API tego samego środowiska |
| `meritum-api-<env>` | meritum-backend | FastAPI: sprawdzenia, strumień postępu, nagrania i obrazy, kanały Discord, SMS i MCP, logowanie, panel personelu, powiadomienia, eksport, API ewaluacji, dokumentacja OpenAPI |
| `meritum-discord-<env>` | meritum-backend | proces Gateway Discorda (wzmianki i wiadomości prywatne); startuje tylko, gdy środowisko ma token bota |
| `meritum-worker-<env>` | meritum-worker | trwałe workflowy DBOS: sprawdzenie, sprawy moderatora, usuwanie danych, retencja, wczytywanie korpusu, ewaluacja, archiwizacja stron |
| `meritum-mocks-prd` | meritum-mocks | makiety X, Facebooka, Instagrama, Reddita i TikToka oraz makieta Discorda dla jury, wybierane według nagłówka `Host` |
| `meritum-postgres` | meritum-infra | jedna instancja PostgreSQL z bazą aplikacji `meritum` i osobną bazą DBOS dla każdego środowiska |
| `meritum-gateway` | meritum-infra | nginx platformy, który kieruje adresy `meritum(-*).gburek.app` do kontenerów |

API nie wywołuje workera bezpośrednio. Zleca zadania przez port `JobQueue` z meritum-core, a worker wykonuje je jako workflowy DBOS o nazwie i kolejce z `WorkflowSpec`. Argument i wynik workflowu to jeden obiekt JSON, więc żadna strona nie potrzebuje klas drugiej. Worker przyjmuje tylko zadania ze swoim `application_version` (`dev`, `prd`, lokalnie `local`), więc środowiska nie podbierają sobie pracy. Nagrania i obrazy leżą na wolumenie plików wspólnym dla API i workera danego środowiska (`BlobStore`), a docelowo w prywatnym buckecie Cloud Storage.

## Dalej

- [Przepływ danych](przeplyw-danych.md): co dzieje się z pytaniem od kanału do wyniku.
- [Komponenty](komponenty.md): moduły backendu, workera, frontendu i pozostałych repozytoriów.
- [Porty i adaptery](porty-i-adaptery.md): jak domeny są podzielone i co egzekwują testy architektury.
- [Mapa repozytoriów](repozytoria.md): wszystkie repozytoria organizacji.
- [Kontrakty danych](../referencja/kontrakty.md): modele, które wymieniają kanały, API i worker.
