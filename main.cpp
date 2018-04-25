#include <iostream>
#include <random>
#include <vector>
#include <string>
#include <algorithm>

#define TEMPERATURE 4000

void print_chessboard(std::vector<int> chess_board) { // print the chessboard
    for (int queen = 0; queen < chess_board.size(); queen++) {
        std::cout << queen << " => " << chess_board[queen] << "\n";
    }
}

int threat_calculate(int n) { // combination formula for calculate number of pairs of threaten queens
    if (n < 2) {
        return 0;
    }
    if (n == 2) {
        return 1;
    }
    return (n - 1) * n / 2;
}

int randrange(int start, int stop) { // random in a range
    return (int) random() % (stop - start + 1) + start;
}

double uniform() { // random between 0 and 1
    return (double) random() / (double) RAND_MAX;
}

int cost(std::vector<int> chess_board) { // cost function to count total of pairs of threaten queens
    int threat = 0;
    std::vector<int> m_chessboard;
    std::vector<int> a_chessboard;

    for (int queen = 0; queen < chess_board.size(); queen++) {
        m_chessboard.push_back(queen - chess_board[queen]);
        a_chessboard.push_back(queen + chess_board[queen]);
    }

    std::sort(m_chessboard.begin(), m_chessboard.end());
    std::sort(a_chessboard.begin(), a_chessboard.end());

    int m_count = 1;
    while (!m_chessboard.empty()) {
        int temp = m_chessboard[0];
        m_chessboard.erase(m_chessboard.begin());
        if (temp == m_chessboard[0]) {
            m_count += 1;
        } else {
            threat += threat_calculate(m_count);
            m_count = 1;
        }
    }

    int a_count = 1;
    while (!a_chessboard.empty()) {
        int temp = a_chessboard[0];
        a_chessboard.erase(a_chessboard.begin());
        if (temp == a_chessboard[0]) {
            a_count += 1;
        } else {
            threat += threat_calculate(a_count);
            a_count = 1;
        }
    }

    return threat;
}

int main() {
    clock_t start = clock();
    srand((unsigned int) time(nullptr));
    std::random_device rd;
    std::mt19937 g(rd());

    std::vector<int> answer;
    unsigned int n_queens; // number of queens

    std::cout << "Number of queens: ";
    std::cin >> n_queens;

    // create a chess board
    answer.reserve(n_queens);
    for (int i = 0; i < n_queens; i++) { // create a vector from 0 to N_QUEENS - 1
        answer.push_back(i);
    }
    std::shuffle(answer.begin(), answer.end(), g); //shuffle chess board to make sure it is random

    // simulated annealing
    std::vector<int> successor;
    bool solution_found = false;
    double t = TEMPERATURE;
    double sch = 0.99;
    while (t > 0) {
        int rand_col_1;
        int rand_col_2;
        t *= sch;
        successor = answer;
        while (true) { // random 2 queens
            rand_col_1 = randrange(0, n_queens - 1);
            rand_col_2 = randrange(0, n_queens - 1);
            if (rand_col_1 != rand_col_2) break;
        }
        std::swap(successor[rand_col_1], successor[rand_col_2]); // swap two queens chosen
        double delta = cost(successor) - cost(answer);
        if (delta < 0) answer = successor;
        else {
            double p = exp(-delta / t);
            if (uniform() < p) {
                answer = successor;
            }
        }
        if (cost(answer) == 0) {
            solution_found = true;
            print_chessboard(answer);
            break;
        }
    }
    if (!solution_found) std::cout << "Failed";
    std::cout << "Runtime:" << (clock() - start) / 1000000.0 << " second" << std::endl;
}
