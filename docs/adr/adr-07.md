# ADR-07. Wyszukiwanie w sieci za portem, tylko w domenach z katalogu

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Bez świeżych publikacji system wstrzymuje się przy każdym bieżącym wydarzeniu. Wyszukiwanie w całym internecie łamie zasadę jasno opisanego zbioru źródeł.

## Decyzja

Podstawą jest własny korpus: RSS i mapy stron domen z katalogu, a do znajdowania adresów Fact Check API i EUvsDisinfo. Wyszukiwanie na żywo uzupełnia korpus przy świeżych twierdzeniach i stoi za portem WebSearch. Pierwszy adapter to Vertex AI Search (Agent Search), website data store: basic website search w lokalizacji global, wzorce INCLUDE dla domen katalogu (do 50), edycja Enterprise, 4 USD za 1 000 zapytań po 10 000 darmowych miesięcznie. Data store, target\_site i search\_engine zakładamy Terraformem w meritum-infra (provider hashicorp/google 6.x; target\_site jest w 6.50.0, więc lock file nie może trzymać starszej wersji 6.x). Wynik daje tylko adres kandydata: stronę pobieramy sami, zgodnie z robots.txt i Content-Signal, i dopiero wtedy cytujemy. Zapasem za tym samym portem jest własna instancja SearXNG ograniczona do domen katalogu filtrami site:. Linkup (Paryż, includeDomains do 100, DPA) zostaje opcją za kluczem i wyłącznikiem w konfiguracji. Strony pobiera domyślnie nasz kod: klient HTTP i ekstrakcja tekstu (np. trafilatura), bo dosłowna weryfikacja cytatu ([ADR-06](adr-06.md)) potrzebuje dokładnego tekstu strony. Strony renderowane przez JavaScript pobiera lokalny crawler z przeglądarką bez interfejsu (np. Crawl4AI, open source). Firecrawl (includeDomains, country = PL) jest opcjonalną usługą hostowaną. Pobieranie źródeł katalogu do korpusu nie korzysta z Vertex AI Search ze względu na koszt: adresy dają RSS i mapy stron, a strony pobiera nasz kod. Vertex AI Search służy tylko wyszukiwaniu na żywo w trakcie sprawdzenia. Nasz filtr domen jest drugą kontrolą. Porównanie opcji jest w podsekcji „Wyszukiwanie w sieci: opcje”. Wyszukiwanie rusza przy każdym sprawdzeniu, równolegle z wyszukiwaniem w korpusie ([ADR-20](adr-20.md)); próg wyszukiwania decyduje tylko o tym, czy czekamy na jego wynik. Limit 10 s na wyszukiwanie. Każda pobrana strona przechodzi skan w kwarantannie; po skanie jest dowodem w tym samym sprawdzeniu, a do wspólnego korpusu dołącza z następną migawką, z datą pobrania, podstawą prawną i retencją (US-KOR-05, [ADR-21](adr-21.md)). Nie omijamy blokad; respektowanie robots.txt, Content-Signal i paywalli sprawdzamy testem adaptera. Gdy czekamy na wynik, błąd wyszukiwania, przekroczony limit czasu albo limit zapytań kończą sprawdzenie stanem technical\_failure z komunikatem dla użytkownika; odpowiedzi z samego korpusu wtedy nie podajemy. Gdy nie czekamy, błąd trafia tylko do zapisu przebiegu (retrieval\_errors).

## Konsekwencje

Świeże dowody już w bieżącej odpowiedzi, audytowalna lista domen. **Ryzyko:** basic website search działa tylko w lokalizacji global, więc zapytanie (zamaskowane twierdzenie) wychodzi poza UE; lokalizacja eu wymaga advanced indexing, a ten weryfikacji domeny przez jej właściciela. Ujawniamy to w README i w rejestrze ([ADR-14](adr-14.md)). Do tego koszt wywołania przy każdym sprawdzeniu i opóźnienie; europejski indeks (Staan) to droga migracji, gdy da publiczne API. SearXNG nie ma własnego indeksu, więc zależy od wyników i warunków wyszukiwarek, do których przekazuje zapytania (załącznik B).

