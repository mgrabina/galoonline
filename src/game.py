import numpy as np


class Game:
    board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    symbols = {}
    moves = 0
    positions = {}
    active = ''

    def rand_symbols(self):
        rand = np.random.randint(2, size=1)
        if rand:
            self.symbols[self.requester_username] = 'X'
            self.symbols[self.opponent_username] = 'O'
        else:
            self.symbols[self.requester_username] = 'O'
            self.symbols[self.opponent_username] = 'X'

    def rand_active(self):
        rand = np.random.randint(2, size=1)
        if rand:
            self.active = self.requester_username
        else:
            self.active = self.opponent_username

    def __init__(self, requester_connection, opponent_connection, requester_username, opponent_username):
        self.requester_connection = requester_connection
        self.opponent_connection = opponent_connection
        self.requester_username = requester_username
        self.opponent_username = opponent_username
        self.rand_symbols()
        self.rand_active()

    def change_turn(self):
        if self.active == self.requester_username:
            self.active = self.opponent_username
        else:
            self.active = self.requester_username

    def username_by_symbol(self, symbol):
        for key in self.symbols:
            if self.symbols[key] == symbol:
                return key

