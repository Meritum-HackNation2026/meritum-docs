# ADR-27. Odtwarzalna ewaluacja: przypięta migawka, nagrane odpowiedzi dostawców, publiczny manifest

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Treść zadania wymaga wyników z danymi do odtworzenia. Korpus rośnie, wyszukiwanie na żywo zwraca za każdym razem coś innego, a jury może nie mieć kluczy.

## Decyzja

Tryb ewaluacji przypina corpus\_version i odtwarza nagrane odpowiedzi dostawców modelu i wyszukiwania (kasety), więc przebieg powtarza się bez kluczy i bez sieci. Publikujemy pliki przypadków, adresy źródeł, cytowane fragmenty i manifest migawki z identyfikatorami dokumentów, sumami kontrolnymi i fetched\_at. Pełnych tekstów nie publikujemy; kasety zawierają pełne teksty stron, więc zostają poza paczką. Migawkę odtwarza się ponownym pobraniem i porównaniem sum kontrolnych.

## Konsekwencje

Każdy może sprawdzić nasze liczby, a my nie rozpowszechniamy cudzych tekstów. **Ryzyko:** strona zmieniona od pobrania nie przejdzie porównania sum i trzeba ją wyłączyć z porównania; po zmianie promptu albo modelu kasety nagrywamy od nowa.

## Alternatywy

Publikacja pełnej migawki korpusu; ewaluacja tylko na żywo.
