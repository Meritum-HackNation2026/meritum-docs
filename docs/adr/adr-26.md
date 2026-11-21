# ADR-26. EUvsDisinfo jako lokalna kopia

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Baza incydentów od organizatora i EUvsDisinfo odpowiadają na to samo wymaganie (scenariusz I), a teksty fact EUvsDisinfo to gotowe sprostowania. Wywołanie cudzego serwera w każdym sprawdzeniu dodaje opóźnienie i zależność.

## Decyzja

Bazę organizatora i EUvsDisinfo łączymy w jedną funkcję MVP. Workflow DBOS pobiera wszystkie artykuły i przypadki przez serwer MCP EUvsDisinfo stronami po 100, a każde pełne ponowne skanowanie zapisuje jako różnicę. Embeddingi wielojęzyczne liczymy dla twierdzenia i dla tekstu fact. Dopasowanie (IncidentMatch z polem database) jest kontekstem, a tekst fact cytatem (Citation, publisher\_id eeas-euvsdisinfo, Source.via = mcp). Domeny z linksToDisinformation dają jawny przypadek ostrzeżenia o domenie. Linki do materiałów z dezinformacją widzą tylko moderatorzy. Każde użycie ma oznaczenie źródła i zastrzeżenie strony. Token do serwera MCP (euvsdisinfo-mcp-server.vercel.app, streamable HTTP, Bearer token) EUvsDisinfo wydał na nasz wniosek; worker czyta go z sekretu GitHub Actions EUVSDISINFO\_MCP\_API\_KEY w meritum-worker. Licencji bazy nie znaleźliśmy i zapytaliśmy o nią we wniosku, a nota prawna EEAS pozwala na ponowne użycie z podaniem źródła, z zastrzeżeniem, że serwisy mogą mieć własne noty. Pytamy o to mentorów (załącznik A). Test niezmienności werdyktu obejmuje tylko IncidentMatch i ostrzeżenie o domenie.

## Konsekwencje

Dopasowanie nie woła sieci w trakcie sprawdzenia i znajduje wpisy w innych językach. **Ryzyko:** licencja bazy jest niepotwierdzona; serwer MCP działa na Vercel w USA (rejestr w [ADR-14](adr-14.md)); między skanami kopia może być nieaktualna.

## Alternatywy

Wywołanie serwera MCP w każdym sprawdzeniu; dwie osobne funkcje (baza organizatora w MVP, EUvsDisinfo później).
