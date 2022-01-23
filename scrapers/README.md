# Scrapers
Podprojekt odpowiedzialny za scraping i pobranie danych z sieci. Projekt ten realizuje następujące funkcjonalności:
* przejście na stronę Wikipedii i ekstrakcja ID encji w serwisie Wikidata.
* Wysłanie zapytania SPQRQL do API Wikidata.
* Zapis danych do bazy danych.

Projekt został zrealizowany z wykorzystaniem serwisów AWS, co umożliwiło uniknięcie zablokowania IP przypisanego do lokalnego komputera.

## Wykorzystane serwisy AWS
* AWS Lambda - serverless-owa, oparta na event-ach, platforma obliczeniowa. Ów serwis wykonuje zdefiniowany przez użytkownika kod w odpowiedzi na przychodzące do niej event-y.
* AWS DynamoDB - serverless-owa baza NoSQL.

### Lambdy
Na potrzeby realizacji zadania zaimplementowano cztery lambdy:
* *wikipedia_scraper_orchestrator* - ma za zadanie wczytać plik z linkami do Wikipedii i rozdystrybuować je do do lambdy *wikipedia_scraper*. Dystrybucja zadań opiera się o wysłanie event-u, a AWS zajmuje się skalowaniem/replikacją lambd.
* *wikipedia_scraper* - pobiera kod strony autora na Wikipedii i wyciąga z niej ID encji na Wikidata.
* *query_wikidata* - wykonuje zapytanie SPARQL do API Wikidata, pobierając wymagane dane.
* *save_data* - zapisuje dane do DynamoDB.

Wspomniane lambdy działają w taki sposób, że jedna wywołuję kolejną przekazując jej swoje dane. Takim sposobem lambda odpowiedzialna za zapis otrzymuje pełen zestaw danych.

### DynamoDB
Po tym jak dane trafią do bazy danych wyciągane są do formatu txt (ogranicznik to Tab), co dzieje się za sprawą skryptu `dynamodb_dump.sh` znajdującego się w folderze `gutenberg_authors_parser/data` (sąsiadujący podprojekt). Do poprawnego działania skryptu wymagane jest poprawnie skonfigurowane [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html).

## Struktura folderów
* bin - zawiera pliki, które inicjalizują zdefiniowaną infrastrukturę (dostarczają danych do konta AWS, na którym ma zostać uruchomiona dana infrastruktura).
* lib - pliki, które definiują infrastrukturę.
* lambda - kod źródłowy lambd wykorzystanych w projekcie - każdy podfolder odnosi się do jednej lambdy.
* katalog główny - poza wspomnianymi folderami, zawiera pliki konfiguracyjne i dokumentacyjne.

## Przydatne komendy

 * `npm install` - instalacja wymaganych zależności.
 * `npm run build` - transpilacja TypeScript-u do JavaScript-u.
 * `npm run watch` - uruchomienie obserwacji zmian i transpilacja.
 * `npm run test` - wykonanie testów jednostkowych.
 * `cdk deploy` - deploy infrastruktury do AWS.
 * `cdk diff` - porównanie lokalnej infrastruktury z wersją obecną na AWS.
 * `cdk synth` - zwrócenie szablonu infrastruktury w formacie CloudFormation.
