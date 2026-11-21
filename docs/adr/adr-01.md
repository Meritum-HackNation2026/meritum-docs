# ADR-01. Pionowe wycinki domenowe z architekturą heksagonalną

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

MSZ wymaga oddzielenia obsługi kanałów od logiki weryfikacji i wymiany modelu lub dostawcy bez przebudowy. Zespół pracuje równolegle nad kilkoma domenami.

## Decyzja

Wycinki: sprawdzanie, korpus, moderacja, zapis przebiegu. Każdy powtarza podfoldery models/, dtos/, ports/, adapters/. Kanały (WWW, wtyczka, Discord, SMS, MCP) to adaptery wejściowe; LLM, wyszukiwarka i baza to adaptery wyjściowe. Granice pilnuje pytestarch.

## Konsekwencje

Nowy kanał albo model to nowy adapter. Domenę testujemy bez sieci. **Ryzyko:** więcej plików na start; testy architektury łapią skróty w CI.

## Alternatywy

Klasyczne warstwy; logika w handlerach kanałów.
