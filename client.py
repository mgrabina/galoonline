#!/usr/bin/python
from pip._vendor.distlib.compat import raw_input

from src import tcp_client
import sys
import threading
import time
from pip._vendor.distlib.compat import raw_input


# Welcoming player
client = tcp_client.connect()
last_update = time.time()
interval = 0.5
push_started = False
entries = 0



def push_notification(client_conn):
    while True:
        try:
            notification = tcp_client.recv_response(client_conn)
            if notification != "UP TO DATE":
                print(notification)
        except:
            print("some error")
        time.sleep(1)


notifications_thread = threading.Thread(target=push_notification, args=(client,))
notifications_thread.daemon = True
notifications_thread.start()

while True:
    command = raw_input()
    tcp_client.send_msg(client, command)
    response = tcp_client.recv_response(client)
    print(response)
    if str(response).startswith('Bye'):
        exit(0)



