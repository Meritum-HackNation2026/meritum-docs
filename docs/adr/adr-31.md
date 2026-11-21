# ADR-31. Magazyn plików: port BlobStore, bucket GCS w UE

<!-- Wygenerowane przez scripts/generate.py. Nie edytuj ręcznie: zmiany przepadną przy następnym odświeżeniu. -->

**Status:** Przyjęta

## Kontekst

Weryfikacja nagrań jest w MVP ([ADR-30](adr-30.md)), a obrazy dodamy, jeśli starczy czasu (US-SPR-08). Synchroniczne rozpoznawanie Speech-to-Text przyjmuje nagrania do około minuty; dłuższe idą przez rozpoznawanie wsadowe, które czyta pliki z Cloud Storage (gs://). Linki do załączników Discorda wygasają, więc przez czas życia sprawdzenia trzymamy własną kopię pliku. Przesłane pliki podlegają zasadom retencji i usuwania z [ADR-13](adr-13.md).

## Decyzja

Port BlobStore w meritum-core; pliki adresujemy przez audio\_id i image\_id z CheckRequest. Za portem są trzy adaptery. Docelowe wdrożenie używa prywatnego bucketu Cloud Storage w europe-central2 z jednolitym dostępem, do którego dostęp mają tylko konta usługowe backendu i workera. Reguła cyklu życia usuwa obiekty po 30 dniach, czyli po tym samym czasie co zapis sprawdzenia, a „Usuń moje sprawdzenia” usuwa też pliki. Bucket zakładamy Terraformem w meritum-infra. Na serwerze zespołu, lokalnie i we własnych przyszłych wdrożeniach działa adapter systemu plików na wolumenie. Do samodzielnego hostowania służy adapter magazynu zgodnego z S3, np. Garage albo SeaweedFS. Cloud Storage też obsługuje API S3 z kluczami HMAC.

## Konsekwencje

Retencję pilnuje reguła cyklu życia, bez własnego zadania usuwania, a pliki zostają w UE. **Ryzyko:** nie potwierdziliśmy, że rozpoznawanie wsadowe w multi-regionie eu czyta pliki z bucketu w europe-central2 (załącznik B). Limity rozmiaru i formatu pliku trzeba sprawdzać przy przesyłaniu.

## Alternatywy

Pliki jako bytea w PostgreSQL; linki do CDN Discorda; MinIO (wersja społecznościowa weszła w 2025 r. w tryb utrzymania, załącznik B).
