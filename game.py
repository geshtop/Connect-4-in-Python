import copy
import alphaBetaPruning
import bcolors

bcolors = bcolors.bcolors()


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


def cpy(s1):
    # construct a parent DataFrame instance
    s2 = game()
    s2.playTurn = s1.playTurn
    s2.size = s1.size
    s2.board = copy.deepcopy(s1.board)
    print("board ", s2.board)
    return s2


def value(s):
    # Returns the heuristic value of s
    grade = Grade(s) #שליחה לפונקציה המחזירה ציון עבור הלוח
    if grade == VICTORY: #למקרה והציון הוא ציון ניצחון
        return VICTORY #מחזיר ניצחון
    elif grade == LOSS: #למקרה והציון הוא ציון הפסד
        return LOSS #תחזיר הפסד
    elif s.size == 0: #אם נגמר המקום בלוח ואין לא ניצחון ולא הפסד
        return TIE #תחזיר תיקו
    else:
        return grade + 0.00001# מוסיף ערך קטן כי אם עשינו על זה פעולות וזה יצא אפס שלא יחזיר בטעות תיקו

def Grade(s): #פונקציה הסוכמת ציון עבור כל אפשרוות של שורה, עמודה ואלכסון ומחזירה ציון כללי עבור הלוח
    grade1 = find_horizontal(s) #ציון שורה
    grade2 = find_vertical(s) #ציון עמודה
    grade3 = find_pos_diagonal(s) #ציון אלכסון חיובי
    grade4 = find_neg_diagonal(s) #ציון אלכסון שלילי
    win_loss = [VICTORY, LOSS]
    if (grade1 in win_loss):
        return grade1
    elif (grade2 in win_loss):
        return grade2
    elif (grade3 in win_loss):
        return grade3
    elif (grade4 in win_loss):
        return grade4
    else: return grade1 + grade2 + grade3 + grade4


def find_horizontal(s): #פונקציה העוברת על השורות וכל סט של ארבע משבצות היא שולחת לבדיקה
    grade = 0
    ihor = []
    for i in range(rows):
        for j in range(columns + 1 - SIZE):
            ihor.clear()
            for k in range(SIZE):
                ihor.append(s.board[i][j + k]) #כל סט של ארבע משבצות מכניס לרשימה
            _help = checkSeq(ihor) #שליחת הרשימה לבדיקה וקבלת מצב על הסט
            if _help in [VICTORY, LOSS] :  # אם זה נצחון או הפסד תחזיר את הציון
                return _help
            grade += _help  # סוכם עם הציון הקודם
    return grade


def find_vertical(s): #פונקציה העוברת על העמודות וכל סט של ארבע משבצות היא שולחת לבדיקה
    grade = 0
    iver = []
    for i in range(rows + 1 - SIZE):
        for j in range(columns):
            iver.clear()
            for k in range(SIZE):
                iver.append(s.board[i + k][j]) #כל סט של ארבע משבצות מכניס לרשימה
            _help = checkSeq(iver) #שליחת הרשימה לבדיקה וקבלת מצב על הסט
            if _help in [VICTORY, LOSS] :  # אם זה נצחון או הפסד תחזיר את הציון
                return _help
            grade += _help  # סוכם עם הציון הקודם
    return grade


def find_neg_diagonal(s): #פונקציה העוברת על האלכסונים השליליים וכל סט של ארבע משבצות היא שולחת לבדיקה
    grade = 0
    idiagneg = []
    for i in range(rows + 1 - SIZE):
        for j in range(columns + 1 - SIZE):
            idiagneg.clear()
            for k in range(SIZE):
                idiagneg.append(s.board[i + k][j + k]) #כל סט של ארבע משבצות מכניס לרשימה
            _help = checkSeq(idiagneg) #שליחת הרשימה לבדיקה וקבלת מצב על הסט
            if _help in [VICTORY, LOSS] :  # אם זה נצחון או הפסד תחזיר את הציון
                return _help
            grade += _help  # סוכם עם הציון הקודם
    return grade

