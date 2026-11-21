---
icon: lucide/radio
---

# Kanały

Kanał to adapter wejściowy. Każdy wysyła do jednego API ten sam `CheckRequest` z innym polem `channel` (`web`, `extension`, `discord`, `sms`, `mcp`) i dostaje ten sam `CheckResult`. To samo pytanie daje więc ten sam wynik merytoryczny w każdym kanale, dopóki żyje wpis w pamięci wyników ([ADR-19](adr/adr-19.md)). Warunek konkursu „dwa kanały, ta sama logika” spełniają formularz WWW i Discord ([ADR-08](adr/adr-08.md)).

Każdy kanał przy pierwszym kontakcie mówi, że odpowiada system z użyciem AI (AI Act, art. 50).

| Kanał | Rola | Stan |
|---|---|---|
| :lucide-globe: Formularz WWW | kanał podstawowy | szkielet działa na [meritum.gburek.app](https://meritum.gburek.app) |
| :lucide-message-circle: Discord | drugi kanał | komendy działają, rdzeń weryfikacji w budowie |
| :lucide-puzzle: Wtyczka Chrome | kanał dodatkowy, dla jury opcjonalny | szkielet: popup ze stanem API |
| :lucide-plug: Konektor MCP | kolejny adapter | planowany, jeśli starczy czasu |
| SMS | adapter demonstracyjny | planowany, jeśli starczy czasu |

## Formularz WWW

Responsywna strona w meritum-frontend (React, TanStack Router i Query, shadcn/ui, Tailwind v4). Jedna kolumna działa od 320 px szerokości. Pole „Tekst albo link” przyjmuje do 4000 znaków albo pełny adres http(s), a w planie także plik audio. Przycisk „Sprawdź” uruchamia pasek analizy, potem pojawia się karta wyniku.

Konto nie jest potrzebne. Historia rozmowy zostaje w sessionStorage przeglądarki i znika po zamknięciu karty. Przycisk „Usuń moje sprawdzenia” usuwa zapisy sesji. Logowanie kontem Google albo Microsoft jest opcjonalne i planowane, jeśli starczy czasu: zalogowany użytkownik ma historię na serwerze i może ją usunąć razem z kontem.

W produkcji formularz to statyczny build w kontenerze nginx, który przekazuje `/api` do API tego samego środowiska.

## Discord

Discord jest kanałem wejściowym jak formularz. Interakcje HTTP, bez bota z trwałym połączeniem, trafiają do `POST /api/v1/discord/interactions` i są podpisane kluczem Ed25519 aplikacji. Aplikację da się dodać do serwera albo do własnego konta. Komendy:

- `/sprawdz tekst:<tekst albo link>`;
- „Sprawdź w Meritum” w menu Aplikacje przy dowolnej wiadomości.

Odpowiedź widzi tylko pytający. Każde środowisko ma własną aplikację Discord, a linki instalacji są w [README repozytorium zbiorczego](https://github.com/Meritum-HackNation2026/meritum-monorepo#discord). Polecenie `/usun-moje-dane` usuwa zapisy powiązane z identyfikatorem użytkownika.

Jury może sprawdzić kanał bez dołączania do serwera na makiecie Discorda w meritum-mocks, która woła to samo API co prawdziwy bot ([F-04 w dokumencie produktowym](https://github.com/Meritum-HackNation2026/meritum-design-system/blob/main/docs/product-doc.html)).

## Wtyczka Chrome

Wtyczka w Manifest V3 (WXT, React) dodaje przycisk „Sprawdź” pod postami na X, Facebooku, Instagramie, Reddicie i TikToku oraz pole do wklejenia tekstu w popupie. Oba wołają to samo API co formularz. Treść posta wysyłamy dopiero po kliknięciu.

Wstrzyknięty interfejs działa w Shadow DOM i dopasowuje się do platformy przez skórki z design systemu: krój, promień narożników, tło, obramowanie i kolor linków ([ADR-09](adr/adr-09.md)). Znak i słowo „Meritum”, werdykt i źródła z cytatem wyglądają wszędzie tak samo. Na makietach platform i na prawdziwych stronach działa ten sam skrypt, bo makiety odtwarzają te same selektory DOM ([ADR-10](adr/adr-10.md)).

Wtyczki nie publikujemy w Chrome Web Store. CI buduje zip z adresem API prd z gałęzi `main` i zostawia go jako artefakt przebiegu.

## Konektor MCP

FastMCP w backendzie wystawi zdalny serwer MCP (Streamable HTTP, publiczny adres HTTPS), który można dodać jako konektor w aplikacjach czatu AI ([ADR-17](adr/adr-17.md)). Planowane narzędzia to „sprawdź twierdzenie”, zwracające ten sam `CheckResult` z cytatami i linkami, oraz `search_sources` nad portem `CorpusSearch` ([ADR-32](adr/adr-32.md)). Identyfikatorem sesji jest skrót z solą identyfikatora klienta MCP. Limity zapytań działają jak w innych kanałach.

## SMS

Adapter demonstracyjny przez webhook bramki SMS na tym samym API, jeśli starczy czasu. Polskie znaki wymuszają kodowanie UCS-2, czyli 70 znaków, więc odpowiedź podaje werdykt głównego twierdzenia i link do pełnej karty wyniku. Opłaty operatora podamy wprost. Słowo USUN usuwa zapisy powiązane z numerem.
