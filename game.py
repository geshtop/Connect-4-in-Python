import copy
import alphaBetaPruning
import random

VICTORY = 10 ** 20  # The value of a winning board (for max)
LOSS = -VICTORY  # The value of a losing board (for max)
TIE = 0  # The value of a tie
SIZE = 4  # the length of winning seq.
COMPUTER = SIZE + 1  # Marks the computer's cells on the board
HUMAN = 1  # Marks the human's cells on the board

rows = 6
columns = 7


class game:
    board = []
    size = rows * columns
    playTurn = HUMAN

    # Used by alpha-beta pruning to allow pruning

    '''
    The state of the game is represented by a list of 4 items:
        0. The game board - a matrix (list of lists) of ints. Empty cells = 0,
        the comp's cells = COMPUTER and the human's = HUMAN
        1. The heuristic value of the state.
        2. Whose turn is it: HUMAN or COMPUTER
        3. Number of empty cells
    '''


def create(s) :
    # Returns an empty board. The human plays first.
    # create the board
    s.board = []
    for i in range(rows) :
        s.board = s.board + [columns * [0]]

    s.playTurn = HUMAN
    s.size = rows * columns
    s.val = 0.00001

    # return [board, 0.00001, playTurn, r*c]     # 0 is TIE


def cpy(s1) :
    # construct a parent DataFrame instance
    s2 = game()
    s2.playTurn = s1.playTurn
    s2.size = s1.size
    s2.board = copy.deepcopy(s1.board)
    #print("board ", s2.board)
    return s2


def value(s):
    print("Value", s.board)
    # Returns the heuristic value of s
    if check_single_victory(s, SIZE, 0):  # בדיקת ניצחון לרצף כל שהוא, בהתחלה זה ל-4
        if s.playTurn == HUMAN:  # המחשב ניצח
            return VICTORY
        else:  # השחקן ניצח
            return LOSS
    elif s.size == 0:  # תיקו
        return TIE  # or return 0-- no better
    else:
        return our_goual(s)


def our_goual(s):


    if check_single_victory(s, SIZE - 1, HUMAN):  # ליריב בדיקת רצף 3
        if s.playTurn == HUMAN:  # למחשב יש רצף
            return 0.15 * 10  # מתקבל ערך ללוח
        elif s.playTurn == COMPUTER:  # לשחקן יש רצף
            return 0.03 * 10  # הערך ללוח יהיה יותר קטן

    #מדובר פה לאחר שאלפאביתא כבר דאג לשכפל את הלוח ולהכניס לעמודה X ולכן נבדוק עכשיו אם יש רצפים אחרים
    if check_single_victory(s, SIZE - 1, 0): #בדיקת רצף 3
        if s.playTurn == HUMAN :  # למחשב יש רצף
            return 0.15 * 10 #מתקבל ערך ללוח
        elif s.playTurn == COMPUTER:   #לשחקן יש רצף
            return 0.03 * 10 #הערך ללוח יהיה יותר קטן

    if check_single_victory(s, SIZE - 2 , 0): #אם אין רצף 3, בדיקת רצף 2
        if s.playTurn == HUMAN :  # המחשב ניצח
            return 0.1 * 10  # מתקבל ערך ללוח
        elif s.playTurn == COMPUTER :  # לשחקן יש רצף
            return 0.02 * 10  # הערך ללוח יהיה יותר קטן

    if check_single_victory(s, SIZE - 3 , 0): #כשאין רצף 2 בלוח נבדוק איפה
        if s.playTurn == HUMAN :  # המחשב ניצח
            return 0.05 * 10  # מתקבל ערך ללוח
        elif s.playTurn == COMPUTER :  # לשחקן יש רצף
            return 0.01 * 10  # הערך ללוח יהיה יותר קטן

# פונקציה הבודקת אם קיים רצף של size
def check_single_victory(s, size, user):
    if find_horizontal(s, size, user) or find_vertical(s, size, user) or find_pos_diagonal(s, size, user) or find_neg_diagonal(s, size, user):
        return True
    return False


