# ADR-21. Dowody z wyszukiwania na żywo w bieżącym sprawdzeniu

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Wcześniej strona z wyszukiwania na żywo czekała na następną migawkę korpusu, więc wyszukiwanie nie pomagało w odpowiedzi, dla której je uruchomiliśmy. Przy świeżych wydarzeniach to właśnie ta odpowiedź potrzebuje nowych dowodów.

## Decyzja

Strona pobrana przez wyszukiwanie na żywo, po skanie pod kątem wstrzykniętych poleceń, jest dowodem w tym samym sprawdzeniu i trafia do CheckRecord (source\_ids, Source.via = web\_search). Do wspólnego korpusu dołącza z następną migawką. Wyszukiwanie zawsze biegnie równolegle z wyszukiwaniem w korpusie; próg wyszukiwania decyduje tylko o tym, czy czekamy na jego wynik. Spójność między kanałami zapewnia pamięć wyników ([ADR-19](adr-19.md), [ADR-22](adr-22.md)).

## Konsekwencje

Świeże dowody już w bieżącej odpowiedzi, a zapis przebiegu pozwala ją odtworzyć. **Ryzyko:** dwa równoczesne pytania o to samo, zanim pierwszy wynik trafi do pamięci, mogą dostać różne strony z wyszukiwania; wyszukiwanie przy każdym sprawdzeniu podnosi koszt.

## Alternatywy

Strony dołączają dopiero z następną migawką (wyszukiwanie nie pomaga w bieżącej odpowiedzi); nowa migawka po każdym sprawdzeniu.
