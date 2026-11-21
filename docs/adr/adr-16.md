# ADR-16. Frontend: React, TanStack Router + Query, shadcn/ui, Tailwind v4; jakość wymuszana narzędziami

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Formularz, panel moderatora i komponenty wtyczki muszą powstać szybko i spójnie z design systemem.

## Decyzja

React z TanStack Router i TanStack Query, shadcn/ui, tokeny Meritum w Tailwind v4. Biome strict, Ruff i Ty strict, TDD, pytestarch, behave.

## Konsekwencje

Te same tokeny w formularzu, panelu i wtyczce. **Ryzyko:** płatnych bloków shadcnblocks nie wolno publikować w publicznym repozytorium, a ich licencji nie da się przenieść na MSZ; używamy tylko darmowych bloków albo żadnych (sekcja 6).

## Alternatywy

Next.js; ESLint i Prettier.
