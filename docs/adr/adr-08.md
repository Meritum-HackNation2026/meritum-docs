# ADR-08. Formularz WWW jako kanał podstawowy, Discord jako drugi; wtyczka i SMS jako kolejne

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

MSZ wymaga interfejsu WWW i drugiego kanału; wśród dopuszczonych kanałów wymienia m.in. SMS i Discord. Osoby o niskich kompetencjach cyfrowych nie powinny niczego instalować. W design systemie mamy makiety platform i zestaw wtyczki (style, skrypt referencyjny, popup); kod produktu to na razie szkielet.

## Decyzja

Formularz WWW obsługuje każdego. Historia rozmowy zostaje w sessionStorage przeglądarki. Kto zaloguje się kontem Google albo Microsoft (to opcja), ma historię na serwerze i może ją usunąć. Bot na Discordzie budujemy od początku na tym samym API: odpowiada na kanałach serwera i w wiadomościach prywatnych, a link zaproszenia pozwala dodać go do własnego serwera. Odpowiedź bota dzielimy: pierwsza wiadomość to podsumowanie z werdyktem każdego twierdzenia i linkiem do pełnej karty, potem po jednej wiadomości na twierdzenie z werdyktem, jednym najważniejszym cytatem ze źródłem i siłą. Każda mieści się w limicie Discorda, a podział nigdy nie przecina cytatu. W każdym kanale system przy pierwszym kontakcie mówi, że jest systemem AI. Razem z formularzem spełnia warunek dwóch kanałów, więc nie zależy on od decyzji mentorów w sprawie wtyczki. Jury testuje Discorda na makiecie z repozytorium meritum-mocks, która woła to samo API co bot, bez dołączania do serwera. Wtyczka dodaje „Sprawdź” pod postem i pole w popupie, oba wołają to samo API; dla jury jest opcjonalna, a wersja bez instalacji działa na makietach platform. Jeśli starczy czasu, dodamy SMS: adapter demonstracyjny, w którym webhook bramki SMS woła to samo API. Opłaty operatora podajemy wprost. Polskie znaki wymuszają kodowanie UCS-2, czyli 70 znaków w jednym SMS-ie, a odpowiedź dla kilku twierdzeń się nie zmieści. Zalecamy werdykt głównego twierdzenia i link do pełnego wyniku; opcją jest zamiana polskich znaków na litery bez ogonków (GSM-7, 160 znaków).

## Konsekwencje

Sprawdzanie tam, gdzie człowiek już jest, a jury przechodzi całą ścieżkę bez instalowania czegokolwiek. **Ryzyko:** makieta Discorda to dodatkowa strona do utrzymania; wtyczka wymaga ręcznej instalacji, więc nie jest główną ścieżką demo. SMS kosztuje (bramka i opłaty operatora) i mieści mało tekstu.

## Alternatywy

WhatsApp lub Messenger (weryfikacja konta firmowego).
