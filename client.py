#!/usr/bin/python
from pip._vendor.distlib.compat import raw_input

from src import tcp_client
import threading

# Welcoming player
client = tcp_client.connect()



def background(client_conn):
    while True:
        try:
            notification = tcp_client.recv_response(client_conn)
            if notification:
                print(notification)
                if str(notification).startswith('Bye'):
                    exit(0)


        except:
            print("Error getting new information.")



def manage_input(client_conn, input):
    tcp_client.send_msg(client, input)


notifications_thread = threading.Thread(target=background, args=(client,))
notifications_thread.daemon = True
notifications_thread.start()


while True:
    command = input()
    if command:
        manage_input(client, command)



