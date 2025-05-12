# server.py
import socket
import threading
import requests
import json

# Constants
HOST = '127.0.0.1'
PORT = 9090
API_KEY = '1d14536c4196c2d80900fd9ac26fb84a'
GROUP_ID = 'SA13'
DATA_FILE = f'{GROUP_ID}.json'


def fetch_flight_data(icao_code):
    url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&arr_icao={icao_code}&limit=100"
    response = requests.get(url)
    data = response.json()
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    return data


def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def handle_client(client_socket, address, username):
    print(f"[+] Connected with {username} at {address}")
    data = load_data()['data']

    try:
        while True:
            request = client_socket.recv(1024).decode().strip()

            if request == '1':  # Arrived flights
                response = ""
                for flight in data:
                    if flight['arrival']['actual'] is not None:
                        response += f"Flight: {flight['flight']['iata']}, From: {flight['departure']['airport']}, Time: {flight['arrival']['actual']}, Terminal: {flight['arrival']['terminal']}, Gate: {flight['arrival']['gate']}\n"
                client_socket.send(response.encode() if response else b"No arrived flights found.\n")

            elif request == '2':  # Delayed flights
                response = ""
                for flight in data:
                    if flight['arrival']['delay']:
                        response += f"Flight: {flight['flight']['iata']}, From: {flight['departure']['airport']}, Dep Time: {flight['departure']['scheduled']}, ETA: {flight['arrival']['estimated']}, Delay: {flight['arrival']['delay']} mins, Terminal: {flight['arrival']['terminal']}, Gate: {flight['arrival']['gate']}\n"
                client_socket.send(response.encode() if response else b"No delayed flights found.\n")

            elif request == '3':  # Flight details
                client_socket.send(b"Enter flight IATA code: ")
                code = client_socket.recv(1024).decode().strip()
                found = False
                for flight in data:
                    if flight['flight']['iata'] == code:
                        found = True
                        details = f"Flight: {code}\nFrom: {flight['departure']['airport']}, Terminal: {flight['departure']['terminal']}, Gate: {flight['departure']['gate']}\nTo: {flight['arrival']['airport']}, Terminal: {flight['arrival']['terminal']}, Gate: {flight['arrival']['gate']}\nStatus: {flight['flight_status']}\nScheduled Departure: {flight['departure']['scheduled']}\nScheduled Arrival: {flight['arrival']['scheduled']}\n"
                        client_socket.send(details.encode())
                        break
                if not found:
                    client_socket.send(b"Flight not found.\n")

            elif request == '4':
                client_socket.send(b"Goodbye!\n")
                break
            else:
                client_socket.send(b"Invalid option.\n")
    finally:
        print(f"[-] Disconnected: {username}")
        client_socket.close()


def main():
    icao_code = input("Enter ICAO code of airport (e.g., OBBI): ").upper()
    print("[*] Fetching flight data...")
    fetch_flight_data(icao_code)
    print("[*] Data saved to", DATA_FILE)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Server listening on {HOST}:{PORT}...")

    while True:
        client_sock, addr = server.accept()
        client_sock.send(b"Enter your username: ")
        username = client_sock.recv(1024).decode().strip()
        threading.Thread(target=handle_client, args=(client_sock, addr, username)).start()


if __name__ == "__main__":
    main()
