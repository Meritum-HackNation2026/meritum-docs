# ADR-29. Powiadomienia: skrzynka i toasty ze zdarzeń DBOS

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Część sprawdzeń trwa dłużej (nagrania, kolejka), moderator odpowiada po czasie, a nowy dowód może pojawić się po kilku dniach. Użytkownik nie powinien pilnować karty.

## Decyzja

Workflowy DBOS publikują zdarzenia, a API wysyła je do przeglądarki przez SSE. Aplikacja WWW pokazuje je od razu jako toasty (Sonner); toast, na który użytkownik nie zareagował, zostaje w skrzynce jako nieprzeczytany. Powiadomienie (kontrakt Notification) ma rodzaj, stan przeczytane albo nieprzeczytane, datę, link w aplikacji i adresata: sesję albo zalogowanego użytkownika, także moderatora. Niesie kody i identyfikatory, a tekst bierze z copy/pl.json. Retencja 30 dni; usunięcie sesji albo historii usuwa też powiadomienia. Moderator dostaje dodatkowo e-mail albo webhook. Opcje: Cloudflare Email Workers (send\_email) na zweryfikowane adresy moderatorów, Gmail API albo ogólny webhook, w tym przychodzący webhook Google Chat.

## Konsekwencje

Jeden mechanizm dla obywatela, moderatora i analityka. **Ryzyko:** bez logowania identyfikator sesji żyje w sessionStorage, więc po zamknięciu karty skrzynka jest nieosiągalna; trwałą skrzynkę ma tylko zalogowany użytkownik.

## Alternatywy

Tylko odpytywanie stanu sprawdzenia; powiadomienia e-mail dla wszystkich.
