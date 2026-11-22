---
icon: lucide/life-buoy
---

# Runbooki

Krótkie procedury dla operatora. Nazwy zmiennych są prawdziwe, wartości sekretów nigdy nie trafiają do zgłoszeń, logów ani zrzutów ekranu. Układ środowisk opisuje [Wdrożenie i uruchomienie](wdrozenie.md).

## Test gotowości

`GET /api/v1/health` zwraca 200, gdy niczego nie brakuje, a 503 z nazwami brakujących zmiennych i niedostępnych dostawców. Łączy raport API (baza, sól kanałów, magazyn plików, token Discorda) z raportem workera (workflow `readiness`). `GET /api/v1/health/live` sprawdza tylko proces i służy healthcheckowi Dockera.

1. Otwórz `/api/v1/health` środowiska i przeczytaj listę nazw.
2. Ustaw brakującą zmienną albo sekret repozytorium (`<NAZWA>_DEV` albo `_PRD`) i wdróż ponownie.
3. Po restarcie workera API odświeża jego raport w ciągu 60 s, bez restartu API.

Odpowiedź `"worker": "not_reported"` znaczy, że worker jeszcze nie opublikował raportu. Nie blokuje sprawdzeń. Brak klucza Fact Check API, odrzucony klucz albo limit dają `fact_check` w niedostępnych dostawcach (stan degraded, nie not ready). Gdy usługa jest niegotowa, `POST /api/v1/checks` odpowiada 503 ze stanem `technical_failure` i kodem `not_ready`.

## Sprawdzenia kończą się „Problem techniczny”

1. Odczytaj `failure_code` w zapisie sprawdzenia albo w wyniku.
2. Sprawdź `/api/v1/health` i log workera (`meritum-worker-<env>`): zmienne i dostawcy są w raporcie bez wartości.
3. Brak klucza OpenRouter, odrzucone dane logowania albo niedostępny Amazon Bedrock kończą się tym stanem, bo adapter przypina Haiku 5.5 do jednego dostawcy i nie przełącza się po cichu na innego. Przełączenie modelu to zmiana `MERITUM_LLM_*` i ponowny deploy.
4. Niedostępna wyszukiwarka, Fact Check API albo reranker nie zatrzymują sprawdzenia: wynik ma ograniczenie (na przykład `fact_check_unavailable`), a w logu stoi przyczyna.

## Przeciążenie

API liczy limity na adres IP, kraj i kanał oraz próg oczekujących sprawdzeń (`MERITUM_MAX_PENDING_CHECKS`, domyślnie 100). Ponad limit odpowiada 429 z komunikatem `errors.rate_limited` (`Retry-After: 60`) albo `errors.busy` (`Retry-After: 300`), nigdy werdyktem. Gdy baza liczników albo DBOS nie odpowiada, limit przepuszcza żądanie i zapisuje ostrzeżenie, a przed API zostają reguły Cloudflare.

## Migracja kończy wdrożenie błędem

Deploy workera robi migracje przed podmianą kontenera: `dbos migrate`, potem `meritum-worker-migrate` dla `app_<env>`, a z `main` także dla `corpus`. Błąd zatrzymuje wdrożenie, a stary kontener działa dalej. Log ma wpis `Migration failed` z nazwą zestawu (`app_dev`, `app_prd` albo `corpus`). Jeśli padł `corpus`, `app_prd` jest już zmigrowane. Migracje są addytywne, więc stary kod działa na nowym schemacie. Popraw migrację w meritum-core, podbij `rev` w workerze i wdróż ponownie.

## Discord