## Alternatywy

Wyszukiwanie w całym internecie; tylko statyczny korpus; Grounding with Google Search (warunki zabraniają przechowywania i analizy wyników); Custom Search JSON API (zamknięte dla nowych klientów).

## Wyszukiwanie w sieci: opcje

Podstawą jest własny korpus z RSS i map stron domen katalogu, a adresy podsuwają Fact Check API i EUvsDisinfo. Wyszukiwanie na żywo uzupełnia korpus przy świeżych twierdzeniach (scenariusz D). Ceny i warunki ze stron dostawców z 21 listopada 2026 r.

| Opcja | Filtr domen | Cena | Przetwarzanie w UE | Przechowywanie wyników | Decyzja |
|---|---|---|---|---|---|
| Vertex AI Search (Agent Search), website data store | wzorce adresów INCLUDE i EXCLUDE (basic: 50 i 50); w Terraformie google\_discovery\_engine\_target\_site | edycja Enterprise 4 USD za 1 000 zapytań, 10 000 zapytań miesięcznie bez opłat | basic website search tylko w lokalizacji global; eu i us wymagają advanced indexing z weryfikacją domeny przez właściciela | osobnych warunków nie sprawdziliśmy | Rekomendowane |
| SearXNG (własna instancja) | site: w zapytaniu dla domen katalogu | bez opłat za zapytania; koszt własnego serwera | zapytania wychodzą z naszego serwera do wyszukiwarek, z których korzysta SearXNG, także spoza UE | wyniki trzymamy u siebie; warunki wyszukiwarek źródłowych niepotwierdzone | Zapas |
| Linkup (Paryż) | includeDomains do 100, excludeDomains | 5–6 USD za 1 000; 4 000 zapytań bez opłat | domyślnie zapytania mogą trafić do US, EU, CA albo APAC; lokalizacja gwarantowana tylko w Enterprise; DPA; kopie zapasowe w Europie | niepotwierdzone | Opcja |
| Firecrawl | includeDomains albo excludeDomains, country (domyślnie US, u nas PL) | wyszukiwanie ok. 7,6 USD za 1 000 w planie Hobby; pobranie strony 1 kredyt | brak deklaracji; zero retencji tylko w Enterprise | regulamin nie mówi; §8.d daje Firecrawl licencję do przesłanych treści | Opcja hostowana do pobierania stron |
| Tavily (Nebius) | include\_domains do 300, exclude\_domains do 150 | 5–8 USD za 1 000 | endpoint EU tylko dla wybranych klientów, bez daty dostępności | niepotwierdzone | Zapas, jeśli dostaniemy endpoint EU |
| Brave Search API | brak parametru; site: w zapytaniu albo Goggles | 5 USD za 1 000 | brak deklaracji UE | tylko w planie custom | Odrzucone |
| Exa | includeDomains (niepotwierdzone w dokumentacji) | 4–12 USD za 1 000 zależnie od trybu | brak deklaracji | brak informacji | Odrzucone |
| Parallel | include\_domains (domeny, prefiksy ścieżek, TLD) | od 1 USD za 1 000 | brak rezydencji | brak informacji | Odrzucone |
| Grounding with Google Search | tylko wykluczanie domen | 14 USD za 1 000 po 5 000 bez opłat | tylko global; logi zapytań 3 dni | warunki (sekcja 20(k)) zabraniają przechowywania i analizy wyników oraz używania linków do pobierania stron | Odrzucone |
| Web Grounding for Enterprise | brak parametru domen | 14 USD za 1 000 po 5 000 bez opłat | niepotwierdzone dla API Vertex | te same warunki co wyżej | Odrzucone |
| Custom Search JSON API | do 50 domen w wyszukiwarce programowalnej | 5 USD za 1 000 | nie dotyczy | nie dotyczy | Odrzucone: zamknięte dla nowych klientów, działa do 1 stycznia 2027 r. |
| Staan (Qwant i Ecosia) | brak publicznej dokumentacji | brak publicznego cennika | indeks europejski | brak samoobsługowego API | Droga migracji na później |
