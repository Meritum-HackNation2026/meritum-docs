# ADR-15. Self-hosted runnery GitHub Actions

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

CI potrzebuje mocy do buildów, testów i ewaluacji.

## Decyzja

Trzy runnery organizacji na GCP (etykieta meritum) i runner ARM64 on-prem. Ewaluacja nie biegnie w CI, także w części: przebieg uruchamia się ręcznie albo według harmonogramu ([ADR-28](adr-28.md)).

## Konsekwencje

Szybkie buildy bez limitów minut. **Ryzyko:** host on-prem jest współdzielony z innym projektem.

## Alternatywy

Runnery hostowane przez GitHub.
