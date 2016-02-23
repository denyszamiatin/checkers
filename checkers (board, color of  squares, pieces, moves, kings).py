BLACK_SQUARE = '*'
WHITE_SQUARE = ' '
BLACK_CHECKER = '0'
WHITE_CHECKER = '1'
BLACK_KING = 'bk'
WHITE_KING = 'wk'


def print_board(board):
    n = 8
    for row in board:
        print((str(n)), ' ', (' '.join(row)))
        n -= 1
    print('')
    print('    ' + ' '.join(('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')))
    print('')


def set_board():
    return [[WHITE_SQUARE if (x + y) % 2 else BLACK_SQUARE
             for x in range(8)]
            for y in range(8)]

def checkers_on(board):
    for row in range(8):
        for column in range(8):
            if board[row][column] == BLACK_SQUARE:
                if 0 <= row < 3:
                    board[row][column] = BLACK_CHECKER
                elif 5 <= row < 8:
                    board[row][column] = WHITE_CHECKER


board = checkers_on(color_board(set_board()))
print_board(board)

def check_border(row, column):
    if row in range(0, 8) and column in range(0, 8):
        return True

def check_square(row, column):
    if check_border(row, column):
        if board[row][column] == BLACK_SQUARE:
            return True

def check_black(row, column):
    if check_border(row, column):
        if board[row][column] == BLACK_CHECKER:
            return True

def check_white(row, column):
    if check_border(row, column):
        if board[row][column] == WHITE_CHECKER:
            return True

def convert_to_row(coordinates):
    return 8 - int(coordinates[0])

def convert_to_column(coordinates):
    return ord(coordinates[1].lower()) - 97

def check_coordinates(coordinates):
    try:
        if len(coordinates) != 2:
            raise ValueError
        row = convert_to_row(coordinates)
        column = convert_to_column(coordinates)
        if check_border(row, column) == None:
            raise ValueError
    except ValueError:
        print ('Incorrect coordinates')
        exit()

def simple_move(row, column):
    moves = ''
    if board[row][column] == BLACK_CHECKER:
        row += 1
        if check_square(row, column - 1):
            moves = str(8 - row) + str(chr(column - 1 + 65))
        if check_square(row, column + 1):
            moves = moves + ' ' +  str(8 - row) + str(chr(column + 1 + 65))
    elif board[row][column] == WHITE_CHECKER:
        row -= 1
        if check_square(row, column - 1):
            moves = str(8 - row) + str(chr(column - 1 + 65))
        if check_square(row, column + 1):
            moves = moves + ' ' +  str(8 - row) + str(chr(column + 1 + 65))
    return moves

def take_move(row, column):
    moves = ''
    if board[row][column] == BLACK_CHECKER:
        if check_white(row + 1, column - 1) and check_square(row + 2, column - 2):
            moves = str(8 - (row + 2)) + str(chr(column - 2 + 65))
        if check_white(row + 1, column + 1) and check_square(row + 2, column + 2):
            moves = moves + ' ' + str(8 - (row + 2)) + str(chr(column + 2 + 65))
        if check_white(row - 1, column - 1) and check_square(row - 2, column - 2):
            moves = moves + ' ' + str(8 - (row - 2)) + str(chr(column - 2 + 65))
        if check_white(row - 1, column + 1) and check_square(row - 2, column + 2):
            moves = moves + ' ' + str(8 - (row + 2)) + str(chr(column + 2 + 65))
    elif board[row][column] == WHITE_CHECKER:
        if check_black(row + 1, column - 1) and check_square(row + 2, column - 2):
            moves = str(8 - (row + 2)) + str(chr(column - 2 + 65))
        if check_black(row + 1, column + 1) and check_square(row + 2, column + 2):
            moves = moves + ' ' + str(8 - (row + 2)) + str(chr(column + 2 + 65))
        if check_black(row - 1, column - 1) and check_square(row - 2, column - 2):
            moves = moves + ' ' + str(8 - (row - 2)) + str(chr(column - 2 + 65))
        if check_black(row - 1, column + 1) and check_square(row - 2, column + 2):
            moves = moves + ' ' + str(8 - (row + 2)) + str(chr(column + 2 + 65))
    else:
        moves = 'Incorrect initial coordinates. No checker'
    return moves

def check_move(coordinates):
    row = convert_to_row(coordinates)
    column = convert_to_column(coordinates)
    moves = take_move(row, column)
    if moves == '':
        moves = simple_move(row, column)
    return moves

def move_direction(coordinates):
    check_coordinates(coordinates)
    moves = check_move(coordinates)
    if moves == '':
        moves = 'None'
    return moves

coordinates = input('Enter checker coordinates, (1-8)(A-H)? ')
print ('Possible move:', move_direction(coordinates))

def check_black_king(row, column):
    if check_border(row, column):
        if board [row][column] == BLACK_CHECKER and row == 7:
            board [row][column] = BLACK_KING

def check_white_king(row, column):
    if check_border(row, column):
        if board [row][column] == WHITE_CHECKER and row == 0:
            board [row][column] = WHITE_KING

def check_king_move(coordinates1, coordinates2):
    check_coordinates(coordinates1)
    check_coordinates(coordinates2)
    row1 = convert_to_row(coordinates1)
    column1 = convert_to_column(coordinates1)
    row2 = convert_to_row(coordinates2)
    column2 = convert_to_column(coordinates2)
    if check_square(row2, column2) and abs(row2 - row1) == abs(column2 - column1):
        return True





