# ADR-24. Fact-checkerzy jako domeny katalogu; Fact Check API tylko do znajdowania adresów

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Treść zadania wymaga wiarygodnych źródeł wtórnych. Google Fact Check Tools API zwraca oceny ClaimReview, ale warunki Google APIs nie pozwalają przechowywać danych dłużej, niż mówią nagłówki cache, więc ocena z API nie może być trwałym dowodem w korpusie.

## Decyzja

Fact-checkerów traktujemy jak inne domeny katalogu, ale każdą domenę według jej sygnałów. fakenews.pl i pravda.org.pl (sygnatariusze IFCN, bez blokad, z RSS i mapami strony) pobieramy jako źródła wtórne z własnym publisher\_id. Demagogu i AFP Sprawdzam nie pobieramy, bo blokują automaty (Demagog: 403 dla kanału i mapy strony, Content-Signal: ai-train=no, use=reference); z nich bierzemy tylko adres i ocenę z Fact Check API. Konkret24 wykluczamy, bo nie jest sygnatariuszem IFCN ani członkiem EFCSN, a TVN wymaga umowy licencyjnej. Dla każdej domeny sprawdzamy robots.txt, Content-Signal i zastrzeżenie eksploracji tekstów i danych; źródło wtórne z zastrzeżeniem wypada z katalogu z powodem (CatalogEntry.tdm\_reservation). Fact Check API służy tylko do znajdowania adresów i do pokazania oceny ClaimReview jako kontekstu z linkiem (ClaimResult.claim\_reviews). Zwraca same metadane, bez treści artykułu; ocena nie jest cytatem, nie liczy się do siły, a przechowujemy ją najwyżej tak długo, jak pozwala nagłówek cache (Google APIs Terms, §5(e)). Teksty fact z EUvsDisinfo są cytowalnym dowodem wtórnym (publisher\_id eeas-euvsdisinfo, [ADR-26](adr-26.md)). [ADR-34](adr-34.md) zmienia część o ocenie ClaimReview: ocena fact-checkera z IFCN albo EFCSN może być przesłanką werdyktu.

## Konsekwencje

Cytaty fact-checkerów przechodzą tę samą weryfikację dosłowną co inne źródła i mają datę publikacji. **Ryzyko:** artykuły fact-checkerów są chronione prawem autorskim, więc pokazujemy krótki fragment z linkiem; zastrzeżenie eksploracji może wykluczyć ważne źródło.

## Alternatywy

Fact Check API jako jedyne źródło wtórne; ocena ClaimReview jako dowód.
