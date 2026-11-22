---
icon: lucide/house
---

# Czym jest Meritum

![](assets/images/meritum-mark.svg#only-light){ width="48" }
![](assets/images/meritum-mark-on-dark.svg#only-dark){ width="48" }

Meritum, obywatelski radar dezinformacji, pozwala sprawdzić informację tak łatwo, jak wysłać wiadomość. Powstaje na HackNation 2026 w konkursie MSZ „Prawdowid”.

Obywatel wkleja tekst albo link w formularzu na stronie, wysyła go botowi na Discordzie albo klika „Sprawdź” pod postem we wtyczce do przeglądarki. System wyodrębnia z treści twierdzenia i szuka ich w opisanym zbiorze źródeł: w dokumentach urzędowych, danych publicznych, u fact-checkerów i w świeżych publikacjach z zatwierdzonych serwisów. Każde twierdzenie dostaje jeden z pięciu werdyktów, a każde ustalenie prowadzi do dosłownego fragmentu źródła z tytułem, wydawcą, datą i linkiem. Gdy dowodów brakuje, system mówi to wprost i opisuje, czego nie ustalił. Taka sprawa może trafić do moderatora.

> Sprawdź, zanim podasz dalej.
>
> Każde ustalenie ma źródło. Gdy źródeł brak, mówimy to wprost.

## Zasady produktu

1. Bez źródła nie ma ustalenia. Każde twierdzenie, które system przedstawia jako ustalone, prowadzi do dosłownego fragmentu nazwanego źródła.
2. Wstrzymanie się jest odpowiedzią. Gdy dowodów brakuje albo są sprzeczne, system mówi to i wymienia, czego brakuje.
3. Interpretacja modelu jest podpisana jako taka i stoi osobno od materiału źródłowego.
4. Siła odpowiedzi wynika z przesłanek, które czytelnik widzi: liczby niezależnych źródeł, źródeł urzędowych, aktualności i zgodności.
5. O werdykcie nigdy nie decyduje to, kto coś powiedział. Domena, autor, kanał, popularność ani status źródła same nie rozstrzygają.
6. Awaria nie jest werdyktem. Brak klucza, limity i nieudane wywołania wyszukiwarki albo modelu są zgłaszane jako problem techniczny.
7. Meritum wspiera czytelnika i nie rozstrzyga za niego o prawdzie. Odpowiedź zaprasza do otwarcia dowodów, a sprawy, których system nie rozstrzygnie, przejmują ludzie.

## Dla kogo

| Kto | Czego potrzebuje |
|---|---|
| Obywatele | Wkleić tekst albo link i przeczytać krótką odpowiedź prostą polszczyzną, bez instalowania czegokolwiek i bez znajomości metod weryfikacji. |
| Czytelnicy mediów społecznościowych | Sprawdzić post jednym kliknięciem tam, gdzie go widzą (wtyczka). |
| Użytkownicy Discorda i SMS | Wysłać tekst, link albo wiadomość głosową botowi (na serwerze, w wiadomości prywatnej albo komendą) lub tekst na numer SMS i dostać krótką odpowiedź. Discord daje też przycisk „Pełna karta”. |
| Moderatorzy i analitycy | Przejmować twierdzenia bez odpowiedzi, które są wysokiego ryzyka albo się powtarzają, odpowiadać pytającym z cytatami ze źródeł, śledzić jakość (wstrzymania, próby wstrzyknięcia poleceń, czas odpowiedzi, koszt) i eksportować dane. |
| Jury konkursu MSZ | Samodzielnie przejść zestaw referencyjny przez formularz WWW i makietę Discorda. Wtyczka jest dla jury opcjonalna. |

## Stan prac

!!! info "Stan kodu"

    Na gałęzi `develop` działa cały tor sprawdzania: formularz, Discord, SMS, wtyczka i konektor MCP wysyłają to samo `CheckRequest`, a worker liczy wynik prawdziwym modelem (Claude Haiku 5.5 przez OpenRouter) na [kontrakcie w wersji 18](jak-dziala/sprawdzenie.md#kontrakt). Obsługuje tekst, link, nagranie głosowe i zrzut ekranu. Są też panel moderatora z odpowiedziami dla pytających, ewaluacja z przebiegami zapisanymi w bazie i eksport dla analityka. Na `main`, czyli w środowisku prd, część tej ścieżki czeka na promocję `develop` do `main`. Docelowy przebieg opisują [dokument produktowy](https://github.com/Meritum-HackNation2026/meritum-design-system/blob/main/docs/product-doc.html) i [decyzje architektoniczne](adr/index.md).

Działające środowiska:

| Co | prd (`main`) | dev (`develop`) |
|---|---|---|
| Aplikacja webowa | [meritum.gburek.app](https://meritum.gburek.app) | [meritum-dev.gburek.app](https://meritum-dev.gburek.app) |
| Dokumentacja API | [meritum.gburek.app/api/docs](https://meritum.gburek.app/api/docs) | [meritum-dev.gburek.app/api/docs](https://meritum-dev.gburek.app/api/docs) |
| Ta dokumentacja | [meritum-docs.pages.dev](https://meritum-docs.pages.dev) | brak, tylko `main` |

Adresy makiet platform, wtyczki i aplikacji Discord są w [README repozytorium zbiorczego](https://github.com/Meritum-HackNation2026/meritum-monorepo#działające-środowiska).

## Gdzie dalej

- [Sprawdzenie krok po kroku](jak-dziala/sprawdzenie.md): co się dzieje od kliknięcia „Sprawdź” do karty wyniku.
- [Werdykty i reguły](jak-dziala/werdykty.md): pięć werdyktów, siła podstawy i stany, które werdyktem nie są.
- [Moderacja i odpowiedzi](jak-dziala/moderacja.md): sprawy, odpowiedź dla pytającego, powiadomienia i eksport.
- [Architektura](architektura/index.md): kontekst, kontenery, przepływ danych, komponenty, porty i adaptery.
- [Runbooki](runbooki.md): co robić, gdy czegoś brakuje albo coś nie działa.
- [Współtworzenie](wspoltworzenie.md): zasady dla ludzi i agentów AI.
