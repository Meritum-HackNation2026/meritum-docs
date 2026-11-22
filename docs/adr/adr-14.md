# ADR-14. Demo na serwerze zespołu w Polsce, pliki i embeddingi Vertex AI w GCP europe-central2, model językowy przez OpenRouter; rejestr podmiotów przetwarzających

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Proponowana (w toku)

## Kontekst

Jury musi uruchomić system albo otworzyć demo bez naszej pomocy. MSZ premiuje przejrzystość miejsca przetwarzania i mniejszą zależność od dostawców spoza EOG.

## Decyzja

Na czas hackathonu demo (API, worker, PostgreSQL w kontenerze, patrz [ADR-04](adr-04.md)) działa na serwerze zespołu w Polsce, z Cloudflare przed nim (TLS, ochrona przed nadużyciami). W GCP europe-central2 (Warszawa) są tylko bucket na przesłane pliki i wywołania Vertex AI. Przeniesienie aplikacji do GCP przez CI/CD przygotowujemy, ale nie wdrażamy na hackathon; CI działa już na runnerach w GCP ([ADR-15](adr-15.md)). W UE przetwarzamy aplikację z bazą (serwer zespołu w Polsce) oraz pliki, embeddingi, transkrypcję i maskowanie danych osobowych (GCP). Poza UE są: główny model językowy Claude Haiku 5.5 przez OpenRouter (bez przechowywania danych, ZDR), Cloudflare (tunel i TLS, widzi całe żądania), Vertex AI Search (lokalizacja global), opcjonalnie Linkup i Firecrawl, Discord, logowanie Google i Microsoft, Google Fact Check Tools API, GitHub (kod i CI, bez danych użytkowników) i serwer MCP EUvsDisinfo na Vercel (tylko pobieranie danych). Rejestr pod tabelą podaje dla każdego podmiotu kraj, dane i cel; ten sam rejestr trafia do README i polityk prywatności kanałów. docker compose do uruchomienia lokalnego. Serwer on-prem z GPU tylko jako opcja dla otwartego modelu.

## Konsekwencje

Miejsce przetwarzania każdej części danych jest jawne. **Ryzyko:** demo zależy od serwera zespołu; README podaje, gdzie działa. Część danych zawsze trafia poza UE (rejestr). Koszt GCP w trakcie oceny: budżet i limity ustawione z góry.

## Alternatywy

Backend tylko na serwerze on-prem; Cloud Run bez workerów DBOS.

Rejestr podmiotów przetwarzających. Ten sam rejestr trafia do README i do polityk prywatności kanałów.

