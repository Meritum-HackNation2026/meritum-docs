---
icon: lucide/plug
---

# Porty i adaptery

Kod dzielimy najpierw według domeny, a w każdej domenie stosujemy architekturę heksagonalną ([ADR-01](../adr/adr-01.md)). Wiążące zasady są w skillu `meritum-architecture` w repozytorium zbiorczym (`.claude/skills/meritum-architecture/SKILL.md`). Ta strona je streszcza.

## Pionowe wycinki

Domeny to `checks`, `channels`, `evidence`, `corpus`, `security`, `moderation`, `observability` i `notifications`, a do tego `jobs` (obsługa DBOS) i `shared` tylko dla kodu, którego używają co najmniej trzy domeny. Każda domena ma te same nazwy plików:

```text
src/meritum_core/evidence/
  __init__.py          # publiczne API domeny: tylko re-eksporty
  constants.py
  models.py
  ports.py
  factory.py
  adapters/            # jeden prywatny moduł na dostawcę
    __init__.py
    _vertex.py
    _stub.py
  errors.py
```

Domena importuje inną tylko przez jej pakiet. Prywatne moduły, funkcje i stałe zaczynają się od `_` i nikt spoza pakietu ich nie importuje.

## Porty, adaptery i fabryki

Każda zależność zewnętrzna stoi za portem: model językowy, embeddingi, wyszukiwanie w sieci, transkrypcja, pobieranie stron, magazyn plików, logowanie, wysyłka powiadomień i baza incydentów. Port to `typing.Protocol` w `<domena>/ports.py` (w TypeScripcie `interface` w `ports.ts`) i mówi modelami domeny, nigdy typami SDK dostawcy. Każdy dostawca to adapter w `<domena>/adapters/`. Adapter buduje tylko fabryka w `<domena>/factory.py`, na podstawie ustawień.

```mermaid
flowchart LR
  subgraph in["Adaptery wejściowe (kanały)"]
    web["Formularz WWW"]
    dc["Discord"]
    ext["Wtyczka"]
    mcp["MCP"]
    sms["SMS"]
  end

  subgraph core["Domena: modele, reguły, workflowy"]
    rules["Reguły werdyktu i siły (ADR-05)"]
    ports{{"Porty"}}
  end

  subgraph out["Adaptery wyjściowe"]
    llm["LLM: Vertex AI albo stub"]
    ws["WebSearch: Vertex AI Search, SearXNG"]
    cs["CorpusSearch: PostgreSQL"]
    blob["BlobStore: GCS"]
    jq["JobQueue: DBOSClient"]
  end

  web --> core
  dc --> core
  ext --> core
  mcp --> core
  sms --> core
  ports --> llm
  ports --> ws
  ports --> cs
  ports --> blob
  ports --> jq
```

Diagram pokazuje układ docelowy. Poniższe porty mają już implementacje w [meritum-core](https://github.com/Meritum-HackNation2026/meritum-core/blob/main/README.md). Wybór adaptera zależy od ustawień, więc testy mogą korzystać z atrap bez dostępu do usług zewnętrznych.

| Port | Co obsługuje |
|---|---|
| `LlmPort`, `EmbeddingsPort` | Model językowy zwraca odpowiedź zgodną z modelem Pydantic, a port embeddingów zwraca wektory. Oba mają adapter Vertex AI i stub. |
| `BlobStore` | Port obsługuje pliki audio i obrazy. API zapisuje nagranie i zwraca identyfikator, po którym worker będzie mógł je odczytać do transkrypcji. Port ma adapter lokalnego systemu plików, adapter prywatnego zasobnika GCS i atrapę w pamięci ([ADR-31](../adr/adr-31.md)). |
| `PageFetcherPort`, `PiiGatePort` | Fetcher pobiera publiczne strony HTTP(S) i blokuje adresy wewnętrzne także po przekierowaniu. Maskowanie łączy bramkę PII z regułami dla telefonów, adresów e-mail i numerów PESEL. |
| `JobQueue` | Backend zleca zadania i czyta strumień postępu. Adapter `DbosJobQueue` używa `DBOSClient`, a testy mogą korzystać z `InMemoryJobQueue`. |

Zapisy sprawdzeń, sprawy moderatorów, tematy wysokiego ryzyka i powiadomienia mają osobne porty repozytoriów. API i worker mogą korzystać z adapterów PostgreSQL, a lokalnie i w testach mają do dyspozycji atrapy w pamięci. [Układ bazy i migracje](../wdrozenie.md#migracje) opisuje strona o wdrożeniu.

## Kontrakty w jednym miejscu

Meritum-core utrzymuje kontrakt sprawdzania w `meritum_core.checks.contracts` ([ADR-02](../adr/adr-02.md)). Z niego powstają JSON Schema i typy TypeScript, których kopie odświeżają design system i frontend. Backend i worker przypinają konkretny commit core w `uv.lock` ([ADR-33](../adr/adr-33.md)). Pola dodane w v4 opisuje strona [Sprawdzenie krok po kroku](../jak-dziala/sprawdzenie.md#kontrakt-v4).

`meritum_core.jobs.contracts` ma własne wersjonowanie. Określa nazwy, kolejki oraz wejścia i wyniki workflowów sprawdzania, eskalacji, usuwania danych, raportu gotowości i zadania testowego `ping`.

## Co pilnuje zasad

| Zasada | Kontrola |
|---|---|
| wycinki i prywatne `_nazwy` | pytestarch w `tests/architecture/`, `scripts/check_conventions.py`; w TypeScripcie dependency-cruiser |
| domena nie importuje adapterów ani frameworków | pytestarch `test_hexagonal.py`; dependency-cruiser `adapters-only-from-factory` |
| lintery na pełną moc | ruff z `select = ["ALL"]` i `ty` w trybie strict; Biome i `tsc` w trybie strict |
| docstringi z identyfikatorami funkcji (`US-…`, `F-…`, `ADR-…`) | ruff `D` i `DOC`, `scripts/check_conventions.py`, test JSDoc w TypeScripcie |
| najwyżej 250 linii na plik | `scripts/check_conventions.py`, test długości plików |
| martwy kod i bezpieczeństwo | vulture, bandit, knip |

Wyjątek od reguły jest wąski i zawsze ma powód zapisany obok, w kodzie albo w `pyproject.toml`. Każde repozytorium z kodem opisuje swoje kontrole w `docs/architecture.md`.

W core, backendzie i workerze `uv run behave` uruchamia scenariusze z `features/`. Domyślny przebieg pytest pomija testy z markerem `integration`. Frontend, wtyczka i makiety uruchamiają `node --test` przez `pnpm test`. `tsx` ładuje komponenty TSX, a happy-dom zapewnia DOM.
