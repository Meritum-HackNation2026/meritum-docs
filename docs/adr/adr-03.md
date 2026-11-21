# ADR-03. DBOS dla workflowu sprawdzania i cyklicznego pobierania źródeł

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Sprawdzenie ma kilka kroków z wywołaniami zewnętrznymi, które mogą zawieść. Korpus musi się odświeżać sam.

## Decyzja

Każde sprawdzenie to workflow DBOS z krokami AnalysisStep, a kroki badań biegną równolegle ([ADR-20](adr-20.md)); kanały odczytują AnalysisStatus strumieniem. Pobieranie RSS i usuwanie danych po retencji to zaplanowane workflowy DBOS. Workflowami są też synchronizacja kopii EUvsDisinfo ([ADR-26](adr-26.md)) i przebiegi ewaluacji ([ADR-28](adr-28.md)), a zdarzenia workflowów zasilają powiadomienia ([ADR-29](adr-29.md)).

## Konsekwencje

Restart nie gubi sprawdzeń; kroki są ponawiane, stan w PostgreSQL. **Ryzyko:** kroki muszą być idempotentne.

## Alternatywy

Celery z Redisem; Cloud Tasks; cron poza aplikacją.
