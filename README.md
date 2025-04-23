
# Quiz Multiplayer z GUI

## Opis projektu

Aplikacja składa się z dwóch komponentów:

1. **Serwer TCP** – obsługuje dwie gry jednocześnie. Pobiera pytania z Open Trivia API i zarządza logiką gry.
2. **Klient GUI** – oparty na `tkinter`, umożliwia użytkownikowi udział w quizie w interfejsie graficznym.

Gra składa się z 5 rund, w których gracze odpowiadają na pytania wielokrotnego wyboru.

## Technologie

- Python 3.x
- Sockets (`socket`)
- Wielowątkowość (`threading`)
- GUI: `tkinter`
- API: [Open Trivia DB](https://opentdb.com/)
- `requests`, `json`, `random`

## Uruchamianie aplikacji

### Krok 1: Uruchomienie serwera

```bash
python server.py
```

Serwer nasłuchuje połączeń na porcie `5678` na `localhost`. Oczekuje dwóch graczy.

### Krok 2: Uruchomienie klienta

Na dwóch oddzielnych instancjach terminala/komputerów:

```bash
python client.py
```

Aplikacja klienta uruchamia GUI z możliwością odpowiadania na pytania.

## Szczegóły działania

### Serwer (`server.py`)

- Oczekuje na połączenie dwóch klientów.
- Pobiera pytania z Open Trivia DB.
- Losuje kolejność odpowiedzi.
- Przesyła pytania i możliwe odpowiedzi do klientów.
- Odbiera odpowiedzi od klientów.
- Oblicza punkty i wysyła podsumowanie wyników.

### Klient (`client.py`)

- Łączy się z serwerem.
- Wyświetla pytania i odpowiedzi w GUI.
- Umożliwia przesłanie odpowiedzi numerycznej.
- Wyświetla wyniki każdej rundy i podsumowanie końcowe.

## Wymagania

Zainstaluj wymagane biblioteki:

```bash
pip install requests
```

Moduły `tkinter`, `socket`, `threading`, `random`, `json` są standardowe i dostępne w Pythonie 3.x.

## Uwagi

- Aplikacja działa wyłącznie lokalnie (`localhost`), ale może zostać zmodyfikowana do pracy w sieci.
- Należy uruchomić serwer jako pierwszy, przed klientami.
- Gra nie obsługuje ponownego dołączania graczy ani większej liczby uczestników.
