#!/usr/bin/python

from src import tcp_server


def client_handler(connection):
    msg = tcp_server.recv_msg(connection)
    print('Received {}'.format(msg))

    msg_to_client = 'OK ' + msg
    tcp_server.send_msg(connection, msg_to_client)


server = tcp_server.start_server()
while True:
    connection = tcp_server.connect(server)
    tcp_server.start_handler(client_handler, connection)
