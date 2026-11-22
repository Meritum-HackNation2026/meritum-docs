---
icon: lucide/ruler
---

# Ewaluacja

Liczby o jakości Meritum pochodzą tylko z naszej ewaluacji i zawsze mają dane do odtworzenia. Dopóki pierwszy przebieg się nie odbędzie, ta strona nie podaje żadnych wyników.

## Zestawy

| Zestaw | Skąd | Do czego |
|---|---|---|
| Golden set (zestaw deweloperski) | budujemy go z materiałów bazy wiedzy i według przykładowych pytań organizatora; obejmuje scenariusze A–J z treści zadania i polski zestaw ataków | strojenie progów, publikacja w repozytorium jako „zestaw jawny” |
| Zestaw referencyjny jury | od MSZ, dla zespołu ukryty | ocena przez jury; nigdy nie stroimy na nim progów |

Jury może uruchomić tę samą ewaluację na własnym pliku z przypadkami (JSON albo CSV, co najmniej 30 przypadków). Jeśli MSZ opublikuje jawną część zestawu referencyjnego, raport poda wyniki na niej i na golden secie osobno.

## Mierniki

- macro-F1 werdyktów; stany niebędące werdyktem (`technical_failure`, `needs_clarification`, `out_of_scope`) są w nim osobną klasą błędu;
- pokrycie i poprawność cytowań;
- odsetek wstrzymań;
- odporność na wstrzyknięcie poleceń;
- mediana i maksimum czasu odpowiedzi;
- koszt 100 sprawdzeń.

Werdykt przypadku to werdykt głównego twierdzenia wskazanego w pliku przypadku. Gdy oznaczono kilka twierdzeń, liczy się najgorszy wynik według stałej kolejności, od najgorszego: błędny werdykt rozstrzygający, stan niebędący werdyktem, błędne wstrzymanie się, wynik poprawny.

Czas przypadku pochodzi z zapisu przebiegu (`received_at` do `answered_at`), mierzony przez kanał. Zadanie zwraca stan zamiast rzucać wyjątek, więc nieudane przypadki zostają w medianie.

Próba wstrzyknięcia jest odparta, gdy werdykt zgadza się z etykietą tego samego przypadku bez polecenia, zdarzenie jest zapisane i żadne polecenie nie zostało wykonane ([ADR-23](adr/adr-23.md)).

## Jak uruchamiamy

Ewaluację prowadzi pydantic-evals ([ADR-28](adr/adr-28.md)). Nie biegnie w CI, nawet w części. Przebieg startuje ręcznie albo ze strony ewaluacji w aplikacji, jako workflow DBOS `eval_run` w workerze. Przebiegi i zestawy leżą w bazie (tabele `eval_runs` i `eval_datasets` z migracji 0005 w meritum-core), a plik własnego zestawu w `BlobStore`. Przebieg kończy się powiadomieniem.

Strona ewaluacji jest za logowaniem dla ról analityk i administrator. Pokazuje historię przebiegów z wynikami przypadków, uruchamia nowy przebieg, przyjmuje własny zestaw i porównuje dwa przebiegi. Odpowiada jej API: start przebiegu, lista, ostatni przebieg, wyniki przypadków, wgranie zestawu i porównanie. Jury może otworzyć stronę z jednorazowego linku, w sesji tylko do odczytu.

Z linii poleceń w repozytorium workera:

```bash
uv run meritum-eval                                  # golden set, raport JSON
uv run meritum-eval --cases jury.csv --output raport.json --max-concurrency 4
```

Model wybiera konfiguracja `MERITUM_LLM_*`, więc jeden przebieg na model daje porównywalny raport. Wyniki zawierają też mierniki spójności kanałów (`channel_consistency`), pętli informacji (`information_loop`, czyli wstrzymania przekazane moderatorowi), tokenów i kosztu na sprawdzenie oraz trafności per scenariusz A–J.

## Porównania

Kandydaci na model językowy i model embeddingów żyją w plikach TOML, nie w kodzie (`evals/models/`, `evals/embeddings/`). `--compare-models` i `--compare-embeddings` uruchamiają każdego na tym samym pliku przypadków i zapisują jeden raport z datą. Przebieg `gates` porównuje bramki przed modelem: klasyfikator wstrzyknięć, reranker i maskowanie z nadmiarowym maskowaniem ([ADR-35](adr/adr-35.md)). Model bez endpointu ZDR wolno uruchamiać wyłącznie na golden secie, nigdy na danych użytkowników. Po każdym przebiegu osoba z zespołu ocenia ręcznie losową próbę co najmniej 20 cytatów i zapisuje wynik w `evals/reports/`.

Koszt 1000 sprawdzeń liczy skrypt `scripts/measure_costs.py` w repozytorium zbiorczym (albo `meritum-cost` w workerze) z rekordów `CheckRecord`. Do czasu pomiaru na prawdziwych dostawcach ta strona nie podaje liczby.

## Odtwarzalność

Tryb ewaluacji przypina wersję korpusu (`corpus_version`) i odtwarza nagrane odpowiedzi dostawców modelu i wyszukiwania, tak zwane kasety. Przebieg powtarza się więc bez kluczy i bez sieci ([ADR-27](adr/adr-27.md)).

Publikujemy paczkę: pliki przypadków, adresy źródeł, cytowane fragmenty i manifest migawki z identyfikatorami dokumentów, sumami kontrolnymi i datą pobrania. Pełnych tekstów źródeł nie publikujemy, a kasety je zawierają, więc zostają poza paczką. Migawkę odtwarza się, pobierając strony ponownie i porównując sumy kontrolne z manifestem.
