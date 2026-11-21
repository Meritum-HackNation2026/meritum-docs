# ADR-11. Pydantic AI ze strukturalnym wyjściem; model nie decyduje sam

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Model rozumie pytanie, wyodrębnia twierdzenia, ocenia wymowę cytatów i pisze odpowiedź, ale nie może zmyślać źródeł ani rozstrzygać bez podstawy.

## Decyzja

Agenci Pydantic AI zwracają typy z kontraktu. Modele bierzemy z GCP przez Vertex AI: może to być dowolny dostępny tam model, niekoniecznie Claude. Główny model wybieramy testami ewaluacji (pydantic-evals, [ADR-28](adr-28.md)) spośród modeli dostępnych w Vertex AI w regionie UE. Kryteria: niska cena, dużo tokenów na sekundę i dobra polszczyzna. Bielika i PLLuM nie rozważamy. Model wybierany konfiguracją; dostawca, region i koszt trafiają do CheckRecord. Opcjonalny model od dostawcy z UE: Mistral Small 3.1 w Vertex AI w europe-west4 (0,10 USD za 1 mln tokenów wejścia, 0,30 USD za 1 mln wyjścia), z przetwarzaniem w UE przy wywołaniu regionalnego API.

## Konsekwencje

Model wymienny bez zmiany domeny. **Ryzyko:** różne modele różnie trzymają format; ewaluacja przy każdej zmianie.

## Alternatywy

Wolny tekst parsowany ręcznie; model wpisany na sztywno.
