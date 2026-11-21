# ADR-10. Kontrakt selektorów: ta sama wtyczka na makietach i prawdziwych stronach

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Demo musi działać przewidywalnie, a wtyczka ma działać na prawdziwych serwisach.

## Decyzja

Makiety (demo/platforms/) odtwarzają punkty zaczepienia DOM z SELECTORS.md. Wtyczka zna tylko kontrakt selektorów.

## Konsekwencje

Jeden kod na demo i produkcję. **Ryzyko:** selektory platform się zmieniają.

## Alternatywy

Osobny tryb demo we wtyczce.
