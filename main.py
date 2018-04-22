import random
from math import factorial, exp
import time
from copy import deepcopy

N_QUEENS = 8
TEMPERATURE = 4000


def create_board(n):
    '''Create a chess boad with each queen on a row'''
    chess_board = {}
    temp = list(range(n))
    random.shuffle(temp)
    column = 0

    while len(temp) > 0:
        row = random.choice(temp)
        chess_board[column] = row
        temp.remove(row)
        column += 1
    del temp
    return chess_board


def cost(chess_board):
    '''Calculate how many pairs queen threatened each other'''
    threat = 0
    m_chessboard = dict()
    a_chessboard = dict()

    for column in chess_board:
        temp_m = column - chess_board[column]
        temp_a = column + chess_board[column]
        if temp_m not in m_chessboard:
            m_chessboard[temp_m] = 1
        else:
            m_chessboard[temp_m] += 1
        if temp_a not in a_chessboard:
            a_chessboard[temp_a] = 1
        else:
            a_chessboard[temp_a] += 1

    for i in m_chessboard:
        count_i = m_chessboard[i]
        if count_i == 1:
            continue
        else:
            temp = factorial(count_i) / (factorial(2) * factorial(count_i - 2))
            threat += int(temp)
    del m_chessboard

    for i in a_chessboard:
        count_i = a_chessboard[i]
        if count_i == 1:
            continue
        else:
            temp = factorial(count_i) / (factorial(2) * factorial(count_i - 2))
            threat += int(temp)
    del a_chessboard

    return threat


def simulated_annealing():
    solution_found = False
    answer = create_board(N_QUEENS)
    t = TEMPERATURE
    sch = 0.99

    while t > 0:
        t *= sch
        successor = deepcopy(answer)
        while True:
            index_1 = random.randrange(0, N_QUEENS - 1)
            index_2 = random.randrange(0, N_QUEENS - 1)
            if index_1 != index_2:
                break
        successor[index_1], successor[index_2] = successor[index_2], \
            successor[index_1]
        delta = cost(successor) - cost(answer)
        if delta < 0:
            answer = deepcopy(successor)
        else:
            p = exp(-delta / t)
            if random.uniform(0, 1) < p:
                answer = deepcopy(successor)
        if cost(answer) == 0:
            solution_found = True
            print_chess_board(answer)
            break
    if solution_found is False:
        print("Failed")


def print_chess_board(board):
    for column, row in board.items():
        print(column, row)


def main():
    start = time.time()
    simulated_annealing()
    print(time.time() - start)


if __name__ == "__main__":
    main()
