## moh
import socket

# Constants
HOST = '127.0.0.1'
PORT = 9090

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    username = input("Enter your username: ")
    client_socket.send(username.encode())

    while True:
        print("\nMenu:")
        print("1. Get Arrived Flights")
        print("2. Get Delayed Flights")
        print("3. Get Flight Details")
        print("4. Quit")
        choice = input("Select an option (1-4): ")

        client_socket.send(choice.encode())

        if choice == '1':
            response = client_socket.recv(4096).decode()
            print("\nArrived Flights:\n", response)

        elif choice == '2':
            response = client_socket.recv(4096).decode()
            print("\nDelayed Flights:\n", response)

        elif choice == '3':
            flight_code = input("Enter flight IATA code: ")
            client_socket.send(flight_code.encode())
            response = client_socket.recv(4096).decode()
            print("\nFlight Details:\n", response)

        elif choice == '4':
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

    client_socket.close()
if __name__ == "__main__":
    main()