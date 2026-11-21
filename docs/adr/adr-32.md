# ADR-32. Korpus jako wycinek w istniejących repozytoriach; narzędzie MCP search\_sources

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Zespół rozważał osobne repozytorium do pobierania i przygotowania materiałów organizatora i źródeł z katalogu, z własną bazą danych i wewnętrznym narzędziem MCP. Migawki korpusu i spójność kanałów ([ADR-19](adr-19.md), [ADR-21](adr-21.md)) zakładają jedną bazę PostgreSQL ([ADR-04](adr-04.md)).

## Decyzja

Nie zakładamy osobnego repozytorium. Wycinek corpus: kontrakty i port CorpusSearch w meritum-core, a workflowy pobierania (RSS, mapy stron, import materiałów organizatora i bazy incydentów, kopia EUvsDisinfo z [ADR-26](adr-26.md)) w meritum-worker jako zaplanowane workflowy DBOS. Pobieranie źródeł katalogu nie korzysta z Vertex AI Search ([ADR-07](adr-07.md)). Jeśli scraper potrzebuje ciężkich zależności, np. przeglądarki bez interfejsu dla stron w JavaScript, to samo repozytorium workera buduje drugi obraz worker-ingest. Korpus nie ma osobnych kopii dla dev i prd: jeden wspólny schemat PostgreSQL corpus wypełnia jedno pobieranie, a czytają go oba środowiska. Zapisy sprawdzeń, sprawy i użytkownicy zostają osobno w każdym środowisku. Serwer MCP z [ADR-17](adr-17.md) (FastMCP w backendzie) dostaje drugie narzędzie, search\_sources, nad tym samym portem CorpusSearch, obok „sprawdź twierdzenie”. Agenci badawczy wołają port w tym samym procesie jako narzędzie Pydantic AI; wywołanie przez MCP dodałoby przejście przez sieć, które zabiera czas z budżetu 30 s ([ADR-20](adr-20.md)).

## Konsekwencje

Jedna baza i jeden mechanizm migawek, a inni klienci (jury, inne zespoły) mogą przeszukiwać korpus przez MCP. **Ryzyko:** publiczny dostęp do MCP wymaga kluczy i limitów (jak w [ADR-17](adr-17.md)); pobieranie obciąża workera, dopóki nie wydzielimy obrazu worker-ingest. Migracje wspólnego schematu corpus muszą być zgodne wstecz i uruchamiamy je tylko z gałęzi main.

## Alternatywy

Osobne repozytorium i baza do pobierania z synchronizacją; agenci wołający korpus przez MCP; osobne kopie korpusu dla dev i prd.
