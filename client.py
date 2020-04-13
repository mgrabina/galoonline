#!/usr/bin/python

from src import tcp_client

# Welcoming player
client = tcp_client.connect()

available_commands_string = "Available commands:\n" \
       "- I AM <username> : register\n"\
       "- OK? : check status\n"\
       "- Players : get players list\n"\
       "- Play <username> : request a new game\n"\
       "- Accept : accept game\n"\
       "- Decline : decline game\n"\
       "- Move <row> <col> : new move\n"\
       "- exit : exit game\n"
print ("Welcome to Galo Online!\n")
print (available_commands_string)

while True:
    command = input()
    tcp_client.send_msg(client, command)
    print(tcp_client.recv_response(client))
    if "exit" in command:
        exit(0)