| Podmiot | Kraj lub region | Jakie dane | Po co |
|---|---|---|---|
| Serwer zespołu | serwer zespołu w Polsce | API, worker, PostgreSQL z zapisami przebiegu, sprawami i korpusem. Telefon zespołu z kartą prepaid i SMS Gateway for Android jako bramka SMS | demo na czas hackathonu (meritum.gburek.app) |
| Cloudflare | USA | całe żądania i odpowiedzi, w tym treść pytań i adresy IP, bo tunel kończy TLS | tunel do serwera zespołu, TLS, ochrona przed DDoS i limity |
| GCP europe-central2 | UE (Warszawa) | przesłane pliki i wywołania modeli wektorów, transkrypcji i maskowania danych; aplikacja i baza tu nie działają | magazyn plików i modele wektorów Vertex AI ([ADR-14](adr-14.md)) |
| OpenRouter (pośrednik do modelu językowego) | USA (OpenRouter, Inc.), poza EOG; standardowe klauzule umowne (moduł 2) w umowie powierzenia OpenRouter | zamaskowane twierdzenia, fragmenty źródeł, odpowiedzi modelu; ustawienie ZDR: zapytania i odpowiedzi nie są rutynowo przechowywane (wyjątki: kontrola CSAM, obowiązki prawne) | dostęp do głównego modelu językowego ([ADR-11](adr-11.md)) |
| Anthropic (Claude Haiku 5.5) | bez gwarancji EOG; z ZDR i wyłączonym Safety Retention model uruchamia Amazon Bedrock; podstawą przekazania jest umowa OpenRouter z Amazon, jej treści jeszcze nie sprawdziliśmy | zamaskowane twierdzenia, fragmenty źródeł, odpowiedzi modelu; tylko punkty końcowe z ZDR | główny model językowy: wyodrębnianie twierdzeń, ocena wymowy, odpowiedź ([ADR-11](adr-11.md)) |
| Model Armor (kandydat na klasyfikator wstrzyknięć) | GCP, multi-region eu | treść każdego wywołania modelu przed wysłaniem | wykrywanie wstrzyknięć przed modelem ([ADR-12](adr-12.md), [ADR-35](adr-35.md)) |
| Cloudflare Workers AI (kandydat) | Cloudflare, poza UE; region do sprawdzenia | wejście użytkownika, pobrane strony i fragmenty źródeł | klasyfikator wstrzyknięć (Prompt Guard albo Llama Guard) i reranker (bge-reranker), jeśli wygrają w ewaluacji ([ADR-35](adr-35.md)) |
| Vertex AI ranking API (kandydat) | GCP, region do sprawdzenia | zamaskowane twierdzenia i fragmenty źródeł | reranking fragmentów przed modelem ([ADR-35](adr-35.md)) |
| Google Sensitive Data Protection (DLP) | GCP, region UE | wejście użytkownika przed maskowaniem i wyniki kroków | maskowanie danych osobowych ([ADR-13](adr-13.md), [ADR-35](adr-35.md)) |
| Cloud Storage (bucket prywatny) | GCP europe-central2 (Warszawa) | pliki audio i obrazy ze sprawdzeń | przechowywanie plików przez czas życia zapisu sprawdzenia ([ADR-31](adr-31.md)) |
| Firecrawl (opcja) | USA | adresy i treść pobieranych stron | opcjonalne hostowane pobieranie stron ([ADR-07](adr-07.md)). Regulamin (§8.d) daje Firecrawl nieodwołalną licencję do przesłanych treści; prawo Kalifornii |
| Vertex AI Search (Agent Search) | GCP, lokalizacja global (poza gwarancją UE) | zapytania zbudowane z zamaskowanych twierdzeń | wyszukiwanie na żywo w domenach katalogu ([ADR-07](adr-07.md)) |
| SearXNG (własna instancja) | nasz serwer; zapytania trafiają dalej do wyszukiwarek, z których korzysta, także spoza UE | zapytania zbudowane z zamaskowanych twierdzeń | zapasowe wyszukiwanie na żywo ([ADR-07](adr-07.md)) |
| Linkup (opcja) | Francja; bez umowy Enterprise zapytania mogą trafić do US, EU, CA albo APAC | zapytania zbudowane z zamaskowanych twierdzeń | opcjonalne wyszukiwanie na żywo ([ADR-07](adr-07.md)) |
| Mistral w Vertex AI (opcja) | GCP europe-west4 | zamaskowane pytanie, fragmenty źródeł, odpowiedzi modelu | opcjonalny model od dostawcy z UE ([ADR-11](adr-11.md)) |
| Google Fact Check Tools API | Google, region do sprawdzenia | zapytania z twierdzeniami | znajdowanie artykułów fact-checkerów i ocena ClaimReview jako kontekst ([ADR-24](adr-24.md)) |
| Discord | USA | nazwa i identyfikator użytkownika, treść wiadomości do bota, wiadomości głosowe i odpowiedź | kanał Discord (US-WTY-06) |
| SMS Gateway for Android, sms-gate.app (tryb Cloud) | api.sms-gate.app; dostawca nie podaje regionu, poza gwarancją EOG | numer telefonu, treść SMS-a i odpowiedź | kanał SMS (US-WTY-07) |
| Google i Microsoft (logowanie) | USA | imię i nazwisko, adres e-mail i identyfikator konta | opcjonalne logowanie obywatela (US-SPR-10) i logowanie zespołu (moderatorzy, administratorzy) |
| Google Speech-to-Text v2 (Chirp 3) | GCP, multi-region eu | pliki audio i transkrypcje | weryfikacja nagrań ([ADR-30](adr-30.md)) |
| Vertex AI (embeddingi) | GCP europe-central2 (Warszawa) | zamaskowane twierdzenia, fragmenty źródeł, opisy incydentów | wyszukiwanie, podobieństwo spraw i incydentów ([ADR-04](adr-04.md)) |
| Serwer MCP EUvsDisinfo (Vercel) | USA | token i nasze zapytania o kolejne strony bazy, bez danych użytkowników | pobieranie lokalnej kopii EUvsDisinfo ([ADR-26](adr-26.md)) |
| Powiadomienia moderatora: Cloudflare Email Workers, Gmail API albo webhook (np. Google Chat) | Cloudflare albo Google, region do sprawdzenia | adres e-mail moderatora, numer i streszczenie sprawy | powiadomienia moderatora (US-POW-05, [ADR-29](adr-29.md)) |
| GitHub | USA | kod, zgłoszenia i logi CI, bez danych użytkowników | repozytoria i CI |
| Jasnopis (jeśli przez API) | do sprawdzenia | próbka odpowiedzi z ewaluacji | ocena zrozumiałości tekstu (US-DST-01) |
