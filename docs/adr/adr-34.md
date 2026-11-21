# ADR-34. Ocena ClaimReview fact-checkera jako przesłanka werdyktu

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Materiał organizatora z przykładowymi pytaniami i odpowiedziami dla scenariuszy A–J opiera werdykty na ocenach Demagoga z indeksu Google Fact Check, np. „Nie. Demagog ocenił twierdzenie jako fałsz” z linkiem. Według [ADR-24](adr-24.md) ocena ClaimReview była tylko kontekstem, więc w takich przypadkach odpowiadalibyśmy „brak wystarczających dowodów”, a jury oczekuje rozstrzygnięcia. Stron Demagogu nie pobieramy: robots.txt podaje Content-Signal use=reference i ai-train=no, a licencja wymaga oznaczenia autora i źródła.

## Decyzja

Ocena ClaimReview fact-checkera z IFCN albo EFCSN, znaleziona przez Fact Check API, może być przesłanką werdyktu rozstrzygającego. Cytatem jest nazwa fact-checkera, ocena dosłownie tak, jak ją opublikował (textualRating), tytuł, data i link, bez fragmentu jego strony; weryfikacja dosłowna ([ADR-06](adr-06.md)) porównuje ocenę z odpowiedzią API. Wymowę oceny ustala w kodzie tabela ocen każdego fact-checkera w katalogu (np. „Prawda” wspiera, „Fałsz” obala, „Manipulacja” i „Częściowa prawda” dają kontekst); ocena spoza tabeli zostaje kontekstem. Ocena liczy się tylko wtedy, gdy oceniane twierdzenie (claimReviewed) zgadza się z naszym co do tematu, liczb i daty; sprawdza to krok oceny wymowy. Do siły liczy się jak jeden wydawca wtórny według reguły z [ADR-05](adr-05.md), więc sama daje siłę „słaba”. Odpowiedź mówi, kto ocenił („Według Demagoga …”). Jeśli źródło pierwotne (np. depesza PAP) jest w korpusie albo w wynikach wyszukiwania, cytujemy je obok oceny. Gdy Fact Check API zawiedzie, sprawdzenie kończy się bez tej przesłanki, a ograniczenia mówią, że indeksu nie dało się sprawdzić z powodu błędu dostępu, nigdy że oceny nie ma (scenariusz J). Decyzja zastępuje część [ADR-24](adr-24.md) o ocenie ClaimReview jako samym kontekście i wymaga zmiany kontraktów w meritum-core (wersja 4), żeby przesłankę z oceny ClaimReview dało się zacytować bez fragmentu strony.

## Konsekwencje

Odpowiadamy tak, jak oczekuje materiał organizatora, a licencję i robots.txt Demagogu szanujemy, bo nie pobieramy jego stron. **Ryzyko:** fact-checker ocenia twierdzenie we własnym sformułowaniu, więc złe dopasowanie do naszego twierdzenia daje błędny werdykt; sprawdzamy to w golden secie w obu wariantach scenariusza I. Ocena zapisana w zapisie przebiegu może żyć dłużej, niż pozwalają nagłówki cache Fact Check API (załącznik B).

## Alternatywy

Ocena ClaimReview tylko jako kontekst ([ADR-24](adr-24.md)); pobieranie stron Demagogu wbrew Content-Signal.
