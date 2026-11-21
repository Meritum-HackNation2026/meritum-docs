# ADR-05. Werdykt i jego siła liczone regułą z przesłanek

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

MSZ: siła werdyktu ma wynikać z jawnych przesłanek, a wynik modelu nie może być przedstawiony jako fakt bez podstawy.

## Decyzja

Model ocenia wymowę każdego cytatu (wspiera, obala, kontekst). Kod wybiera werdykt: same cytaty wspierające dają „potwierdzone”, same obalające „fałszywe”; „wprowadzające w błąd” wymaga cytatu dającego kontekst i nazwanej techniki; źródła sprzeczne dają „brak wystarczających dowodów” z cytatami obu stron obok siebie, notatką o różnicy i bez poziomu siły. Liczby są sprzeczne tylko wtedy, gdy mierzą tę samą wielkość, zakres i okres; szacunek z wypowiedzi i pozycja budżetu za konkretny rok to różne wielkości, a wyjaśnienie mówi, co mierzy każda (scenariusz C); brak cytatów to „brak wystarczających dowodów”, a opinie i przewidywania „nie podlega weryfikacji”. Siłę liczy funkcja strength\_for z przesłanek i mają ją tylko werdykty rozstrzygające. Liczymy wyłącznie wydawców, których cytaty mają wymowę zgodną z werdyktem (wspiera przy „potwierdzone”, obala przy „fałszywe”, kontekst przy „wprowadzające w błąd”), według identyfikatora wydawcy z katalogu (publisher\_id). Mocna: co najmniej 2 zgodni niezależni wydawcy, w tym co najmniej 1 urzędowy lub pierwotny, i świeże dowody. Umiarkowana: co najmniej 2 zgodni wydawcy albo 1 urzędowy lub pierwotny. Słaba: jeden wydawca spoza źródeł urzędowych albo dowód nieaktualny. Wiek liczymy od daty twierdzenia (claim\_date, z zapisanym pochodzeniem); źródło starsze o ponad 365 dni od tej daty to dowód nieaktualny, który obniża siłę do „słaba”. Pozycja katalogu może ustawić krótszy próg (max\_age\_hours) dla źródeł krótkotrwałych: ostrzeżeń, informacji drogowych, pogody, danych hydrologicznych. Wiek nie liczy się dla obowiązującego aktu prawnego, stałej strony urzędowej aktualizowanej w miejscu i dowodu wprost o zdarzeniu z przeszłości (pole validity przy każdym cytacie). Dowód zastąpiony nowszym (validity = superseded) nie tworzy rozbieżności i nie liczy się do siły ([ADR-25](adr-25.md)). Każde twierdzenie o fakcie dostaje werdykt: stan out\_of\_scope jest tylko dla nieobsługiwanego typu wejścia albo prośby, która nie dotyczy informacji, a needs\_clarification tylko dla wejścia bez twierdzeń. Kontrakt odrzuca werdykt niezgodny z tymi regułami, a także siłę przy werdykcie, który niczego nie rozstrzyga.

## Konsekwencje

Przesłanki są widoczne dla czytelnika i powtarzalne. **Ryzyko:** reguła może być zbyt ostrożna; progi stroimy na golden secie, nigdy na zestawie jury.

## Alternatywy

Pewność podawana przez model; jeden prompt od pytania do werdyktu.
