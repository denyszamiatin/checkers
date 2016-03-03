import pprint

BOARD_SIZE = 8
BLACK = 'black'
WHITE = 'white'
BLACK_SHORT = BLACK[0].upper()
WHITE_SHORT = WHITE[0].upper()
EMPTY_CELL = ' '


def set_board():
    return [[EMPTY_CELL] * BOARD_SIZE for j in range(BOARD_SIZE)]


def color_of_square(row, column):
    """
    Return the color of cell
    :param row: coordinate (0...7)
    :param column: coordinate (0...7)
    :return: BLACK or WHITE
    """
    return WHITE if (row + column) % 2 else BLACK


def put_checks_on_row(row, start, CHECKS_COLOR):
    for column in range(start, BOARD_SIZE, 2):
        row[column] = CHECKS_COLOR


def set_checkers(board):
    """
    :param board: list[len(8)][len(8)]
    Set checks on board.
    >>> set_checkers([[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']])
    [[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']]
    """
    for row_number, row in enumerate(board):
        if 2 < row_number < 5:
            continue
        else:
            put_checks_on_row(row, (row_number + 1) % 2, BLACK_SHORT if row_number < 3 else WHITE_SHORT)
    return board


def get_checker_color(board, row, column):
    """
    Check checker color
    :param column: coordinate (0...7)
    :param row: coordinate (0...7)
    :param board: checkers board
    :return: BLACK or WHITE
    >>> get_checker_color([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 0, 0)
    Traceback (most recent call last):
    ...
    ValueError
    >>> get_checker_color([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 2, 7)
    'black'
    >>> get_checker_color([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 6, 3)
    'white'
    """
    if board[row][column] == EMPTY_CELL:
        raise ValueError
    return BLACK if board[row][column] == BLACK_SHORT else WHITE


def get_direction_of_motion(board, row, column):
    """
    Get direction of motion
    :param row: coordinate (0...7)
    :param column: coordinate (0...7)
    :return:
    """
    return 1 if get_checker_color(board, row, column) == BLACK else -1


def check_falling_into_field(row, column):
    if 0 <= row < BOARD_SIZE and 0 <= column < BOARD_SIZE:
        return True
    return False


def possibility_to_go(board, start_row, start_column, end_row, end_column):
    """
    Check the possibility of movement on the specified square
    >>>possibility_to_go([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 0, 1, 1, 0)
    False
    >>>possibility_to_go([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 2, 7, 3, 6)
    True
    >>>possibility_to_go([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 0, 5, 7, 4)
    False
    >>>possibility_to_go([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 5, 6, 4, 7)
    True
    """
    return all((check_falling_into_field(start_row, start_column),
               check_falling_into_field(end_row, end_column),
               board[start_row][start_column] != EMPTY_CELL,
               board[end_row][end_column] == EMPTY_CELL,
               end_row == start_row + get_direction_of_motion(board, start_row, start_column),
               end_column in (start_column + 1, start_column - 1)
               ))


def print_board(board):
    BOARD_SIZE = 8
    print('   A   B   C   D   E   F   G   H')
    print(' ', "+---" * 8, "+", sep='')
    for row in board:
        print(BOARD_SIZE, end='')
        for i in row:
            print('| %s ' % i, end='')
        print('|%d' % BOARD_SIZE)
        BOARD_SIZE -= 1
        print(' ', "+---" * 8, "+", sep='')
    print('   A   B   C   D   E   F   G   H')


def get_input():
    coordinates = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
    while True:
        try:
            column = input('Столбец = ').upper()
            row = int(input('Строка = '))
            if column not in coordinates.keys():
                raise ValueError
            if row > 8:
                raise ValueError
            if row < 0:
                raise ValueError
        except ValueError:
            print('Неправильный ввод')
        except KeyError:
            print('Ужос')
        else:
            row = 8 - row
            column = coordinates[column]
            return row, column


