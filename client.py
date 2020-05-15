#!/usr/bin/python
import os
from src import tcp_client
import threading

# Welcoming player
client = tcp_client.connect()



def background(client_conn):
    while True:
        notification = None
        try:
            notification = tcp_client.recv_response(client_conn)

        except:
            print("Error getting new information.")

        if notification:
            print(notification)
            if str(notification).startswith('Bye'):
                os._exit(0)



def manage_input(client_conn, input):
    tcp_client.send_msg(client, input)


notifications_thread = threading.Thread(target=background, args=(client,))
notifications_thread.daemon = True
notifications_thread.start()


while True:
    command = input()
    if command:
        manage_input(client, command)



