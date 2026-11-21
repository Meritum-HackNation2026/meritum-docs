# ADR-09. Wtyczka Chrome MV3: widżety w Shadow DOM ze skórkami platform

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Widżet trafia do cudzych feedów w trybie jasnym i ciemnym; style nie mogą przeciekać w żadną stronę.

## Decyzja

Każdy widżet renderuje się w Shadow DOM. Skórka platformy zmienia krój, promień, tło, obramowanie, przyciski i linki; znak, werdykt i blok źródeł są stałe. Zapytania do API idą przez background.js.

## Konsekwencje

Izolacja stylów i jeden komponent na pięć platform. **Ryzyko:** zmiany DOM platform; łagodzi to kontrakt selektorów ([ADR-10](adr-10.md)).

## Alternatywy

Iframe na widżet; style globalne z prefiksem.
