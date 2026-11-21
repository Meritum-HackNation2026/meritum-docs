# ADR-28. Ewaluacja w pydantic-evals poza CI, ze stroną ewaluacji w aplikacji

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Pełna ewaluacja woła modele i wyszukiwarkę, więc kosztuje i trwa. Analityk ma śledzić jakość bez terminala, a jury może chcieć dodać własny plik.

## Decyzja

Ewaluację prowadzi pydantic-evals. Nie biegnie w CI, także w części: przebieg uruchamia się ręcznie, ze strony ewaluacji albo według harmonogramu, poza sprawdzeniami CI w PR. Strona w aplikacji WWW, za logowaniem dla ról analityk i administrator, pokazuje historię przebiegów z miernikami i wynikami przypadków, uruchamia przebieg na golden secie, przyjmuje inny zestaw w formacie przypadków (JSON albo CSV) i porównuje przebiegi. Przebieg działa asynchronicznie w workerze jako workflow DBOS i zapisuje wyniki w bazie.

## Konsekwencje

CI zostaje szybki i tani, a historia jakości jest w jednym miejscu. **Ryzyko:** spadek jakości wykryje dopiero przebieg ręczny albo z harmonogramu, a nie sprawdzenie PR.

## Alternatywy

Pełna ewaluacja w każdym CI; podzbiór dymny w CI; tylko skrypt w terminalu.