def find_pos_diagonal(s): #פונקציה העוברת על האלכסוניים החיוביים וכל סט של ארבע משבצות היא שולחת לבדיקה
    grade = 0
    idiagpos = []
    for i in range(rows + 1 - SIZE):
        for j in range(SIZE - 1, columns):
            idiagpos.clear()
            for k in range(SIZE):
                idiagpos.append(s.board[i + k][j - k]) #כל סט של ארבע משבצות מכניס לרשימה
            _help = checkSeq(idiagpos) #שליחת הרשימה לבדיקה וקבלת מצב על הסט
            if _help in [VICTORY, LOSS] :  # אם זה נצחון או הפסד תחזיר את הציון
                return _help
            grade += _help  # סוכם עם הציון הקודם
    return grade


def checkSeq(seq): #בודקת ברצף של 4 את היחס בין השחקני מחשב והשחקני משתמש הנמצאים שם
    sumPlayers = sum(seq) #סכום הכולל גם של המחשב וגם של המשתמש
    if sumPlayers == SIZE * HUMAN: #אם קיבלנו 4 זה אומר שיש לנו 4 שחקני משתמש
        return LOSS #המחשב הפסיד
    if sumPlayers == SIZE * COMPUTER: # אם קיבלנו 20 זה אומר שיש לנו 4 שחקני מחשב
        return VICTORY # המחשב ניצח
    if sumPlayers == 2 * SIZE: #אם קיבלנו 8 זה אומר שיש לנו מחשב אחד ושלושה משתמשים
        return 1000 #לכן ניתן ציון גבוה ממש כדי שהמחשב ישאר שם
    if sumPlayers == 2 * SIZE - 1:#אם קיבלנו 7 זה אומר מחשב אחד ו-2 משתמש
        comp_index = seq.index(COMPUTER) #זה תלוי איפה המחשה נמצא. אינדקס של המחשב
        if (comp_index in [1, 2] and seq[comp_index + 1] == HUMAN and seq[comp_index - 1] == HUMAN): #במחשב בין 2 משתמשים
            return 500
        if (comp_index < 3 and seq[comp_index + 1] == HUMAN) or (comp_index > 0 and seq[comp_index - 1] == HUMAN): #מצד כלשהו יש למחשב משתמש, אך לא מ2 הצדדים
            return 100
    if COMPUTER not in seq:#יש לי רק שחקנים של המשתמש
        return -sumPlayers
    if HUMAN not in seq: #יש לי רק שחקנים של המחשב
        return sumPlayers % SIZE #בודק כמה מחשבים
    return 0

def printState(s):

    # Prints the board. The empty cells are printed as numbers = the cells name(for input)
    # If the game ended prints who won.
    for r in range(rows) :
        print("\n|", end="")
        # print("\n",len(s[0][0])*" --","\n|",sep="", end="")
        for c in range(columns) :
            if s.board[r][c] == COMPUTER :
                #print("X|", end="")
                print(bcolors.RED + bcolors.BOLD +"X" + bcolors.ENDC +"|"  , end="")

            elif s.board[r][c] == HUMAN :
                #print("O|", end="")
                print(bcolors.BLUE + bcolors.BOLD +"O" + bcolors.ENDC +"|"  , end="")

            else :
                print(" |", end="")

    print()

    for i in range(columns) :
        print(bcolors.CYAN + " " , i, sep="", end="")


    print(bcolors.ENDC)

    val = value(s)

    if val == VICTORY :
        print( bcolors.RED + "I won!" + bcolors.ENDC)
    elif val == LOSS :
        print( bcolors.BLUE + "You beat me!" + bcolors.ENDC)
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
        print("c=", c)
        if s.board[0][c] == 0 :
            print("possible move ", c)
            tmp = cpy(s)
            makeMove(tmp, c)
            print("tmp board=", tmp.board)
            ns += [tmp]
            print("ns=", ns)
    print("returns ns ", ns)
    return ns


def inputComputer(s) :
    return alphaBetaPruning.go(s)