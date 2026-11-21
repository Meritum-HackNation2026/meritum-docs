# ADR-17. Serwer MCP (FastMCP) jako kolejny adapter i konektor dla aplikacji czatu AI

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

MSZ premiuje architekturę, do której łatwo podłączyć kolejne kanały. Wiele osób w Polsce korzysta już z asystentów AI, więc obywatel może dodać Meritum jako konektor w ChatGPT, claude.ai albo innej aplikacji czatu.

## Decyzja

FastMCP w backendzie wystawia zdalny serwer MCP przez Streamable HTTP pod publicznym adresem HTTPS. Ma dwa narzędzia: „sprawdź twierdzenie” nad tym samym portem co formularz i wtyczka oraz search\_sources nad portem CorpusSearch ([ADR-32](adr-32.md)). Sprawdzenie zwraca ten sam CheckResult według tych samych reguł co w innych kanałach: werdykt, cytaty z linkami, siłę i informację o AI. Odpowiedź zachowuje cytaty, żeby model w aplikacji czatu mógł je pokazać. Identyfikatorem sesji jest skrót z solą identyfikatora klienta MCP (kanał mcp w kontrakcie). Limity zapytań działają jak w innych kanałach, a uwierzytelnienie (klucz albo OAuth) dobieramy do wymagań aplikacji czatu.

## Konsekwencje

Kolejny kanał to kolejny adapter na tym samym porcie, a obywatel sprawdza twierdzenie w asystencie, z którego już korzysta. **Ryzyko:** nadużycia publicznego dostępu, stąd klucze i limity. Wymagań aplikacji czatu wobec konektorów (OAuth albo brak uwierzytelnienia, plany z własnymi konektorami) nie potwierdziliśmy (załącznik B). Model w aplikacji czatu może pominąć cytaty przy pokazywaniu odpowiedzi.

## Alternatywy

Tylko REST API.
