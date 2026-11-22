---
icon: lucide/scale
---

# Werdykty i reguły

Każde twierdzenie dostaje jeden z pięciu werdyktów. Nazwy i podpowiedzi pochodzą z `copy/pl.json` w design systemie, a kody z kontraktu (`ClaimResult.verdict`). Werdykt zawsze jest pokazany słowem, nigdy samym kolorem.

<div class="m-legend" markdown>

| Werdykt | Kod | Podpowiedź na karcie wyniku |
|---|---|---|
| <span class="m-verdict m-verdict--confirmed">Potwierdzone</span> | `confirmed` | Źródła potwierdzają to twierdzenie. |
| <span class="m-verdict m-verdict--false">Fałszywe</span> | `false` | Źródła przeczą temu twierdzeniu. |
| <span class="m-verdict m-verdict--misleading">Wprowadzające w błąd</span> | `misleading` | Dane mogą być prawdziwe, ale prowadzą do błędnego wniosku albo brakuje im kontekstu. |
| <span class="m-verdict m-verdict--muted">Brak wystarczających dowodów</span> | `insufficient_evidence` | Nie rozstrzygamy, bo nie mamy wystarczających źródeł. |
| <span class="m-verdict m-verdict--muted">Nie podlega weryfikacji</span> | `not_verifiable` | To opinia, przewidywanie albo ocena. Faktów nie da się tu sprawdzić. |

</div>

Kolory plakietek to tokeny `--verified`, `--contested`, `--scam` i `--muted` z `tokens/meritum.css`. Czerwień pojawia się tylko przy werdykcie „Fałszywe”.

## Jak kod wybiera werdykt

Model ocenia tylko wymowę każdego cytatu: wspiera twierdzenie, obala je albo daje kontekst (`supports`, `refutes`, `context`). Werdykt wybiera kod według stałej reguły ([ADR-05](../adr/adr-05.md)):

- same cytaty wspierające dają „Potwierdzone”, same obalające dają „Fałszywe”;
- „Wprowadzające w błąd” wymaga cytatu, który daje kontekst, i nazwanej techniki manipulacji;
- wiarygodne źródła sprzeczne ze sobą dają „Brak wystarczających dowodów” z cytatami obu stron obok siebie, jednym zdaniem o tym, czym się różnią, i bez siły;
- brak cytatów też daje „Brak wystarczających dowodów”, a karta zawsze mówi, czego nie ustalono;
- opinie, przewidywania i oceny dostają „Nie podlega weryfikacji”.

Pierwsze trzy werdykty są rozstrzygające. Każdy wymaga co najmniej jednego cytatu i jawnych przesłanek. Cytat przechodzi tylko wtedy, gdy jego fragment znaleziono w źródle dosłownie ([ADR-06](../adr/adr-06.md)). Tych reguł pilnuje walidacja kontraktów w meritum-core ([ADR-02](../adr/adr-02.md)).

## Siła podstawy

Siłę mają tylko werdykty rozstrzygające. Liczy ją funkcja z przesłanek, a nie deklaracja modelu. Liczą się wyłącznie wydawcy, których cytaty zgadzają się z werdyktem, według identyfikatora wydawcy z katalogu (`publisher_id`), a nie według strony.

| Siła | Warunek |
|---|---|
| <span class="m-strength" data-level="3">Mocna <span class="m-strength__bars" aria-hidden="true"><i></i><i></i><i></i></span></span> | co najmniej 2 zgodni niezależni wydawcy, w tym co najmniej 1 urzędowy lub pierwotny, i świeże dowody |
| <span class="m-strength" data-level="2">Umiarkowana <span class="m-strength__bars" aria-hidden="true"><i></i><i></i><i></i></span></span> | co najmniej 2 zgodni wydawcy albo 1 urzędowy lub pierwotny |
| <span class="m-strength" data-level="1">Słaba <span class="m-strength__bars" aria-hidden="true"><i></i><i></i><i></i></span></span> | jeden wydawca spoza źródeł urzędowych albo dowód nieaktualny |

Ocena fact-checkera z IFCN albo EFCSN liczy się jak jeden wydawca wtórny, a jedna taka ocena daje siłę co najmniej „Umiarkowana”. Częściowe potwierdzenie twierdzenia nie daje werdyktu „Potwierdzone”.

Siła jest zawsze w kolorze atramentu, jako słowo i trzy kreski poziomu.

Wiek dowodu liczymy od daty, której dotyczy twierdzenie, i zapisujemy, skąd ta data pochodzi: z tekstu, z daty publikacji wejścia albo z dnia sprawdzenia. Źródło starsze o ponad 365 dni od tej daty jest nieaktualne i obniża siłę do „Słaba”. Pozycja katalogu może ustawić krótszy próg (`max_age_hours`) dla źródeł krótkotrwałych, takich jak ostrzeżenia czy informacje drogowe. Obowiązujący akt prawny, strona urzędowa aktualizowana w miejscu i dowód o zdarzeniu z przeszłości nie są archiwalne. Dowód zastąpiony nowszym nie tworzy sprzeczności ([ADR-25](../adr/adr-25.md)).

## Stany, które nie są werdyktem

Gdy sprawdzenie nie kończy się werdyktem, karta pokazuje ikonę, tytuł stanu i komunikat. Nie ma plakietki ani źródeł, bo awaria nie jest oceną treści.

| Stan | Kod | Komunikat |
|---|---|---|
| <span class="m-state">:lucide-circle-help: Doprecyzuj pytanie</span> | `needs_clarification` | Nie wiemy, które twierdzenie sprawdzić. Napisz je jednym zdaniem. |
| <span class="m-state">:lucide-circle-slash: Poza zakresem</span> | `out_of_scope` | Sprawdzamy twierdzenia o faktach z życia publicznego. Tego pytania nie obsługujemy. |
| <span class="m-state">:lucide-triangle-alert: Problem techniczny</span> | `technical_failure` | Nie udało się sprawdzić. To nie jest ocena treści. Spróbuj za kilka minut. |

„Poza zakresem” dostaje tylko nieobsługiwany typ wejścia albo prośba, która nie dotyczy informacji, na przykład o napisanie tekstu. „Doprecyzuj pytanie” dostaje tylko wejście, z którego nie da się wyodrębnić żadnego twierdzenia. Każdy tekst ograniczenia ma własny kod, a stan „Poza zakresem” podaje kod powodu (nagranie, obraz, rodzaj prośby), więc karta mówi, co wysłać zamiast. Niedostępny adres albo strona za paywallem to problem techniczny. Każde twierdzenie o fakcie dostaje werdykt.

## Ostrzeżenia obok werdyktu

Obok werdyktu karta może pokazać werdyktu ocenę fact-checkera, materiał archiwalny, podobieństwo do znanego incydentu i neutralną informację, że treść pochodzi od podmiotu z oficjalnej listy sankcji UE. Każde ostrzeżenie stoi w osobnym wierszu, bez czerwieni, i żadne nie zmienia werdyktu. Pole „co zmieniłoby werdykt” liczy reguła, a oś czasu dowodów pokazuje daty i rozbieżność.

## Sprawy dla moderatorów

Twierdzenie bez odpowiedzi trafia do kolejki moderatorów, gdy dotyczy tematu wysokiego ryzyka z listy administratora albo gdy podobne twierdzenie bez odpowiedzi pojawia się drugi raz, od kogokolwiek i w dowolnym kanale. Podobne twierdzenia trafiają do jednej sprawy. Karta odróżnia zalecenie przekazania od faktycznego przekazania, a dołączenie do istniejącej sprawy nigdy nie zdradza, że ktoś inny pytał o to samo.