- Komendy nie odpowiadają: sprawdź, czy Interactions Endpoint URL aplikacji wskazuje `/api/v1/discord/interactions` środowiska, a `DISCORD_PUBLIC_KEY_{DEV,PRD}` jest ustawiony. Zły podpis daje 401.
- Bot nie reaguje na wzmianki: kontener `meritum-discord-<env>` startuje tylko z sekretem `DISCORD_BOT_TOKEN_{DEV,PRD}`. Bez tokenu proces kończy się kodem 1. Bot potrzebuje uprawnień do czytania i pisania w kanale.
- Nowa opcja komendy: deploy rejestruje komendy sam. Ręcznie: `scripts/register_discord_commands.py` z `DISCORD_APPLICATION_ID` i `DISCORD_BOT_TOKEN`.

## SMS

Bramka wysyła webhooki `sms:received` i `mms:downloaded` na `/api/v1/sms/webhook`, podpisane HMAC (klucz `MERITUM_SMS_GATEWAY_WEBHOOK_SIGNING_KEY`). Odpowiedź 401 znaczy zły podpis albo zegar rozjechany o więcej niż 5 minut. Webhooki rejestruje się przez API sms-gate.app ze stałym `id`, więc ponowna rejestracja nadpisuje, a nie dubluje. Dziś są zarejestrowane tylko dla dev, bo dev i prd dzielą telefon. Próba na żywo: wyślij SMS na numer bramki i sprawdź w logu `meritum-api-dev` wpis `POST /api/v1/sms/webhook ... 202`.

## Konektor MCP

Bez `MERITUM_MCP_API_KEYS` i bez trzech zmiennych `MERITUM_MCP_OAUTH_*` serwer odpowiada 401 każdemu. Jedna etykieta klucza na konektor pozwala odebrać dostęp jednemu klientowi: usuń parę `etykieta=klucz` z sekretu `MERITUM_MCP_API_KEYS_{DEV,PRD}` i wdróż ponownie. Klucze generuj losowo, na przykład `openssl rand -base64 32`.

## Logowanie

Brak pary `MERITUM_GOOGLE_CLIENT_ID` i `_SECRET` wyłącza Google, brak pary Microsoft wyłącza Microsoft. Adres powrotu wpisany u dostawcy to `<adres środowiska>/api/v1/auth/callback/<google|microsoft>`. Bez `MERITUM_SESSION_SECRET` proces losuje klucz, więc restart kończy wszystkie sesje. Rolę personelu nadaje administrator, a pierwsi administratorzy pochodzą z `MERITUM_ADMIN_EMAILS`. Rolę dostaje tylko adres z `email_verified: true`.

## Usunięcie danych na prośbę

1. Użytkownik z sesją, Discordem albo SMS-em usuwa dane sam (przycisk, `/usun-moje-dane`, słowo `USUN`).
2. Wniosek wydawcy o usunięcie źródła trafia do ewidencji w korpusie (migracja 0006), a worker czyści pełny tekst po 90 dniach i usuwa dokumenty na wniosek.
3. Po zmianie soli `MERITUM_CHANNEL_HASH_SALT` osoby z Discorda, SMS-a i MCP dostają nowe skróty, więc starych zapisów nie da się już z nimi połączyć. Nie zmieniaj soli bez powodu.

## Ewaluacja i link dla jury

Przebieg uruchamia analityk albo administrator ze strony ewaluacji. Link dla jury wystawia administrator (`POST /api/v1/staff/jury-links`): wygasa po 24 godzinach albo na koniec okresu oceny, a jego wykorzystanie go zużywa. Link demo wielokrotnego użytku można odwołać (`POST /api/v1/staff/demo-links/revoke`). Przebiegi z prawdziwymi dostawcami uruchamia się ręcznie, nigdy w CI.

## Skan sekretów zgłasza znalezisko

Gitleaks sprawdza historię pushowanej gałęzi. Jeśli zgłasza commit, którego nie ma w gałęzi, zrób rebase na `origin/main`. Fałszywy alarm dopisz z uzasadnieniem do `.gitleaks.toml`, zamiast pushować z `--no-verify`. Prawdziwy sekret unieważnij u dostawcy, zanim cokolwiek usuniesz z historii.
