# ADR-22. Pamięć wyników przechowuje tylko część merytoryczną

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Gdy pamięć wyników zwracała cały CheckResult, trafienie omijało pętlę moderatora: powtórzone pytanie nie zwiększało licznika, a użytkownik mógł zobaczyć cudzy numer sprawy.

## Decyzja

Pamięć wyników przechowuje tylko część merytoryczną (CachedResult): twierdzenia, ograniczenia, corpus\_version i identyfikatory cytowanych źródeł. Eskalację i licznik powtórzeń liczymy przy każdym zapytaniu, także przy trafieniu w pamięć. Sprawę tworzy drugie podobne pytanie bez odpowiedzi od kogokolwiek, w dowolnym kanale; liczba różnych pytających (ModeratorCase.distinct\_askers) tylko podnosi priorytet. Wyniku technical\_failure nigdy nie zapisujemy. CheckRecord.cache\_hit mówi, że część merytoryczna pochodzi z pamięci.

## Konsekwencje

Pętla informacji działa tak samo przy trafieniu w pamięć i bez niego, a awaria nie utrwala się na czas życia wpisu. **Ryzyko:** dwa źródła prawdy o wyniku (pamięć i eskalacja liczona na nowo) trzeba złożyć w jeden CheckResult w jednym miejscu kodu.

## Alternatywy

Cały CheckResult w pamięci; brak pamięci wyników.
