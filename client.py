#!/usr/bin/python

from src import tcp_client
import sys
import threading
import time

# Welcoming player
client = tcp_client.connect()
last_update = time.time()
print(last_update)
interval = 0.5
push_started = False
entries = 0

available_commands_string = "Available commands:\n" \
                            "- I AM <username> : register\n" \
                            "- OK? : check status\n" \
                            "- Players : get players list\n" \
                            "- Play <username> : request a new game\n" \
                            "- Accept <username>: accept game\n" \
                            "- Decline <username>: decline game\n" \
                            "- Move <row> <col> : new move\n" \
                            "- exit : exit game\n"
print("Welcome to Galo Online!\n")
print(available_commands_string)


def push_notification(client_conn):
    while True:
        try:
            tcp_client.send_msg(client_conn, "push")
            notification = tcp_client.recv_response(client_conn)
            if notification != "UP TO DATE":
                print(notification)
        except:
            print("some error")
        time.sleep(1)




while True:

    command = input()
    tcp_client.send_msg(client, command)
    response = tcp_client.recv_response(client)
    if "hello" in response.lower() and not push_started:
        notifications_thread = threading.Thread(target=push_notification, args=(client,))
        notifications_thread.daemon = True
        notifications_thread.start()
        push_started = True

    print(response)
    if "exit" in command:
        exit(0)