def get_cells_after_take(board, start_row, start_column):
    """
    Get the cells after take
    """
    cells_after_take = [[start_row + r_offset, start_column + c_offset]
                        for r_offset in [-2, 2] for c_offset in [-2, 2]]
    cells_after_take = [[row, column] for row, column in cells_after_take
                        if check_falling_into_field(row, column) and board[row][column] == EMPTY_CELL
                        ]
    return cells_after_take


def get_cells_after_take2(board, row, column):
    CELLS = ((-1, -1), (-1, 1), (1, 1), (1, -1))
    cells_after_take = [[row + way[0] * 2, column + way[1] * 2] for way in CELLS if
                        board[row + way[0]][column + way[1]] ==
                        enemy_color(board, row, column) and check_falling_into_field(row + way[0] * 2,
                                                                                      column + way[1] * 2)
                        and board[row + way[0] * 2][column + way[1] * 2] == EMPTY_CELL
                        ]
    return cells_after_take


def check_take(board, start_row, start_column, end_row, end_column):
    """
    Check the possibility of taking a checker
    :param board:
    :param start_row:
    :param start_column:
    :param end_row:
    :param end_column:
    :return: True
    """
    return all((
        check_falling_into_field(start_row, start_column),
        check_falling_into_field(end_row, end_column),
        board[start_row][start_column] != EMPTY_CELL,
        [end_row, end_column] in get_cells_after_take(board, start_row, start_column),
        board[int((end_row + start_row) / 2)] [int((end_column + start_column) / 2)] != EMPTY_CELL,
        get_checker_color(start_row, start_column) !=
        get_checker_color(int((end_row + start_row) / 2), int((end_column + start_column) / 2))))


def get_list_of_cells(board, checker_color):
    """
    Return the list of cells with checkers of definite color
    :param board:
    :param checker_color:
    :return: list
    """
    return [[row, column] for row in range(BOARD_SIZE)
            for column in range(BOARD_SIZE)
            if board[row][column] == checker_color]


def get_list_of_takes(board, checker_color):
    """
    Return the list of possible takes for the checkers of definite color
    :param board:
    :param checker_color:
    :return:
    """
    list_of_takes = []
    list_of_cells = get_list_of_cells(board, checker_color)
    for [start_row, start_column] in list_of_cells:
        for [end_row, end_column] in get_cells_after_take(board, start_row, start_column):
                   if check_take(start_row, start_column, end_row, end_column):
                       list_of_takes.append([end_row, end_column])
    return list_of_takes


def enemy_color(board, row, column):
    return WHITE_SHORT if board[row][column] == BLACK_SHORT else BLACK_SHORT


def is_fight(board, color):  # Есть ли бой
    enemy = set()
    CELLS = ((-1, -1), (-1, 1), (1, 1), (1, -1))
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            for i in CELLS:
                if board[row][column] == color and \
                        check_falling_into_field(row - i[0] * 2, column - i[1] * 2) and \
                        board[row - i[0]][column - i[1]] == enemy_color(board, row, column) and \
                        board[row - i[0] * 2][column - i[1] * 2] == EMPTY_CELL:
                    enemy.add((row, column))
    return enemy


'''
if __name__ == "__main__":
    import doctest
    doctest.testmod()
'''
'''
    board = [[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'],
             ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', 'B', ' ', 'B', ' ', 'B', ' '],
             [' ', 'W', ' ', 'W', ' ', 'W', ' ', ' '],
             [' ', ' ', ' ', ' ', 'B', ' ', ' ', ' '],
             [' ', 'B', ' ', 'W', ' ', ' ', ' ', 'W'],
             ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']]
    # board = set_board()
    # set_checkers(board)
    print_board(board)
    print(is_fight(board, WHITE_SHORT))
    row, column = get_input()
    print(board[row][column])
    print(get_list_of_takes(board, WHITE))
    print(get_list_of_squares(board, WHITE))
    print(get_cells_after_take2(board, row, column))
'''
