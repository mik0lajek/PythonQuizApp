import socket
import threading
import requests
import json
import random

# Funkcja pobierająca pytania z Open Trivia API
def get_question():
    url = "https://opentdb.com/api.php?amount=1&type=multiple"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Ładnie formatuje wynik
        pretty_json = json.dumps(data, indent=4)
        print(pretty_json)

        question_data = data['results'][0]

        question = question_data['question']
        correct_answer = question_data['correct_answer']
        incorrect_answers = question_data['incorrect_answers']
        options = incorrect_answers + [correct_answer]
        random.shuffle(options)

        return question, options, correct_answer
    else:
        return None, None, None

# Inicjalizacja serwera
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5678)
server_socket.bind(server_address)
server_socket.listen(2)
print("Czekam na dwóch graczy...")

# Akceptowanie dwóch klientów
clients = []
for i in range(2):
    client_socket, client_address = server_socket.accept()
    print(f"Gracz {i + 1} połączony: {client_address}")
    clients.append(client_socket)

# Funkcja obsługująca grę quiz
def quiz_game():
    scores = [0, 0]  # Wyniki graczy

    for round_num in range(5):  # 5 rund gry
        question, options, correct_answer = get_question()

        if not question:
            print("Błąd podczas pobierania pytania.")
            break

        # Wysłanie pytania i opcji do graczy
        question_message = f"Pytanie {round_num + 1}: {question}\n"
        for i, option in enumerate(options):
            question_message += f"{i + 1}. {option}\n"
        for client in clients:
            client.send(question_message.encode('utf-8'))

        # Odbieranie odpowiedzi od graczy
        answers = []
        for i, client in enumerate(clients):
            try:
                answer = int(client.recv(1024).decode('utf-8').strip())
                answers.append((i, answer))
            except ValueError:
                answers.append((i, None))

        # Sprawdzanie odpowiedzi
        for player, answer in answers:
            if answer and 0 < answer <= len(options) and options[answer - 1] == correct_answer:
                scores[player] += 1

        # Informowanie graczy o prawidłowej odpowiedzi
        correct_message = f"Prawidłowa odpowiedź: {correct_answer}\n"
        for client in clients:
            client.send(correct_message.encode('utf-8'))

    # Wyświetlenie wyników
    results_message = "\nWyniki końcowe:\n"
    for i, score in enumerate(scores):
        results_message += f"Gracz {i + 1}: {score} punktów\n"

    if scores[0] > scores[1]:
        results_message += "Gracz 1 wygrywa!\n"
    elif scores[1] > scores[0]:
        results_message += "Gracz 2 wygrywa!\n"
    else:
        results_message += "Remis!\n"

    for client in clients:
        client.send(results_message.encode('utf-8'))

    # Zamykanie połączenia
    for client in clients:
        client.close()

# Rozpoczęcie gry w osobnym wątku
quiz_thread = threading.Thread(target=quiz_game)
quiz_thread.start()
quiz_thread.join()

server_socket.close()
