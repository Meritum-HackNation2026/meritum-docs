# meritum-docs

Główna dokumentacja Meritum, obywatelskiego radaru dezinformacji (HackNation 2026, konkurs MSZ „Prawdowid”). Strona powstaje w [Zensical](https://zensical.org) z katalogu `docs/` i działa na Cloudflare Pages.

| Środowisko | Gałąź | Adres |
|---|---|---|
| produkcja | `main` | https://meritum-docs.pages.dev |

## Praca lokalna

Potrzebujesz `uv`.

```bash
uv sync
uv run zensical serve                    # http://localhost:8000, przeładowanie na żywo
uv run zensical build --strict --clean   # to samo co CI: ostrzeżenie, zły link albo brak kotwicy przerywa build
```

Zasady pisania, design system i podział na strony ręczne i generowane opisuje [AGENTS.md](AGENTS.md). W skrócie: każdy artykuł przechodzi przez skill `humanizer` z `.claude/skills/humanizer/`, wygląd wynika z design systemu Meritum, a fakty pochodzą z dokumentu produktowego i z repozytoriów.

Wygląd: `docs/assets/stylesheets/meritum.css` kopiuje tokeny z `tokens/meritum.css` (meritum-design-system) i przypisuje je do zmiennych motywu Zensical w trybie jasnym (`default`) i ciemnym (`slate`). Kroje Archivo i Azeret Mono ustawia `zensical.toml`. Po zmianie tokenów w design systemie trzeba je przepisać także tutaj.

## Strony generowane

`scripts/generate.py` (sama biblioteka standardowa Pythona) zapisuje tylko pliki ze swoim znacznikiem i odmawia nadpisania strony pisanej ręcznie.

```bash
# z lokalnych checkoutów obok tego repo
uv run python scripts/generate.py \
  --product-doc ../design-system/docs/product-doc.html \
  --schema ../core/contracts/meritum.schema.json
GH_TOKEN=$(gh auth token) uv run python scripts/generate.py --org Meritum-HackNation2026
uv run python scripts/test_generate.py   # samosprawdzenie parsera dokumentu produktowego
```

| Strona | Źródło |
|---|---|
| `docs/adr/` (indeks i strona na każdą decyzję) | sekcja „Decyzje architektoniczne” w `docs/product-doc.html`, meritum-design-system |
| `docs/slownik.md` | sekcja „Słownik pojęć” w tym samym dokumencie |
| `docs/referencja/kontrakty.md` | `contracts/meritum.schema.json`, meritum-core |
| `docs/architektura/repozytoria.md` | lista repozytoriów organizacji z API GitHuba |

## Workflowy

| Plik | Kiedy | Co robi | Sekrety |
|---|---|---|---|
| `.github/workflows/ci.yml` | każdy push | `zensical build --strict --clean`; na `main` dodatkowo `wrangler pages deploy` na produkcję | `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`; bez nich build przechodzi, a deploy jest pominięty z ostrzeżeniem |
| `.github/workflows/refresh.yml` | codziennie o 04:17 UTC i ręcznie | generuje strony od nowa, robi build w trybie strict i otwiera albo aktualizuje PR z gałęzi `chore/refresh-generated` do `main`, gdy coś się zmieniło | `MERITUM_BOT_TOKEN` do odczytu innych repozytoriów; push i PR idą przez `GITHUB_TOKEN`; bez sekretu workflow kończy się ostrzeżeniem |

Oba działają na runnerach `[self-hosted, meritum]`. Organizacja jest na planie Free, więc sekrety muszą być sekretami repozytorium, nie organizacji.

## Kroki dla właściciela

Projekt Cloudflare Pages `meritum-docs` (gałąź produkcyjna `main`) już istnieje, a sekret repozytorium `CLOUDFLARE_ACCOUNT_ID` jest ustawiony. Zostały trzy kroki.

1. Token Cloudflare do deployu. W panelu Cloudflare: My Profile → API Tokens → Create Token → Custom token, uprawnienie **Account → Cloudflare Pages → Edit**, zasób: konto z projektem `meritum-docs`. Potem:

    ```bash
    gh secret set CLOUDFLARE_API_TOKEN -R Meritum-HackNation2026/meritum-docs   # wklej token, gdy gh o niego poprosi
    ```

2. Token do odświeżania. Na GitHubie: Settings → Developer settings → Fine-grained personal access tokens → Generate new token. Właściciel zasobów `Meritum-HackNation2026`, dostęp do wszystkich repozytoriów (inaczej mapa repozytoriów będzie niepełna), uprawnienia **Contents: Read-only** i **Metadata: Read-only**. Potem:

    ```bash
    gh secret set MERITUM_BOT_TOKEN -R Meritum-HackNation2026/meritum-docs
    ```

3. PR z workflowu. Żeby `GITHUB_TOKEN` mógł otworzyć PR, włącz **Allow GitHub Actions to create and approve pull requests** w Settings → Actions → General → Workflow permissions, najpierw w organizacji, potem w tym repozytorium. Bez tego workflow i tak wypycha gałąź `chore/refresh-generated` i w ostrzeżeniu podaje link do ręcznego otwarcia PR.

Strony `*.pages.dev` są publiczne. Jeśli dokumentacja ma zostać prywatna do końca hackathonu, trzeba ją zamknąć za Cloudflare Access.
