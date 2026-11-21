# ADR-20. Równoległe agenty badawcze i strumieniowanie odpowiedzi

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Proponowana

## Kontekst

Cel to najwyżej 30 s na sprawdzenie (treść zadania wymaga mediany do 30 s). Kroki wykonywane jeden po drugim sumują czasy wyszukiwania i modelu.

## Decyzja

Po wyodrębnieniu twierdzeń kilka agentów badawczych działa osobno i równolegle: korpus, wyszukiwanie na żywo (rusza zawsze, [ADR-07](adr-07.md)) i fact-checkerzy (krok search\_fact\_checks). Agent główny strumieniuje kolejne wersje odpowiedzi razem z postępem badań; wersja wstępna nie pokazuje werdyktu, dopóki cytaty nie przejdą weryfikacji ([ADR-06](adr-06.md)). Czas sprawdzenia bierzemy z zapisu przebiegu (received\_at → answered\_at), mierzony przez kanał. pydantic-evals uruchamia przypadki z naszego zestawu z kontrolą współbieżności (max\_concurrency); zadanie zwraca stan zamiast rzucać wyjątek, więc nieudane przypadki zostają w medianie (task\_duration obejmuje tylko udane przypadki).

## Konsekwencje

Czas odpowiedzi zależy od najwolniejszego agenta, na którego czekamy, a użytkownik widzi postęp od pierwszych sekund. **Ryzyko:** więcej równoczesnych wywołań modelu i wyszukiwarki podnosi koszt i szybciej wyczerpuje limity dostawców ([ADR-18](adr-18.md)).

## Alternatywy

Kroki po kolei bez strumieniowania; jeden agent od pytania do odpowiedzi.
