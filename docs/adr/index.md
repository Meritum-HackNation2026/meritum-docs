---
icon: lucide/scroll-text
---

# Decyzje architektoniczne (ADR)

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

Status **Przyjęta** oznacza decyzję podjętą przez zespół. **Proponowana** czeka na przegląd, odpowiedź mentorów albo wdrożenie; **w toku** znaczy, że wdrożenie trwa.

| Numer | Decyzja | Status |
|---|---|---|
| [ADR-01](adr-01.md) | Pionowe wycinki domenowe z architekturą heksagonalną | **Przyjęta** |
| [ADR-02](adr-02.md) | Kontrakty Pydantic jako jedno źródło prawdy i miejsce reguł z treści zadania | **Przyjęta** |
| [ADR-03](adr-03.md) | DBOS dla workflowu sprawdzania i cyklicznego pobierania źródeł | **Przyjęta** |
| [ADR-04](adr-04.md) | PostgreSQL z pgvector i wyszukiwaniem pełnotekstowym | **Przyjęta** |
| [ADR-05](adr-05.md) | Werdykt i jego siła liczone regułą z przesłanek | **Przyjęta** |
| [ADR-06](adr-06.md) | Dosłowna weryfikacja cytatów | **Przyjęta** |
| [ADR-07](adr-07.md) | Wyszukiwanie w sieci za portem, tylko w domenach z katalogu | **Przyjęta** |
| [ADR-08](adr-08.md) | Formularz WWW jako kanał podstawowy, Discord jako drugi; wtyczka i SMS jako kolejne | **Przyjęta** |
| [ADR-09](adr-09.md) | Wtyczka Chrome MV3: widżety w Shadow DOM ze skórkami platform | **Przyjęta** |
| [ADR-10](adr-10.md) | Kontrakt selektorów: ta sama wtyczka na makietach i prawdziwych stronach | **Przyjęta** |
| [ADR-11](adr-11.md) | Pydantic AI ze strukturalnym wyjściem; model nie decyduje sam | **Przyjęta** |
| [ADR-12](adr-12.md) | Ochrona przed prompt injection warstwami | **Przyjęta** |
| [ADR-13](adr-13.md) | Prywatność: maskowanie, retencja, usuwanie danych, konta opcjonalne | **Przyjęta** |
| [ADR-14](adr-14.md) | GCP w UE (europe-central2) jako docelowe miejsce demo; rejestr podmiotów przetwarzających | **Proponowana (w toku)** |
| [ADR-15](adr-15.md) | Self-hosted runnery GitHub Actions | **Przyjęta** |
| [ADR-16](adr-16.md) | Frontend: React, TanStack Router + Query, shadcn/ui, Tailwind v4; jakość wymuszana narzędziami | **Przyjęta** |
| [ADR-17](adr-17.md) | Serwer MCP (FastMCP) jako kolejny adapter i konektor dla aplikacji czatu AI | **Przyjęta** |
| [ADR-18](adr-18.md) | Koszt i skalowanie | **Proponowana** |
| [ADR-19](adr-19.md) | Spójność kanałów: migawki korpusu, pamięć wyników, deterministyczny model | **Przyjęta** |
| [ADR-20](adr-20.md) | Równoległe agenty badawcze i strumieniowanie odpowiedzi | **Proponowana** |
| [ADR-21](adr-21.md) | Dowody z wyszukiwania na żywo w bieżącym sprawdzeniu | **Przyjęta** |
| [ADR-22](adr-22.md) | Pamięć wyników przechowuje tylko część merytoryczną | **Przyjęta** |
| [ADR-23](adr-23.md) | Wstrzyknięcie w treści użytkownika i definicja odpartej próby | **Przyjęta** |
| [ADR-24](adr-24.md) | Fact-checkerzy jako domeny katalogu; Fact Check API tylko do znajdowania adresów | **Przyjęta** |
| [ADR-25](adr-25.md) | Dowód zastąpiony; rozbieżność tylko między dowodami ważnymi w dacie twierdzenia | **Przyjęta** |
| [ADR-26](adr-26.md) | EUvsDisinfo jako lokalna kopia | **Przyjęta** |
| [ADR-27](adr-27.md) | Odtwarzalna ewaluacja: przypięta migawka, nagrane odpowiedzi dostawców, publiczny manifest | **Przyjęta** |
| [ADR-28](adr-28.md) | Ewaluacja w pydantic-evals poza CI, ze stroną ewaluacji w aplikacji | **Przyjęta** |
| [ADR-29](adr-29.md) | Powiadomienia: skrzynka i toasty ze zdarzeń DBOS | **Przyjęta** |
| [ADR-30](adr-30.md) | Weryfikacja nagrań: transkrypcja w regionie UE | **Przyjęta** |
| [ADR-31](adr-31.md) | Magazyn plików: port BlobStore, bucket GCS w UE | **Przyjęta** |
| [ADR-32](adr-32.md) | Korpus jako wycinek w istniejących repozytoriach; narzędzie MCP search\_sources | **Przyjęta** |
| [ADR-33](adr-33.md) | Przypięcie meritum-core i automatyczne podbicia | **Przyjęta** |
| [ADR-34](adr-34.md) | Ocena ClaimReview fact-checkera jako przesłanka werdyktu | **Przyjęta** |
| [ADR-35](adr-35.md) | Klasyfikatory jako tanie bramki przed LLM | **Przyjęta** |
