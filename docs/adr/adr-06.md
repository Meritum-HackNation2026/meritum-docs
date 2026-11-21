# ADR-06. Dosłowna weryfikacja cytatów

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Mierniki: pokrycie cytowań ≥ 95% i poprawność ≥ 85%. Model potrafi przekręcić cytat.

## Decyzja

Po wygenerowaniu odpowiedzi kod sprawdza, czy każdy fragment występuje w tekście źródła (po normalizacji spacji i cudzysłowów). Tytuł, wydawcę i datę bierzemy z bazy po identyfikatorze źródła. Czy fragment wspiera tezę, ocenia osobne wywołanie, które widzi twierdzenie, fragment i metadane z bazy (claim\_date, published\_at, validity); losową próbę sprawdzamy ręcznie w ewaluacji. Cytat niespełniający warunku odpada, a twierdzenie bez cytatu traci werdykt rozstrzygający.

## Konsekwencje

Brak zmyślonych cytatów i metadanych w odpowiedzi. **Ryzyko:** dosłowność nie gwarantuje, że fragment wspiera tezę; stąd osobna ocena wymowy i ręczna próba. Parafrazy odpadają, więc prompt wymaga dosłownych fragmentów.

## Alternatywy

Zaufanie modelowi; sprawdzanie podobieństwa embeddingów.
