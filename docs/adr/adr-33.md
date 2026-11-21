# ADR-33. Przypięcie meritum-core i automatyczne podbicia

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Backend i worker przypinają meritum-core z gałęzi main w uv.lock, więc każda zmiana kontraktu wymaga scalenia w core do main i ręcznych podbić w dwóch repozytoriach. Kopię kontraktów w design systemie odświeża się ręcznie skryptem contracts/sync.sh.

## Decyzja

Backend i worker przypinają meritum-core do konkretnego commitu (rev w pyproject.toml i uv.lock); na develop jest to commit z gałęzi develop w core. Workflow bump-dependents.yml w meritum-core uruchamia scripts/open-bump-prs.sh po każdym pushu do develop, który zmienia src/, contracts/ albo pyproject.toml. Skrypt ustawia rev w backendzie i workerze, uruchamia uv lock i otwiera albo aktualizuje PR na stałej gałęzi chore/bump-core. Gdy zmieniły się kontrakty, otwiera też PR w design systemie z kopią kontraktów (ten sam wynik co contracts/sync.sh). Te PR tylko podbijają wersję: CI nie uruchamia testów e2e ani testów między komponentami. Workflow potrzebuje sekretu repozytorium MERITUM\_BOT\_TOKEN (fine-grained token); bez niego tylko ostrzega. Przy promocji core trafia do main przed backendem i workerem, a develop łączymy z main commitami scalającymi, więc przypięty commit jest już osiągalny z main. Wdrożenie: meritum-core \#9, meritum-backend \#7, meritum-worker \#5.

## Konsekwencje

Zmiana kontraktu trafia do zależnych repozytoriów bez ręcznych podbić, a każda wersja backendu i workera wskazuje dokładny commit core. **Ryzyko:** token z prawem zapisu do innych repozytoriów trzeba utrzymać jako sekret, a bez niego PR z podbiciem nie powstają. Jeśli backend albo worker trafi do main przed core, przypiętego commitu nie będzie jeszcze w main.

## Alternatywy

Przypięcie do gałęzi (main albo develop); ręczne podbicia; jedno repozytorium Pythona (uv workspace) dla core, backendu i workera.
