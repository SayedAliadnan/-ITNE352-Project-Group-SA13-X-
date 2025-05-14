##SAYED ALI ADNAN 202109837

# server.py
import socket
import threading
import requests
import json

# Constants 
# ثوابت الاتصال
HOST = '127.0.0.1' # عنوان السيرفر
PORT = 9090 # رقم المنفذ
API_KEY = '1d14536c4196c2d80900fd9ac26fb84a' # مفتاح API حق aviationstack
GROUP_ID = 'SA13' # معرف المجموعة
DATA_FILE = f'{GROUP_ID}.json' # اسم ملف البيانات

def fetch_flight_data(icao_code): # المثود هذي تجيب بيانات الرحلات من API
    url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&arr_icao={icao_code}&limit=100" # هنا نكون حطينا رابط API
    response = requests.get(url) # هنا نسوي طلب للAPI
    data = response.json() # هنا نحول البيانات الي جابها لنا من API الى JSON
    with open(DATA_FILE, 'w') as f: # هنا نكتب البيانات الي جابها لنا في ملف
        json.dump(data, f, indent=4) # هنا نستخدم indent عشان يكون شكل البيانات مرتب
    return data # هنا نكون حطينا رابط API

def load_data(): # المثود هذي تقرا البيانات من ملف
    with open(DATA_FILE, 'r') as f: # هنا نفتح الملف
        return json.load(f) # هنا نستخدم load عشان نحول البيانات من JSON الى Python dict

def handle_client(client_socket, address, username): # المثود هذي تتعامل مع كل كلاينت
    print(f"[+] Connected with {username} at {address}") # هنا نطبع اسم الكلاينت الي اتصل
    data = load_data()['data'] # هنا نستخدم load_data عشان نحمل البيانات من الملف

    try: # هنا نستخدم try عشان لو صار خطا في الاتصال نقدر نتعامل معاه
        while True: # هنا نبدي لووب عشان ننتظر من الكلاينت يرسل طلب
                        # ننتظر من الكلاينت يرسل خيار من القائمة
            request = client_socket.recv(1024).decode().strip() # هنا ناخذ الخيار الي اختاره الكلاينت

            if request == '1': # الرحلات الي وصلت
                response = "" # هنا نكون حطينا متغير فاضي عشان نستخدمه لاحقا
                for flight in data: # هنا نستخدم لووب عشان نبحث في البيانات الي جبناها من API
                    if flight['flight_status'] == "landed": # هنا نبحث عن الرحلات الي وصلت
                        response += f"Flight: {flight['flight']['iata']}, From: {flight['departure']['airport']}, Time: {flight['arrival']['actual']}, Terminal: {flight['arrival']['terminal']}, Gate: {flight['arrival']['gate']}\n"
                client_socket.send(response.encode() if response else b"No arrived flights found.\n") # هنا نرسل البيانات للكلاينت

            elif request == '2': # الرحلات المتأخرة
                response = "" # هنا نكون حطينا متغير فاضي عشان نستخدمه لاحقا
                for flight in data:     # هنا نستخدم لووب عشان نبحث في البيانات الي جبناها من API
                    if flight['arrival']['delay']: # هنا نبحث عن الرحلات المتأخرة
                        response += f"Flight: {flight['flight']['iata']}, From: {flight['departure']['airport']}, Dep Time: {flight['departure']['scheduled']}, ETA: {flight['arrival']['estimated']}, Delay: {flight['arrival']['delay']} mins, Terminal: {flight['arrival']['terminal']}, Gate: {flight['arrival']['gate']}\n"
                client_socket.send(response.encode() if response else b"No delayed flights found.\n")       # هنا نرسل البيانات للكلاينت    

            elif request == '3':  # Flight details تفاصيل الرحلة
                code = client_socket.recv(1024).decode().strip()# هني ناخذ كود الرحلة من الكلاينت
                found = False# اهني نبي نشوف اذا الكود موجود ولا لا
                for flight in data: # اهني نبحث في البيانات الي جبناها من API
                    if flight['flight']['iata'] == code: # اهني نشوف اذا الكود موجود ولا لا
                        found = True    # اهني نكون حطينا متغير فاضي عشان نستخدمه لاحقا
                        details = f"Flight: {code}\nFrom: {flight['departure']['airport']}, Terminal: {flight['departure']['terminal']}, Gate: {flight['departure']['gate']}\nTo: {flight['arrival']['airport']}, Terminal: {flight['arrival']['terminal']}, Gate: {flight['arrival']['gate']}\nStatus: {flight['flight_status']}\nScheduled Departure: {flight['departure']['scheduled']}\nScheduled Arrival: {flight['arrival']['scheduled']}\n"
                        client_socket.send(details.encode()) # اهني نرسل تفاصيل الرحلة للكلاينت
                        break  # اهني نوقف اللووب بعد ما نلقى الرحلة
                if not found: # اهني لو ما لقينا الرحلة
                    client_socket.send(b"Flight not found.\n") # اهني نرسل رسالة للكلاينت ان الرحلة مو موجودة

            elif request == '4': # الكلاينت خلص ويبغي يطلع
                client_socket.send(b"Goodbye!\n") # اهني نرسل رسالة للكلاينت اننا بنقفل الاتصال
                break # اهني نوقف اللووب
            else: # اهني لو الكلاينت كتب شي مو موجود في القائمة
                client_socket.send(b"Invalid option.\n") #هني لو خربط الكلاينت وكتب شي غلط 
    finally: # اهني نستخدم finally عشان نتأكد اننا بنقفل الاتصال حتى لو صار خطا
        print(f"[-] Disconnected: {username}") # اهني نطبع اسم الكلاينت الي اتصل
        client_socket.close() # اهني نغلق الاتصال على الكلاينت 

def main():     
    icao_code = input("Enter ICAO code of airport (e.g., OBBI): ").upper() # (المستخدم)اهني ناخذ كود المطار من لكلاينت
    print("[*] Fetching flight data...") # اهني نطبع رسالة اننا بنجيب بيانات الرحلات
    fetch_flight_data(icao_code) #اهني ناخذ بيانات الرحلات 
    print("[*] Data saved to", DATA_FILE)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# اهني انسوي سوكيت ويكون TCP
    server.bind((HOST, PORT)) #اهني نربط السوكيت بل العنوان 
    server.listen(5)#اهني نبدي الاستماع للاتصالات 
    print(f"[*] Server listening on {HOST}:{PORT}...") # اهني نطبع رسالة ان السيرفر قاعد يستمع للاتصالات

    while True: # اهني نبدي لووب عشان نستقبل الاتصالات
        client_sock, addr = server.accept() #نستقبل  اي كلاينت جديد 
        username = client_sock.recv(1024).decode().strip()#هني اول شي لكلاينت يرسل اسمه 
        threading.Thread(target=handle_client, args=(client_sock, addr, username)).start() # اهني نستخدم threading عشان نتعامل مع كل كلاينت في خيط خاص فيه


if __name__ == "__main__": # اهني نستخدم __name__ عشان نتأكد اننا بنشغل السيرفر بس لو كنا نشغل الملف هذا
    main()# اهني نبدي السيرفر
