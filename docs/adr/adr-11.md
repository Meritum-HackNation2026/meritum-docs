# ADR-11. Pydantic AI ze strukturalnym wyjściem; model nie decyduje sam

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Model rozumie pytanie, wyodrębnia twierdzenia, ocenia wymowę cytatów i pisze odpowiedź, ale nie może zmyślać źródeł ani rozstrzygać bez podstawy.

## Decyzja

Agenci Pydantic AI zwracają typy z kontraktu. Domyślny główny model to Claude Haiku 5.5 przez OpenRouter (decyzja zespołu z 21.11.2026; Vertex AI wymaga dla Claude formularza dostępu Anthropic dla firmy). OpenRouter działa bez routingu w UE, z ustawieniem ZDR (zapytania i odpowiedzi nie są rutynowo przechowywane), więc model działa poza EOG. Konto organizacji musi mieć wyłączone „Safety Retention”, inaczej ZDR dopuszcza też Google Vertex AI, które może trzymać oznaczone zapytania do 90 dni. Inne modele porównujemy testami ewaluacji (pydantic-evals, [ADR-28](adr-28.md)). Kryteria: niska cena, dużo tokenów na sekundę i dobra polszczyzna. Bielika i PLLuM nie rozważamy. Model wybierany konfiguracją; dostawca, region i koszt trafiają do CheckRecord. Opcjonalny model od dostawcy z UE: Mistral Small 3.1 w Vertex AI w europe-west4 (0,10 USD za 1 mln tokenów wejścia, 0,30 USD za 1 mln wyjścia), z przetwarzaniem w UE przy wywołaniu regionalnego API.

## Konsekwencje

Model wymienny bez zmiany domeny. **Ryzyko:** różne modele różnie trzymają format; ewaluacja przy każdej zmianie.

## Alternatywy

Wolny tekst parsowany ręcznie; model wpisany na sztywno.