def find_horizontal(s, size, user):
    if size > SIZE:
        size = SIZE
    delta = SIZE - size
    delta_total = 0
    for i in range(rows):
        for j in range(columns + 1 - size):
            num1 = 0
            for k in range(size):
                num1 = num1 + s.board[i][j + k]
            if delta > 0 :
                for d in range(delta):
                    delta_total = delta_total + s.board[i][size +  delta]
                print (delta_total)
            if (user == 0 or user == COMPUTER) and num1 == COMPUTER * size and delta_total == 0 :
                return True
            if (user  == 0 or user == HUMAN) and num1 == HUMAN * size and delta_total == 0:
                return True
    return False


def find_vertical(s, size, user):
    if size > SIZE:
        size = SIZE
    delta = SIZE - size
    delta_total = 0
    for i in range(rows + 1 - size):
        for j in range(columns):
            num2 = 0
            for k in range(size):
                num2 = num2 + s.board[i + k][j]
            if delta > 0:
                for d in range(delta):
                    delta_total = delta_total + s.board[size + delta][j]
            if (user == 0 or user == COMPUTER) and num2 == COMPUTER * size:
                return True
            if (user  == 0 or user == HUMAN) and num2 == HUMAN * size:
                return True
    return False


def find_pos_diagonal(s, size ,user):
    if size > SIZE:
        size = SIZE
    delta = SIZE - size
    delta_total = 0
    for i in range(rows + 1 - size):
        for j in range(size - 1, columns):
            num3 = 0
            for k in range(size):
                num3 = num3 + s.board[i + k][j - k]
                if (user == 0 or user == COMPUTER) and num3 == COMPUTER * size:
                    return True
                if (user  == 0 or user == HUMAN) and num3 == HUMAN * size:
                    return True
    return False


def find_neg_diagonal(s, size, user):
    for i in range(rows + 1 - size):
        for j in range(columns + 1 - size):
            num4 = 0
            for k in range(size):
                num4 = num4 + s.board[i + k][j + k]
                if(user == 0 or user == COMPUTER) and num4 == COMPUTER * size:
                    return True
                if (user  == 0 or user == HUMAN) and num4 == HUMAN *size:
                    return True
    return False


def printState(s):
    # Prints the board. The empty cells are printed as numbers = the cells name(for input)
    # If the game ended prints who won.
    for r in range(rows) :
        print("\n|", end="")
        # print("\n",len(s[0][0])*" --","\n|",sep="", end="")
        for c in range(columns) :
            if s.board[r][c] == COMPUTER :
                print("X|", end="")
            elif s.board[r][c] == HUMAN :
                print("O|", end="")
            else :
                print(" |", end="")

    print()

    for i in range(columns) :
        print(" ", i, sep="", end="")

    print()

    val = value(s)

    if val == VICTORY :
        print("I won!")
    elif val == LOSS :
        print("You beat me!")
    elif val == TIE :
        print("It's a TIE")


def isFinished(s) :
    # Seturns True iff the game ended
    return value(s) in [LOSS, VICTORY, TIE] or s.size == 0


def isHumTurn(s) :
    # Returns True iff it is the human's turn to play
    return s.playTurn == HUMAN


def decideWhoIsFirst(s) :
    # The user decides who plays first
    if int(input("Who plays first? 1-me / anything else-you : ")) == 1 :
        s.playTurn = COMPUTER
    else :
        s.playTurn = HUMAN

    return s.playTurn


def makeMove(s, c) :
    # Puts mark (for huma. or comp.) in col. c
    # and switches turns.
    # Assumes the move is legal.

    r = 0
    while r < rows and s.board[r][c] == 0 :
        r += 1

    s.board[r - 1][c] = s.playTurn  # marks the board
    s.size -= 1  # one less empty cell
    if (s.playTurn == COMPUTER) :
        s.playTurn = HUMAN
    else :
        s.playTurn = COMPUTER


def inputMove(s) :
    # Reads, enforces legality and executes the user's move.

    # self.printState()
    flag = True
    while flag :
        c = int(input("Enter your next move: "))
        if c < 0 or c >= columns or s.board[0][c] != 0 :
            print("Illegal move.")

        else :
            flag = False
            makeMove(s, c)


def getNext(s) :
    # returns a list of the next states of s
    ns = []
    for c in list(range(columns)) :
        #print("c=", c)
        if s.board[0][c] == 0 :
            #print("possible move ", c)
            tmp = cpy(s)
            makeMove(tmp, c)
            #print("tmp board=", tmp.board)
            ns += [tmp]
            #print("ns=", ns)
    #print("returns ns ", ns)
    return ns


def inputComputer(s) :
    return alphaBetaPruning.go(s)