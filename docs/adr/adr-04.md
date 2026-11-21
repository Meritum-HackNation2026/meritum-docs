# ADR-04. PostgreSQL z pgvector i wyszukiwaniem pełnotekstowym

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Wyszukiwanie dowodów wymaga podobieństwa znaczeniowego i dokładnych słów (nazwy, liczby, daty).

## Decyzja

Jedna baza: dokumenty, fragmenty, embeddingi w pgvector, indeks pełnotekstowy, zapisy przebiegu, sprawy. PostgreSQL we własnym obrazie kontenera (pgvector/pgvector:0.8.7-pg18-trixie) ze słownikiem polskim z pakietu Debiana hunspell-pl, na którym infra buduje konfigurację public.polish; bez niego „Tusk” i „Tuska” to różne słowa. Licencja słownika według debian/copyright pakietu źródłowego libreoffice-dictionaries (Debian trixie): GPL, LGPL, MPL, Apache-2.0 albo CC-SA-1.0 do wyboru; wybieramy Apache-2.0 (sekcja 6). Do tego pg\_trgm na literówki. Embeddingi domyślnie z gemini-embedding-001 w Vertex AI. Ewaluacja porównuje go z tańszymi modelami (np. text-multilingual-embedding-002) na golden secie wyszukiwania; tańszy model z lepszym wynikiem zastępuje domyślny ([ADR-28](adr-28.md)). Model, dostawcę i region podajemy w README. Wyniki obu wyszukiwań łączone i ważone świeżością.

## Konsekwencje

Jeden system do kopii i wdrożenia; DBOS korzysta z tej samej bazy. **Ryzyko:** zarządzana baza (Cloud SQL) nie pozwala dodać własnego słownika, więc PostgreSQL działa w kontenerze i sami robimy kopie.

## Alternatywy

Osobna baza wektorowa; Elasticsearch.
