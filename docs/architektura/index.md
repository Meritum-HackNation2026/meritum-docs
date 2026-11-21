---
icon: lucide/boxes
---

# Kontekst i kontenery

Diagramy idą za modelem C4: najpierw system wśród ludzi i usług zewnętrznych, potem kontenery w środku. Opisują stan docelowy z dokumentu produktowego. Dziś działa szkielet: frontend, API z kanałem Discord, worker z workflowem `ping`, makiety i PostgreSQL ([stan prac](../index.md#stan-prac)).

## Kontekst systemu

```mermaid
flowchart LR
  citizen(["Obywatel"])
  mod(["Moderator, analityk, administrator"])
  jury(["Jury MSZ"])

  subgraph meritum["Meritum"]
    sys["Rdzeń weryfikacji z kanałami: formularz WWW, Discord, wtyczka, MCP"]
  end

  discord["Discord"]
  vertex["Vertex AI: modele i embeddingi"]
  search["Wyszukiwanie na żywo w domenach katalogu"]
  sources["Źródła z katalogu: gov.pl, ISAP, EUR-Lex, dane.gov.pl, BIP, fact-checkerzy"]
  fcapi["Google Fact Check Tools API"]
  euvs["EUvsDisinfo: lokalna kopia"]
  cf["Cloudflare: tunel, TLS, ochrona przed DDoS"]

  citizen -->|"wkleja tekst albo link"| cf
  jury -->|"formularz i makieta Discorda"| cf
  mod -->|"panel moderatora"| cf
  cf --> sys
  citizen -->|"/sprawdz"| discord
  discord -->|"interakcje HTTP"| cf
  sys -->|"zamaskowane twierdzenia i fragmenty"| vertex
  sys -->|"zapytania z twierdzeń"| search
  sys -->|"RSS, mapy stron, pobieranie"| sources
  sys -->|"szukanie ocen ClaimReview"| fcapi
  sys -->|"synchronizacja"| euvs
```

Kto przetwarza jakie dane i gdzie, opisuje strona [Prywatność](../prywatnosc.md).

## Kontenery

```mermaid
flowchart TB
  user(["Użytkownik"])
  cf["Cloudflare"]

  subgraph host["Serwer zespołu dziś, docelowo GCP europe-central2"]
    gw["meritum-gateway (nginx)"]
    web["meritum-web: React, nginx, przekazuje /api"]
    api["meritum-api: FastAPI, kanały WWW, Discord, MCP"]
    worker["meritum-worker: workflowy DBOS"]
    mocks["meritum-mocks: makiety platform (Hono)"]
    db[("meritum-postgres: PostgreSQL, pgvector, pg_trgm, słownik polski")]
  end

  ext["Wtyczka Chrome (MV3)"]
  llm["Vertex AI"]

  user --> cf --> gw
  gw --> web
  gw --> mocks
  web -->|"/api"| api
  ext -->|"to samo API"| cf
  api -->|"JobQueue przez DBOSClient"| db
  worker -->|"kolejki i tabele DBOS"| db
  api -->|"swój schemat"| db
  mocks -->|"swój schemat"| db
  worker --> llm
```

| Kontener | Repozytorium | Co robi |
|---|---|---|
| `meritum-web-<env>` | meritum-frontend | statyczny build aplikacji w nginx; `/api` idzie do API tego samego środowiska |
| `meritum-api-<env>` | meritum-backend | FastAPI: health, zlecanie zadań, kanał Discord, dokumentacja OpenAPI |
| `meritum-worker-<env>` | meritum-worker | trwałe workflowy DBOS: sprawdzenie, pobieranie źródeł, retencja, ewaluacja |
| `meritum-mocks-<env>` | meritum-mocks | makiety X, Facebooka, Instagrama, Reddita i TikToka; wybór po nagłówku `Host` |
| `meritum-postgres` | meritum-infra | jedna baza `meritum` dla wszystkich; każda aplikacja i środowisko ma własną rolę i schemat |
| `meritum-gateway` | meritum-infra | nginx platformy, który kieruje adresy `meritum(-*).gburek.app` do kontenerów |

API nie wywołuje workera bezpośrednio. Zleca zadania przez port `JobQueue` z meritum-core, a worker wykonuje je jako workflowy DBOS o nazwie i kolejce z `WorkflowSpec`. Argument i wynik workflowu to jeden obiekt JSON, więc żadna strona nie potrzebuje klas drugiej. Worker przyjmuje tylko zadania ze swoim `application_version` (`dev`, `prd`, lokalnie `local`), więc środowiska nie podbierają sobie pracy.

## Dalej

- [Porty i adaptery](porty-i-adaptery.md): jak domeny są podzielone i co egzekwują testy architektury.
- [Mapa repozytoriów](repozytoria.md): wszystkie repozytoria organizacji.
- [Kontrakty danych](../referencja/kontrakty.md): modele, które wymieniają kanały, API i worker.
