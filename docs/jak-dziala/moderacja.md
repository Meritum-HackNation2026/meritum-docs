---
icon: lucide/user-check
---

# Moderacja i odpowiedzi

Gdy system nie rozstrzygnie twierdzenia, sprawę przejmują ludzie. Ta strona opisuje drogę od sprawy do odpowiedzi dla pytającego, powiadomienia i eksport dla analityka.

## Sprawy

Sprawa powstaje, gdy twierdzenie bez odpowiedzi dotyczy tematu wysokiego ryzyka z listy administratora, gdy podobne twierdzenie pojawia się drugi raz albo gdy użytkownik kliknie „Przekaż moderatorom” lub „Zgłoś błąd”. Pojedynczy brak dowodów w zwykłym temacie daje tylko zalecenie przekazania (`recommended`). Worker zakłada sprawy sam po werdykcie i grupuje podobne twierdzenia: podobieństwo embeddingów od 0,85 przy zgodnych liczbach, miesiącach i nazwach własnych, w oknie 14 dni. Numer sprawy użytkownik dostaje dopiero po jej zapisaniu. Gdy zapis się nie uda, karta mówi to osobnym komunikatem (`escalation.not_saved`) i nie podaje numeru. Dołączenie do istniejącej sprawy nie zdradza, że ktoś inny pytał o to samo.

## Panel i role

Personel loguje się kontem Google albo Microsoft. Rolę nadaje administrator, a pierwsi administratorzy pochodzą z konfiguracji.

| Rola | Co może |
|---|---|
| moderator | widzi kolejkę spraw i odpowiada pytającym |
| analityk | widzi mierniki i ewaluację, eksportuje dane |
| administrator | zarządza kontami personelu, listą tematów wysokiego ryzyka i celem powiadomień |

Konta personelu zapisuje repozytorium PostgreSQL z meritum-core, więc role przetrwają restart API. Zmiany stanu wymagają tokenu CSRF. Jury dostaje jednorazowy link, który otwiera sesję analityka tylko do odczytu na stronie ewaluacji. Link wygasa po 24 godzinach albo na koniec okresu oceny (najwyżej po 7 dniach), a jego wykorzystanie usuwa wiersz z bazy. Dla pokazów jest też link demo wielokrotnego użytku, który loguje na konto techniczne.

## Odpowiedź moderatora

Moderator pisze odpowiedź w formularzu panelu i dołącza cytaty ze źródeł. API sprawdza, czy każdy cytat występuje dosłownie w tekście źródła z katalogu, i odrzuca odpowiedź z cytatem, którego nie znalazło ([ADR-06](../adr/adr-06.md)). Odpowiedź nie jest publiczna. Pytający dostaje powiadomienie `moderator_answer` w sesji albo na koncie i czyta odpowiedź na osobnej stronie. Tożsamość pytających nie trafia do panelu: nazwa z Discorda ani numer SMS nie są nigdzie zapisane w jawnej postaci.

## Powiadomienia dla moderatorów

Po zapisaniu nowej albo zaktualizowanej sprawy moderatorzy i administratorzy dostają w skrzynce powiadomienie `case_assigned`. Administrator wybiera dodatkowo jeden cel zewnętrzny: webhook podpisany HMAC-SHA256, przestrzeń Google Chat albo e-mail wysyłany przez Worker Cloudflare. Wysyłka ma cztery próby z przerwami 1, 2 i 4 s, a po ostatniej zapisuje tylko błąd w logu i nie blokuje sprawy. Treść nie zawiera danych osobowych ani identyfikatorów kanałów, a sekret konfiguracji nigdy nie wraca w API.

## Eksport dla analityka

Analityk i administrator eksportują sprawdzenia z ostatnich dni i sprawy w trzech formatach: JSON, CSV i STIX 2.1. Dane są zamaskowane. Ekran eksportu FIMI w panelu wywołuje ten sam punkt końcowy `GET /api/v1/export`. Eksport obejmuje sprawdzenia powiązane ze sprawami, bo port zapisów nie ma jeszcze zapytania o wszystkie.

## Dane i retencja

Sprawy, powiadomienia i zapisy sprawdzeń znikają zgodnie z [retencją 30 dni](../prywatnosc.md). Usunięcie danych osoby usuwa jej miejsce w sprawie, a sprawa zostaje dla innych pytających. Zapis sprawy wczytany przed usunięciem nie przywróci usuniętego sprawdzenia, bo `removed_case_checks` trzyma losowy identyfikator sprawdzenia przez 30 dni.
