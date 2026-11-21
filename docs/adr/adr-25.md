# ADR-25. Dowód zastąpiony; rozbieżność tylko między dowodami ważnymi w dacie twierdzenia

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Starszy dowód wspierający i nowszy obalający (np. uchylony przepis i nowy) dawały „sprzeczne źródła”, czyli „brak wystarczających dowodów”, choć stan na dzień twierdzenia jest jasny.

## Decyzja

Nowa ważność dowodu: superseded, ustawiana dla pojedynczego cytatu deterministyczną regułą w kodzie, bez oceny modelu. Dowód A jest zastąpiony przez B w dacie twierdzenia, gdy mają ten sam publisher\_id i tę samą serię, a B jest nowszy i nie późniejszy niż data twierdzenia; gdy akt prawny jest w ISAP albo ELI uchylony lub zmieniony, a nowsze brzmienie obowiązuje w tej dacie; albo gdy B jest jawną korektą A. Różne liczby od różnych wydawców to nie zastąpienie. Krok oceny wymowy dostaje z bazy datę twierdzenia, datę publikacji źródła i ważność (same metadane, bez treści innych źródeł). Rozbieżność liczymy tylko między dowodami ważnymi w dacie twierdzenia. Dowód zastąpiony nie liczy się do siły, a karta pokazuje go na osi czasu. Kontrakt przyjmuje go tylko obok nowszego dowodu. Test: starszy dowód wspierający i nowszy urzędowy obalający dają „fałszywe” albo „wprowadzające w błąd” z techniką „nieaktualna informacja”.

## Konsekwencje

Werdykt odpowiada stanowi na dzień twierdzenia, a czytelnik widzi, co się zmieniło. **Ryzyko:** reguła nie złapie zastąpienia, którego nie widać w metadanych (np. inna seria albo brak daty); takie przypadki zostają sprzecznością i pilnują ich przypadki scenariusza C w golden secie.

## Alternatywy

Każda para wspierający i obalający jako sprzeczność; ręczne oznaczanie w katalogu.
