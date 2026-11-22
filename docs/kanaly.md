---
icon: lucide/radio
---

# Kanały

Kanał to adapter wejściowy. Każdy wysyła do jednego API ten sam `CheckRequest` z innym polem `channel` (`web`, `extension`, `discord`, `sms`, `mcp`) i dostaje ten sam `CheckResult`. To samo pytanie daje więc ten sam wynik merytoryczny w każdym kanale, dopóki żyje wpis w pamięci wyników, wspólnej dla kanałów ([ADR-19](adr/adr-19.md)). Warunek konkursu „dwa kanały, ta sama logika” spełniają formularz WWW i Discord ([ADR-08](adr/adr-08.md)).

Każdy kanał przy pierwszym kontakcie mówi, że odpowiada system z użyciem AI (AI Act, art. 50). Wynik niesie też znacznik `ai_marker`, a API dodaje do odpowiedzi nagłówek `AI-Disclosure`.

| Kanał | Rola | Stan na `develop` |
|---|---|---|
| :lucide-globe: Formularz WWW | kanał podstawowy | działa: tekst, link, nagranie, zrzut ekranu, logowanie obywatela |
| :lucide-message-circle: Discord | drugi kanał | działa: komendy, wzmianki, wiadomości prywatne, wiadomości głosowe |
| :lucide-puzzle: Wtyczka Chrome | kanał dodatkowy, dla jury opcjonalny | działa, do pobrania z GitHub Releases |
| :lucide-plug: Konektor MCP | kolejny adapter | działa: `check_claim` i `search_sources`, z kluczem albo OAuth |
| :lucide-smartphone: SMS | adapter demonstracyjny | działa na dev przez bramkę sms-gate.app, także wiadomości MMS i RCS |

Wszystkie kanały przechodzą przez te same limity zapytań i to samo maskowanie danych osobowych. Ruch ponad limit dostaje HTTP 429 z komunikatem, nigdy werdykt.

## Formularz WWW

Responsywna strona w meritum-frontend (React, TanStack Router i Query, shadcn/ui, Tailwind v4). Jedna kolumna działa od 320 px szerokości. Sprawdzanie wygląda jak rozmowa: pytanie, podpisana odpowiedź i pole wiadomości na dole. Po pierwszym sprawdzeniu pole prosi o kolejne twierdzenie. Karta wyniku zaczyna się od werdyktu, a cytaty stoją bez ramek jako dowód. Na karcie jest też łańcuch dowodów na osi czasu z rozbieżnością i datami, blok kontekstu (fact-checker, incydent, sankcje) i „co zmieniłoby werdykt”.

Pole wiadomości przyjmuje:

- tekst do 4000 znaków albo pełny adres http(s);
- nagranie głosowe jako plik albo nagrywane na żywo w polu wiadomości. Karta pokazuje transkrypcję z ostrzeżeniem o możliwych błędach;
- zrzut ekranu z twierdzeniem. Karta pokazuje odczytany tekst, a obraz bez tekstu dostaje podpowiedź, co wysłać zamiast.

Stany niebędące werdyktem (doprecyzuj, poza zakresem, problem techniczny) mają własne, neutralne karty, a awaria serwera ma własny tekst. Przyciski „Zgłoś błąd” i „Przekaż moderatorom” tworzą sprawę albo dołączają do niej, a numer pojawia się po zapisie. Link „Przejdź do treści” stoi na początku każdej strony, a ekrany przeszły audyt WCAG 2.2 AA.

Konto nie jest potrzebne. Lista sprawdzeń z rozmowy żyje w sessionStorage przeglądarki, a „Usuń moje sprawdzenia” czyści zapisy. Obywatel może się zalogować kontem Google albo Microsoft (OIDC z PKCE): wtedy widzi historię na każdym urządzeniu, ma osobne usuwanie historii i konta z potwierdzeniem, a po zalogowaniu wraca na stronę, z której zaczął. Pytający czyta odpowiedź moderatora na osobnej stronie po powiadomieniu.

Panel personelu (kolejka spraw, konta, tematy wysokiego ryzyka, eksport FIMI, ewaluacja) opisują [Moderacja i odpowiedzi](jak-dziala/moderacja.md) i [Ewaluacja](ewaluacja.md). W produkcji aplikacja to statyczny build w nginx, który przekazuje `/api` i `/mcp` do API tego samego środowiska.

## Discord

Discord ma dwie drogi wejścia do tego samego sprawdzenia.

Interakcje HTTP trafiają do `POST /api/v1/discord/interactions`, podpisane kluczem Ed25519 aplikacji. Komendy:

- `/sprawdz tekst:<tekst albo link>` z opcją `publiczne:True`, która pokazuje odpowiedź całemu kanałowi (domyślnie widzi ją tylko pytający);
- „Sprawdź w Meritum” w menu Aplikacje przy dowolnej wiadomości (zawsze odpowiedź prywatna);
- `/usun-moje-dane`, które usuwa zapisy sprawdzeń użytkownika.

