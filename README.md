# Multithreaded Flight arrival Client/Server Information System

## Project Description:
The Multithreaded Flight Arrival Client/Server Information System is a Python-based application designed to provide real-time flight status updates using the AviationStack API. The system consists of a server application (sayed.py) and a client application (mClient.py). The server connects to the AviationStack API to fetch the latest flight data, manages multiple client connections simultaneously through multithreading, and stores the retrieved flight information in JSON format for efficient access. Clients interact with the system via a command-line interface, where they can view lists of arrived or delayed flights, search for specific flights by their code, and receive up-to-date information. The client-server architecture ensures that multiple users can access flight data concurrently, making the system suitable for environments where timely and accurate flight information is essential.  

## Semester
Second Semester 2024/2025

## group members
* Group Name: SA13
* course code: ITNE352
* sec: 01
* SAYED ALI ADNAN 202109837 
* mohammed

## table of contents
1. [Project Description](#project-description)
2. [requirements](#requirements)
3. [how to run the project](#how-to-run-the-project)
   * [run the server code](#run-the-server-code)
   * [run the client code](#run-the-client-code)
4. [API Key](#api-key)









## requirements
* Python 3.x
* install the required libraries using pip:
```bash
pip install requests
```
# how to run the project
## run the server code
1. Open a terminal and navigate to the directory where the server code (sayed.py) is located.
2. Run the server code using the following command:
```bash
python sayed.py
```
3. The server will start listening for incoming client connections on the specified host and port (default is localhost:'127.0.0.1').
4. The server will fetch flight data from the AviationStack API and store it in a JSON file (flights.json) for efficient access.
5. The server will handle multiple client connections simultaneously using multithreading.

## run the client code
1. Open a new terminal and navigate to the directory where the client code (mClient.py) is located.
2. Run the client code using the following command:
```bash
python mClient.py
```
3. The client will connect to the server and display a menu with options to view arrived flights, delayed flights, search for a flight by code, or exit the program.
4. The client will send requests to the server based on user input and display the corresponding flight information.


## API Key
API URL: http://api.aviationstack.com/v1/flights?access_key

API Key: 1d14536c4196c2d80900fd9ac26fb84a




