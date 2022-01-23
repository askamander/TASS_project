# Gutenberg authors data parser
Podprojekt mający na celu sparsowanie danych o autorach tj. wyciągnięcie linków do stron autorów w serwisie Wikipedia a następnie pobranie danych o autorach z bazy danych (zbieraniem danych zajmuje się podprojekt *scrapers*) i połączenie ich z danymi o książkach.
## Gutenberg metadane
Metadane o książkach zostały pobrane ze strony [Gutenberg feed page](https://www.gutenberg.org/cache/epub/feeds/) w formacie RDF (rdf-files.tar.zip).

## Struktura folderów
* data - dane o książkach i autorach oraz skrypt do pobierania danych z DynamoDB `dynamodb_dump.sh`. Dane są w wielu plikach co wynika z pozostawieniu plików pośrednich z działania skryptów z do parsowania i łączenia danych. Przykładowo pliki `unique_authors_wiki_<cyfra>.csv` dzielą zbiór przeznaczony dla *scraper-ów*, ponieważ lambda ma ograniczony czas działania.
* gutenberg_parser - skrypty z do parsowania i łączenia danych.
* katalog główny - poza wspomnianymi folderami, zawiera pliki konfiguracyjne i dokumentacyjne.

## Instalacja
Aby stworzyć i aktywować [virtual environnement](https://docs.python.org/3/tutorial/venv.html) wykonaj komendę:
```
# Create venv
python3 -m venv venv

# Activate venv
source venv/bin/activate
```

Wymagana wersja pythona to **>=3.7**.

Wszystkie zależności wymagane do uruchomienia projektu znajdują się w pliku `requirements.txt`. Aby zainstalować zależności wykonaj komendę:
```
pip install -r requirements.txt
```

W przypadku zadań developerskich należy zainstalować zależności z pliku `requirements-dev.txt`.
## Zbiór wynikowy
Plik `pg_authors.csv` w folderze `data` zawiera finalną wersję danych o książkach wzbogaconą o dane o autorach.
