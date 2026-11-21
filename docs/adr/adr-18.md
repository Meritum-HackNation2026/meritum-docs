# ADR-18. Koszt i skalowanie

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Proponowana

## Kontekst

MSZ wymaga opisu kluczy, limitów, kosztów i zachowania przy zwiększonym ruchu. Koszt 100 testów jest miernikiem: przy równej jakości niższy wynik jest premiowany.

## Decyzja

Koszt każdego sprawdzenia liczymy z tokenów (ModelUsage) i wywołań wyszukiwarki zapisanych w CheckRecord. Z tych danych wyliczamy koszt 100 testów, koszt 1 000 zapytań i koszt utrzymania każdego kanału (np. hosting bota, bramka SMS). Liczby podamy po pomiarze w trakcie implementacji. Raportujemy odsetek trafień w pamięci wyników (CheckRecord.cache\_hit), bo trafienie nie wywołuje modelu ani wyszukiwarki. Sprawdzenia idą przez kolejkę DBOS z limitem współbieżności. DBOS nie zna pojęcia pełnej kolejki (ma tylko limit współbieżności globalny i na worker oraz limiter), więc HTTP 429 z jasnym komunikatem zwracamy według własnego licznika oczekujących sprawdzeń albo po przekroczeniu limitu zapytań. Przed API stoją Cloudflare (ochrona przed DDoS, reguły limitów) i middleware slowapi z limitami według adresu IP, regionu i kanału. W GCP liczba instancji API i workerów skaluje się automatycznie w granicach budżetu. Cel 30 s na sprawdzenie to wartość, do której optymalizujemy; po 30 s nic się nie dzieje.

## Konsekwencje

Koszt każdej odpowiedzi jest zmierzony, a limit współbieżności chroni przed przekroczeniem limitów dostawców. **Ryzyko:** na hackathon przyjmujemy te ryzyka. Ocena wymowy osobno dla każdego cytatu mnoży wywołania modelu i warstwy kontroli. Pełną kolejkę trzeba liczyć samemu. slowapi liczy w pamięci każdego procesu osobno, więc przy kilku instancjach limit się rozjeżdża. W szczycie ruchu kolejka może wydłużyć odpowiedź ponad cel 30 s. Zalecane, bez zobowiązania: pamięć wyników skanu według skrótu fragmentu, jedno wywołanie oceny wymowy na twierdzenie z izolowanymi parami twierdzenie i fragment, wspólny licznik w PostgreSQL albo Redisie.

## Alternatywy

Szacunek kosztu bez pomiaru; brak limitu współbieżności; własny middleware limitów od zera.
