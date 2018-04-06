import random
import math
import decimal
import time

N_QUEENS = 8


# Create N x N chess board
def create_board(N_QUEENS):
    queens = []
    for i in range(N_QUEENS):
        queens.append(random.randint(1, N_QUEENS))
    return queens


# Cost function
def cost(queens):
    h = 0
    for i in range(len(queens)):
        for j in range(i + 1, len(queens)):
            # Queens are in the same row
            if queens[i] == queens[j]:
                h += 1
            offset = j - i
            # Queens are in the same diagonal
            if queens[i] == queens[j] - offset \
                or queens[i] == queens[j] + offset:
                h += 1
    return h


def simulated_annealing():
    solution_found = False
    answer = create_board(N_QUEENS)
    temperature = 4000

    while temperature > 0:
        temperature *= 0.99
        successor_queen = answer[:]
        successor_queen[random.randint(0, N_QUEENS - 1)] = random.randint(1, N_QUEENS)
        delta = cost(successor_queen) - cost(answer)

        if delta < 0:
            answer = successor_queen[:]
        else:
            p = math.exp(-delta / temperature)
            if random.uniform(0, 1) < p:
                answer = successor_queen[:]

        if cost(answer) == 0:
            solution_found = True
            print_chessboard(answer)
            break

    if solution_found is False:
        print("Failed", answer)


def print_chessboard(answer):
    for row in list(enumerate(answer, start=1)):
        print(row)


def main():
    start = time.time()
    simulated_annealing()
    print(time.time() - start)


if __name__ == "__main__":
    main()
