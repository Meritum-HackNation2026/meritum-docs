# ADR-19. Spójność kanałów: migawki korpusu, pamięć wyników, deterministyczny model

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Scenariusz G: to samo zgłoszenie przez WWW i drugi kanał ma dać ten sam wynik merytoryczny. Korpus rośnie przez RSS i wyszukiwanie na żywo, a model bez stałych ustawień odpowiada za każdym razem trochę inaczej.

## Decyzja

Korpus jest wersjonowany migawkami tworzonymi według harmonogramu (np. co godzinę); identyfikator migawki trafia do CheckResult.corpus\_version. Wynik zapisujemy w pamięci wyników pod kluczem ze znormalizowanego wejścia i zwracamy każdemu kanałowi. Wpis żyje stały czas (np. 2 h), niezależnie od nowych migawek, i trzyma tylko część merytoryczną ([ADR-22](adr-22.md)). Strony z wyszukiwania na żywo są dowodami w sprawdzeniu, które je pobrało, a do korpusu dołączają z następną migawką ([ADR-21](adr-21.md)). Model działa z temperaturą 0 i przypiętą wersją. Test spójności porównuje JSON z CheckResult, a nie wyrenderowany tekst kanału.

## Konsekwencje

To samo wejście, dopóki wpis w pamięci żyje, daje ten sam wynik merytoryczny w każdym kanale. **Ryzyko:** przez czas życia wpisu nowa publikacja nie zmieni odpowiedzi z pamięci; temperatura 0 nie gwarantuje identycznego tekstu u każdego dostawcy, więc o spójności decyduje pamięć wyników.

## Alternatywy

Klucz z identyfikatorem migawki (wpis traci ważność przy każdej nowej migawce); wersja korpusu podnoszona po każdym sprawdzeniu; brak pamięci wyników.
