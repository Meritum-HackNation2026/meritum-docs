# ADR-13. Prywatność: maskowanie, retencja, usuwanie danych, konta opcjonalne

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

MSZ wymaga minimalizacji danych, maskowania oczywistych danych osobowych, retencji i usuwania sesji demonstracyjnej.

## Decyzja

Maskowanie telefonów, e-maili i PESEL-i przez Google Sensitive Data Protection w UE ([ADR-35](adr-35.md)) w API, zanim wystartuje workflow DBOS (DBOS zapisuje wejścia w bazie), więc ani zapis, ani dostawca modelu nie dostają danych w jawnej postaci. Tak samo maskujemy wyniki kroków, które DBOS zapisuje (pobrane strony, odpowiedzi modelu). Retencja 30 dni, usuwanie workflowem DBOS; obie obejmują tabele systemowe DBOS. Konto nie jest potrzebne: sesja ma losowy identyfikator w przeglądarce (CheckRecord.session\_id), historia rozmowy zostaje w sessionStorage, a „Usuń moje sprawdzenia” czyści też dane workflowów i powiązania ze sprawami. Kto zaloguje się kontem Google albo Microsoft, ma na serwerze identyfikator konta od dostawcy logowania (CheckRecord.user\_id) i historię sprawdzeń z zamaskowanym pytaniem. Usuwa ją przyciskiem „Usuń moją historię”, a razem z kontem przyciskiem „Usuń konto”. Sposób przetwarzania adresów IP (limit zapytań) i retencję logów określa polityka prywatności. Kanały inne niż strona (Discord, SMS, wtyczka) mają osobne polityki. Discord daje nazwę i identyfikator użytkownika, SMS numer telefonu: przetwarzamy je tylko, żeby odpowiedzieć i policzyć powtórzenia, przechowujemy jako skrót z solą (CheckRecord.channel\_user\_hash) z retencją 30 dni i nie pokazujemy moderatorom. W tych kanałach i w MCP ten skrót jest też identyfikatorem sesji (session\_id). Powiadomienia mają tę samą retencję 30 dni. Polecenie /usun-moje-dane na Discordzie i SMS ze słowem USUN usuwają zapisy dla identyfikatora. Telemetria użycia służy tylko zbiorczym miarom liczbowym, a adresy IP i regiony możemy przetwarzać dla ochrony przed DDoS i innymi atakami (US-BEZ-06).

## Konsekwencje

Mniej danych osobowych w systemie i u dostawców. **Ryzyko:** maskowanie regułami nie złapie wszystkiego; opisujemy to w ograniczeniach.

## Alternatywy

Pełne logi bez maskowania; obowiązkowe konta użytkowników.
