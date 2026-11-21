# ADR-33. Przypięcie meritum-core i automatyczne podbicia

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Backend i worker przypinają meritum-core z gałęzi main w uv.lock, więc każda zmiana kontraktu wymaga scalenia w core do main i ręcznych podbić w dwóch repozytoriach. Kopię kontraktów w design systemie odświeża się ręcznie skryptem contracts/sync.sh.

## Decyzja

Backend i worker przypinają meritum-core do konkretnego commitu (rev w pyproject.toml i uv.lock); jest to commit z gałęzi main w core, bo core nie ma gałęzi develop. Workflow bump-dependents.yml w meritum-core uruchamia scripts/open-bump-prs.sh po każdym pushu do main, który zmienia src/, contracts/ albo pyproject.toml. Skrypt ustawia rev w backendzie i workerze, uruchamia uv lock i otwiera albo aktualizuje PR do develop na stałej gałęzi chore/bump-core. Gdy zmieniły się kontrakty, otwiera też PR w design systemie z kopią kontraktów (ten sam wynik co contracts/sync.sh). Te PR tylko podbijają wersję: CI nie uruchamia testów e2e ani testów między komponentami. Workflow potrzebuje sekretu repozytorium MERITUM\_BOT\_TOKEN (fine-grained token); bez niego tylko ostrzega. Przypięty commit jest więc na main w core, zanim backend albo worker wyda develop do main. Wdrożenie: meritum-core \#9, meritum-backend \#7, meritum-worker \#5.

## Konsekwencje

Zmiana kontraktu trafia do zależnych repozytoriów bez ręcznych podbić, a każda wersja backendu i workera wskazuje dokładny commit core. **Ryzyko:** token z prawem zapisu do innych repozytoriów trzeba utrzymać jako sekret, a bez niego PR z podbiciem nie powstają.

## Alternatywy

Przypięcie do gałęzi main bez konkretnego commitu; ręczne podbicia; jedno repozytorium Pythona (uv workspace) dla core, backendu i workera.
