def generatePattern(id):
    board = [False, False, False, False, False, False, False, False, False]
    for i in range(len(id)):
        board[int(id[i])] = True
    return board

def deadTest(board):
        """
          Check whether a board is a dead board
        """
        if board[0] and board[4] and board[8]:
            return True
        if board[2] and board[4] and board[6]:
            return True
        for i in range(3):
            #check every row
            row = i * 3
            if board[row] and board[row+1] and board[row+2]:
                return True
            #check every column
            if board[i] and board[i+3] and board[i+6]:
                return True
        return False

def eq(board1, board2):
        equal = (board1[0] == board2[0] and board1[1] == board2[1] and
                board1[2] == board2[2] and board1[3] == board2[3] and
                board1[4] == board2[4] and board1[5] == board2[5] and
                board1[6] == board2[6] and board1[7] == board2[7] and
                board1[8] == board2[8])
        return equal

def transform(board, xy):
    tmp = list(board)
    if xy == 'x':
        for i in range(3):
            tmp[i*3] = board[i*3 + 2]
            tmp[i*3 + 2] = board[i*3]
            
    elif xy == 'y':
        for i in range(3):
            tmp[i] = board[i + 6]
            tmp[i + 6] = board[i]
    elif xy == 'r':
        tmp[0] = board[6]
        tmp[1] = board[3]
        tmp[2] = board[0]
        tmp[3] = board[7]
        tmp[4] = board[4]
        tmp[5] = board[1]
        tmp[6] = board[8]
        tmp[7] = board[5]
        tmp[8] = board[2]
    return tmp        

def deepEq(board1, board2):
    for i in range(4):
        if eq(board1, board2) or eq(transform(board1, 'x'), board2):
            return True
        board1 = transform(board1, 'r')
    return False

def getPattern(board):
        """
          Get the Pattern
        """
        pattern = [ 
            ('a', ["013578", "01568", "01567", "01456", "1357", "0268", "0178", "0138", "0135", "0134", "045", "027", "023", "016", "17", "13", "08"]),
            ('b', ["02", "04", "05", "14", "013", "315", "0145", "0146", "0156", "0167", "0168", "0247", "0457", "01357", "01358"]),
            ('c', [""]),
            ('c2', ["4"]),
            ('d', ["017", "018", "015"]),
            ('ad', ["01"]),
            ('ab', ["014", "026", "134", "0157", "0158"]),
            ('1', ["0", "1", "057"]) 
            ]

        if deadTest(board):
            return '1'
        for p in pattern:
            for i in p[1]:
                if deepEq( generatePattern(i), board ):
                    return p[0]

        return "Error"

print(getPattern(generatePattern("015")))

arr = [ ["013578", "01568", "01567", "01456", "1357", "0268", "0178", "0138", "0135", "0134", "045", "027", "023", "016", "17", "13", "08"],
["02", "04", "05", "14", "013", "315", "0145", "0146", "0156", "0167", "0168", "0247", "0457", "01357", "01358"],
[""],
["4"],
["017", "018","015"],
["01"],
["014", "026", "134", "0157", "0158"] ]
sum = 0
for i in arr:
    sum+=len(i)
    print(len(i))
print(sum)
# print( deepEq(generatePattern("01"), generatePattern("12")) )