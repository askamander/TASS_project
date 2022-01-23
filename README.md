# System rekomendacyjny dla książek z projektu Gutenberg
Treść zadania: Zaprojektuj mechanizm rekomendacji dla projektu Gutenberg- używający dodatkowych informacji o autorach

## Struktura folderów
* data - dane o książkach i autorach oraz oczyszczone dane wykorzystywane bezpośrednio w mechanizmie rekomendacji.
* embeddings - funkcje i skrypty przydatne do przygotowania danych dla systemu rekomendacji.
* gutenberg_authors_parser - skrypty z do parsowania i łączenia danych.
* scrapers - skrypty do pozyskiwania danych.
* tests - testy jednostkowe
* katalog główny - zawiera plik ```main.py```, w którym znajduje się silnik rekomendacyjny wraz z API umożliwającym dostęp do wyników rekomendacji za pomocą statycznej strony HTML.
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

## Wykorzystanie

W celu uruchomienia systemu rekomendacyjnego należy z poziomu katalogu głównego wywołać komendę:
```commandline
python main.py
```
