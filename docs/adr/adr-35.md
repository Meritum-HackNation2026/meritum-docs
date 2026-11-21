# ADR-35. Klasyfikatory jako tanie bramki przed LLM

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Sprawdzenie ma budżet 30 s, a każde wywołanie modelu kosztuje. Model językowy da się namówić wstrzykniętym tekstem do złamania reguł. Dokument wymaga ochrony przed wstrzyknięciami ([ADR-12](adr-12.md), [ADR-23](adr-23.md)), maskowania danych osobowych ([ADR-13](adr-13.md)) i dobrego pokrycia cytowań.

## Decyzja

W MVP trzy bramki przed LLM. Wstrzyknięcia w wejściu użytkownika i w pobranych stronach wykrywa osobny klasyfikator przed każdym wywołaniem modelu. Kandydaci: Model Armor w GCP (rezydencja danych tylko w multi-regionie eu, polskiego Google nie testował) oraz Prompt Guard albo Llama Guard w Cloudflare Workers AI. Wybieramy na naszym golden secie, bo polszczyznę trzeba zmierzyć; wykrycie zapisujemy jak w [ADR-23](adr-23.md). Fragmenty z korpusu i z wyszukiwania w sieci porządkuje przed LLM reranker (cross-encoder); kandydaci to Vertex AI ranking API i bge-reranker w Workers AI. Model dostaje mniej fragmentów, za to lepszych, więc odpowiada szybciej i taniej. Dane osobowe maskuje Google Sensitive Data Protection (DLP) w UE zamiast promptu: wynik jest deterministyczny i da się go skontrolować. W ewaluacji (pydantic-evals, [ADR-28](adr-28.md)) porównujemy, bez decyzji, dwie kolejne bramki: wielojęzyczny model NLI jako pierwszy krok oceny wymowy cytatu ([ADR-06](adr-06.md)), po którym LLM ocenia tylko niepewne przypadki, i tani klasyfikator wejścia (twierdzenie, needs\_clarification, out\_of\_scope) przed głównym modelem. Osobnego klasyfikatora tematów wysokiego ryzyka i grupowania spraw nie dodajemy, bo wystarczą embeddingi z progiem. Żaden model nie decyduje o werdykcie; werdykt zostaje regułą z przesłanek ([ADR-05](adr-05.md)). Każda bramka stoi za portem z zapasowym adapterem, który nic nie robi, więc awaria bramki nie zatrzymuje sprawdzeń, a zapis przebiegu notuje, że bramkę pominięto.

## Konsekwencje

Model dostaje mniej tekstu i mniej wstrzykniętych poleceń, a maskowanie da się sprawdzić. **Ryzyko:** jakość klasyfikatorów po polsku poznamy dopiero z pomiaru. Model Armor, Workers AI i Sensitive Data Protection to kolejne podmioty przetwarzające w rejestrze [ADR-14](adr-14.md), a Cloudflare jest poza UE. Gdy bramka jest pominięta z powodu awarii, ochrona jest słabsza do czasu jej powrotu.

## Alternatywy

LLM robi wszystko promptami; bez klasyfikatora wstrzyknięć, tylko obrona strukturalna.
