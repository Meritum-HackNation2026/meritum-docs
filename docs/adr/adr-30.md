# ADR-30. Weryfikacja nagrań: transkrypcja w regionie UE

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Treść zadania premiuje weryfikację dźwięku i wymaga ujawnienia kosztu, zakresu, retencji i ograniczeń zewnętrznego API dźwięku. Wiele plotek krąży jako wiadomości głosowe.

## Decyzja

Plik audio z formularza i wiadomość głosowa z Discorda (CheckRequest.audio\_id) idą do transkrypcji Google Speech-to-Text v2 z modelem Chirp 3 w multi-regionie eu (pl-PL w GA), za portem, tak jak model i wyszukiwarka. Cennik Standard to 0,016 USD za minutę; czy chirp\_3 jest tak rozliczany, nie potwierdziliśmy. Tryb dynamic batch (0,003 USD za minutę) nie zmieści się w 30 s. Transkrypcję maskujemy jak tekst i sprawdzamy zwykłą ścieżką; karta pokazuje ją z informacją, że powstała automatycznie. README podaje dostawcę, region, koszt, retencję i limity. Awaria transkrypcji daje technical\_failure. Obraz (OCR, metadane, wyszukiwanie wcześniejszych wystąpień) zostaje w priorytecie „Jeśli starczy czasu”.

## Konsekwencje

Obywatel sprawdzi to, co usłyszał, tą samą ścieżką co tekst. **Ryzyko:** błąd transkrypcji zmienia twierdzenie, dlatego pokazujemy transkrypcję; dłuższe nagranie wydłuża sprawdzenie ponad cel 30 s, który dotyczy tekstu i linku.

## Alternatywy

Transkrypcja po hackathonie; model multimodalny bez osobnej transkrypcji.
