# ADR-02. Kontrakty Pydantic jako jedno źródło prawdy i miejsce reguł z treści zadania

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

API, formularz, wtyczka i panel renderują te same dane. Reguły MSZ (cytat przy werdykcie, wstrzymanie się, awaria to nie werdykt) nie mogą zależeć od promptu.

## Decyzja

Źródłem prawdy jest pakiet src/meritum\_core/checks/contracts/ w repozytorium meritum-core, z własnym CONTRACT\_VERSION (osobnym od kontraktu zadań w jobs/contracts.py); schemat niesie go w polu x-contract-version. Kontrakty definiują CheckRequest, CheckResult, CachedResult, ClaimResult, Citation, EvidenceStrength, Escalation, CheckRecord, ModeratorCase, CatalogEntry i Notification. Walidatory wymuszają reguły, a testy pytest w core sprawdzają, czy złe dane są odrzucane. JSON Schema i typy TS generuje tylko core (scripts/generate-contracts.sh, Python i Pydantic przypięte w uv.lock), a job CI contracts sprawdza, czy wygenerowane pliki są aktualne. Design system trzyma kopię w contracts/: sync.sh pobiera ją z core, zapisuje commit źródłowy (SOURCE) i sumy kontrolne (SHA256SUMS), a workflow contracts.yml odrzuca ręczne zmiany kopii. Po zmianie kontraktów na gałęzi main w core workflow otwiera PR z odświeżoną kopią ([ADR-33](adr-33.md)); przy rozbieżności wygrywa core.

## Konsekwencje

Reguły są sprawdzalne testem, a każda aplikacja wie, z której wersji kontraktu korzysta. **Ryzyko:** dopóki nikt nie scali PR z odświeżoną kopią, kopia w design systemie zostaje w tyle; przypomni o tym różnica wersji.

## Alternatywy

Reguły tylko w promptach; ręcznie pisane typy TS.