Osobny proces Gateway (`meritum-discord-<env>`, ten sam obraz co API) odpowiada na wzmianki bota na serwerze i na wiadomości prywatne, także głosowe. Używa tylko intencji `guilds`, `guild_messages` i `dm_messages`, bez uprzywilejowanej `MESSAGE_CONTENT`. Wiadomość bez wzmianki jest ignorowana. W docker compose to usługa w profilu `discord`, więc zwykłe uruchomienie nie wymaga tokenu bota.

Wynik to jedna wiadomość: osadzenie z polem na każde twierdzenie (werdykt, najważniejszy cytat ze źródłem i datą albo ocena fact-checkera, siła podstawy), kolor z najpoważniejszego werdyktu i przycisk „Pełna karta” z linkiem do wyniku w aplikacji. Za długi wynik skraca cytaty, nie twierdzenia. Numer sprawy pojawia się tylko wtedy, gdy sprawa została utworzona albo zaktualizowana.

Każde środowisko ma własną aplikację Discord, a linki instalacji są w [README repozytorium zbiorczego](https://github.com/Meritum-HackNation2026/meritum-monorepo#discord). Jury może sprawdzić kanał bez dołączania do serwera na makiecie Discorda w meritum-mocks, która woła to samo API co prawdziwy bot ([F-04 w dokumencie produktowym](https://github.com/Meritum-HackNation2026/meritum-design-system/blob/main/docs/product-doc.html)).

## Wtyczka Chrome

Wtyczka w Manifest V3 (WXT, React) dodaje przycisk „Sprawdź” pod postami na X, Facebooku, Instagramie, Reddicie i TikToku oraz pole do wklejenia tekstu w popupie. Oba wołają to samo API co formularz i wysyłają losowy `session_id`, zapisany tylko w przeglądarce. Treść posta wysyłamy dopiero po kliknięciu. Post zbyt krótki do sprawdzenia dostaje osobny tekst, a popup waliduje tekst i link tak samo jak formularz.

Wstrzyknięty interfejs działa w Shadow DOM i dopasowuje się do platformy przez skórki z design systemu: krój, promień narożników, tło, obramowanie i kolor linków ([ADR-09](adr/adr-09.md)). Znak i słowo „Meritum”, werdykt i źródła z cytatem wyglądają wszędzie tak samo. Na makietach platform i na prawdziwych stronach działa ten sam skrypt, bo makiety odtwarzają te same selektory DOM ([ADR-10](adr/adr-10.md)).

Wtyczki nie publikujemy w Chrome Web Store. Gotowy pakiet z adresem API prd jest do pobrania z GitHub Releases repozytorium meritum-extension (budowany z gałęzi `main`).

## Konektor MCP

Zdalny serwer MCP działa w tym samym procesie co API, pod adresem `/mcp` środowiska (Streamable HTTP). Można go dodać jako konektor w aplikacjach czatu AI ([ADR-17](adr/adr-17.md)). Narzędzia:

- `check_claim`: jedno twierdzenie albo pytanie o fakt do 4000 znaków; zwraca ten sam wynik z werdyktem, cytatami z linkami i siłą podstawy oraz informacją, że wynik tworzy system AI. Czeka do 90 s;
- `search_sources`: krótkie fragmenty z katalogu źródeł (tytuł, wydawca, data, link, wersja korpusu) nad portem `CorpusSearch`. To nie jest werdykt ([ADR-32](adr/adr-32.md)).

Dostęp wymaga klucza API (`Authorization: Bearer` albo `X-API-Key`) albo tokenu OAuth sprawdzanego introspekcją (RFC 7662). Bez nich serwer odpowiada 401. Tożsamość klienta MCP jest zapisywana tylko jako skrót HMAC z solą. Limity: 30 wywołań na minutę na klienta dla `check_claim` i 30 na minutę z adresu dla `search_sources`, oprócz wspólnych limitów sprawdzeń. Instrukcje podłączenia klientów są w README backendu. Claude Code łączy się kluczem API; ChatGPT wymaga serwera OAuth, którego zespół jeszcze nie ma.

## SMS

SMS idzie przez telefon z Androidem i aplikację SMS Gateway for Android w trybie Cloud (sms-gate.app). Bramka wysyła webhook `POST /api/v1/sms/webhook` ze zdarzeniami `sms:received` i `mms:downloaded`, podpisany HMAC; zły podpis albo znacznik czasu spoza ±5 minut daje 401. Wiadomość z telefonu z RCS bramka widzi jako MMS, więc jej treść idzie tą samą ścieżką, a załączniki są pomijane.

Numer nadawcy zamienia się od razu w skrót z solą i to on jest identyfikatorem sesji. Odpowiedź podaje werdykt głównego twierdzenia, bez linku, bo operatorzy filtrują linki. Polskie znaki wymuszają kodowanie UCS-2, czyli 70 znaków na SMS. Pierwszy SMS do numeru zaczyna się od informacji, że odpowiada system AI. Powtórzone zdarzenie bramki nie startuje drugiego sprawdzenia. Słowo `USUN` usuwa zapisy powiązane z numerem. Operator nadawcy może pobrać standardową opłatę za SMS według swojej taryfy. Webhooki są dziś zarejestrowane tylko dla dev, bo dev i prd dzielą jeden telefon.
