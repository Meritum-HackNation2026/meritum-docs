---
icon: lucide/library
---

# Źródła i katalog

Meritum szuka dowodów tylko w jawnym katalogu źródeł. Katalog to lista domen, z których korzysta system. Każda pozycja (`CatalogEntry` w [kontraktach](../referencja/kontrakty.md#catalogentry)) ma:

- wydawcę z identyfikatorem `publisher_id`, według którego liczymy niezależne źródła;
- typ i poziom: urzędowe lub pierwotne (`primary`) albo wtórne (`secondary`);
- licencję albo podstawę prawną i wynik kontroli robots.txt oraz zastrzeżeń eksploracji tekstów i danych (TDM);
- sposób i częstotliwość odświeżania, ważność dokumentów i opcjonalny maksymalny wiek;
- powód kwalifikacji, a przy pozycji wykluczonej powód wykluczenia. Wykluczenie bez powodu nie przechodzi walidacji.

## Dwa typy źródeł

| Typ | Co obejmuje |
|---|---|
| Urzędowe i pierwotne | Serwisy gov.pl i agencji z listy organizatora (na przykład odyseusz.gov.pl, komunikaty RCB, policja.pl, moje.cert.pl), ISAP i EUR-Lex dla aktów prawnych, dane.gov.pl dla danych publicznych i strony BIP instytucji z katalogu. |
| Wtórne | Artykuły fact-checkerów fakenews.pl i pravda.org.pl (sygnatariusze IFCN) oraz teksty „fact” z EUvsDisinfo. |

Demagogu i AFP Sprawdzam nie pobieramy, bo blokują automaty. Konkret24 jest wykluczony: nie należy do IFCN ani EFCSN i wymaga umowy licencyjnej. Oceny ClaimReview z Google Fact Check Tools API, także tych fact-checkerów, służą do znajdowania adresów. Ocena fact-checkera z IFCN albo EFCSN może być przesłanką werdyktu: karta podaje wtedy nazwę fact-checkera, ocenę, tytuł, datę i link, bez fragmentu strony ([ADR-24](../adr/adr-24.md), [ADR-34](../adr/adr-34.md)).

Pełną ewidencję, czyli każde źródło z licencją, stanem kontroli robots.txt i tym, czego jeszcze brakuje, prowadzi sekcja „Ewidencja źródeł” w [dokumencie produktowym](https://github.com/Meritum-HackNation2026/meritum-design-system/blob/main/docs/product-doc.html).

## Korpus

Korpus powstaje z katalogu: dokumenty są pobierane, dzielone na fragmenty i wektoryzowane. Cel na hackathon to co najmniej 100 dokumentów z co najmniej 10 domen i obu typów. Wyszukiwanie jest hybrydowe: pgvector i wyszukiwanie pełnotekstowe ze słownikiem polskim w PostgreSQL ([ADR-04](../adr/adr-04.md)).

Nowe publikacje przychodzą z RSS i map stron. Robi to zaplanowany workflow DBOS co 15 do 30 minut, a błąd pobrania jest zapisywany i nie blokuje sprawdzeń. Korpus jest wersjonowany migawkami, a identyfikator migawki trafia do wyniku jako `corpus_version` ([ADR-19](../adr/adr-19.md)). Dev i prd czytają jeden wspólny schemat korpusu ([ADR-32](../adr/adr-32.md)).

```mermaid
flowchart LR
  CAT["Katalog źródeł"] --> ING["Workflow pobierania: RSS, mapy stron, wybrane akty"]
  ING --> SCAN["Skan pod kątem ukrytych poleceń"]
  SCAN --> CORP[("Korpus w PostgreSQL: pgvector, pełny tekst po polsku")]
  CORP --> SNAP["Migawka korpusu (corpus_version)"]
  LIVE["Wyszukiwanie na żywo w domenach katalogu"] --> Q["Kwarantanna do końca skanu"]
  Q --> EV["Dowód w bieżącym sprawdzeniu"]
  Q -.->|z następną migawką| CORP
```

## Wyszukiwanie na żywo

Wyszukiwanie na żywo uzupełnia korpus przy świeżych twierdzeniach i stoi za portem `WebSearch`. Szuka tylko w domenach z katalogu. Wynik daje adres kandydata, a stronę pobiera nasz kod, zgodnie z robots.txt, i dopiero wtedy ją cytuje ([ADR-07](../adr/adr-07.md)). Pobrana strona czeka w kwarantannie, aż skan wykluczy ukryte polecenia. Po skanie jest dowodem w sprawdzeniu, które ją pobrało, a do wspólnego korpusu dołącza z następną migawką ([ADR-21](../adr/adr-21.md)). Dostawców i ich warunki porównuje ADR-07.

## Przechowywanie

Pełny tekst dokumentu przechowujemy 90 dni od pobrania. Metadane i cytowane fragmenty zostają tak długo jak zapis przebiegu. Wydawca może poprosić o usunięcie. Użytkownik widzi krótki fragment z linkiem do źródła.
