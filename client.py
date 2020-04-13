#!/usr/bin/python

from src import tcp_client

# Welcoming player
client = tcp_client.connect()

print ("Welcome to Galo Online!\n")
print ("Please enter a name to register\n")
username = input()

tcp_client.send_msg(client, username)
print(tcp_client.recv_response(client))
