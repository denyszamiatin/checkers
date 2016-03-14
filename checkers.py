import pprint
import copy

BOARD_SIZE = 8
BLACK = 'black'
WHITE = 'white'
BLACK_SHORT = BLACK[0].upper()
WHITE_SHORT = WHITE[0].upper()
EMPTY_CELL = ' '
taken = {'taken_black': 0, 'taken_white': 0}
BLACK_KING = 'bk'
WHITE_KING = 'wk'

observers = []
def use_observers(f):
    def wraper(*args, **kwargs):
        result = f(*args, **kwargs)
        for observer in observers:
            observer()
        return result
    return wraper

def on_observer(observer):
    observers.append(observer)

def off_observer(observer):
    observers.remove(observer)



def set_board():
    return [[EMPTY_CELL] * BOARD_SIZE for j in range(BOARD_SIZE)]


def color_of_square(row, column):
    """
    Return the color of cell
    :param row: coordinate (0...7)
    :param column: coordinate (0...7)
    :return: BLACK or WHITE

    >>> color_of_square(5, 5)
    'white'
    >>> color_of_square(5, 0)
    'black'
    """
    return BLACK if (row + column) % 2 else WHITE


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
    return BLACK if (board[row][column] == BLACK_SHORT or board[row][column] == BLACK_KING) else WHITE


def get_checker_color_short(color):
    return color[0].upper()


def get_direction_of_motion(board, row, column):
    """
    Get direction of motion
    :param row: coordinate (0...7)
    :param column: coordinate (0...7)
    :return:

    >>> get_direction_of_motion([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 5, 2)
    -1
    >>> get_direction_of_motion([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 2, 1)
    1
    """
    return 1 if get_checker_color(board, row, column) == BLACK else -1


def check_falling_into_field(row, column):
    """

    :param row:
    :param column:
    :return: True or False

    >>> check_falling_into_field(3, 7)
    True
    >>> check_falling_into_field(5, 9)
    False
    """
    if 0 <= row < BOARD_SIZE and 0 <= column < BOARD_SIZE:
        return True
    return False


def possibility_to_go(board, start_row, start_column, end_row, end_column):
    """
    Check the possibility of movement on the specified square
    >>> possibility_to_go([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 0, 1, 1, 0)
    False
    >>> possibility_to_go([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 2, 7, 3, 6)
    True
    >>> possibility_to_go([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 0, 5, 7, 4)
    False
    >>> possibility_to_go([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 5, 6, 4, 7)
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
    >>> get_cells_after_take([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 0, 1)
    []
    >>> get_cells_after_take([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 5, 0)
    [[3, 2]]
    >>> get_cells_after_take([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 2, 3)
    [[4, 1], [4, 5]]
    """
    cells_after_take = [[start_row + r_offset, start_column + c_offset]
                        for r_offset in [-2, 2] for c_offset in [-2, 2]]
    cells_after_take = [[row, column] for row, column in cells_after_take
                        if check_falling_into_field(row, column) and board[row][column] == EMPTY_CELL]
    return cells_after_take


def check_take_checker(board, start_row, start_column, end_row, end_column):
    """
    Check the possibility of taking a checker
    :param board:
    :param start_row:
    :param start_column:
    :param end_row:
    :param end_column:
    :return: True

    >>> check_take_checker([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', 'W', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 2, 3, 4, 1)
    True
    >>> check_take_checker([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', 'W', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 5, 4, 3, 6)
    False

    """
    return (
        check_falling_into_field(start_row, start_column) and
        check_falling_into_field(end_row, end_column) and
        board[start_row][start_column] != EMPTY_CELL and
        [end_row, end_column] in get_cells_after_take(board, start_row, start_column) and
        board[int((end_row + start_row) / 2)] [int((end_column + start_column) / 2)] != EMPTY_CELL and
        get_checker_color(board, start_row, start_column) != get_checker_color(board, int((end_row + start_row) / 2), int((end_column + start_column) / 2))
    )



def get_list_of_cells(board, checker_color):
    """
    Return the list of cells with checkers of definite color
    :param board:
    :param checker_color:
    :return: list

    >>> get_list_of_cells([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], WHITE_SHORT)
    [[5, 0], [5, 2], [5, 4], [5, 6], [6, 1], [6, 3], [6, 5], [6, 7], [7, 0], [7, 2], [7, 4], [7, 6]]
    >>> get_list_of_cells([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], BLACK_SHORT)
    [[0, 1], [0, 3], [0, 5], [0, 7], [1, 0], [1, 2], [1, 4], [1, 6], [2, 1], [2, 3], [2, 5], [2, 7]]

    """
    return [[row, column] for row in range(BOARD_SIZE)
            for column in range(BOARD_SIZE)
            if board[row][column] == get_checker_color_short(checker_color) or
            board[row][column][0].upper() == get_checker_color_short(checker_color)]


def get_list_of_takes_checkers(board, checker_color):
    """
    Return the list of possible takes for the checkers of definite color
    :param board:
    :param checker_color:
    :return:

    >>> get_list_of_takes_checkers([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], WHITE_SHORT)
    []
    >>> get_list_of_takes_checkers([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', 'W', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], BLACK_SHORT)
    [[4, 3], [4, 1]]
    """
    list_of_takes = []
    list_of_cells = get_list_of_cells(board, checker_color)
    for [start_row, start_column] in list_of_cells:
        for [end_row, end_column] in get_cells_after_take(board, start_row, start_column):
            if check_take_checker(board, start_row, start_column, end_row, end_column):
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


def make_move_checker(board, start_row, start_column, end_row, end_column):
    """
    Function to make move if possible, otherwise get a message
    :param board:
    :param start_row:
    :param start_column:
    :param end_row:
    :param end_column:
    :return:
    >>> make_move_checker([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', 'W', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 2, 1, 4, 3)
    Move impossible
    >>> make_move_checker([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', 'W', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 5, 4, 4, 5)
    [[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', 'W', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', 'W', ' ', ' '], ['W', ' ', 'W', ' ', ' ', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']]
    """
    if possibility_to_go(board, start_row, start_column, end_row, end_column):
        board[end_row][end_column] = board[start_row][start_column]
        board[start_row][start_column] = EMPTY_CELL
        return board
    else:
        print('Move impossible')

@use_observers
def make_take_checker(board, start_row, start_column, end_row, end_column):
    """
    Function to make take if possible, otherwise get a message
    :param board:
    :param start_row:
    :param start_column:
    :param end_row:
    :param end_column:
    :return:
    >>> make_take_checker([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', 'W', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 2, 3, 4, 1)
    [[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', ' ', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', 'B', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']]
    >>> make_take_checker([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', 'W', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 2, 5, 4, 7)
    Take impossible
    """
    if check_take_checker(board, start_row, start_column, end_row, end_column):
        board[end_row][end_column] = board[start_row][start_column]
        board[start_row][start_column] = EMPTY_CELL
        board[int((end_row + start_row) / 2)][int((end_column + start_column) / 2)] = EMPTY_CELL
        return board
    else:
        print('Take impossible')


def count_the_number_of_checkers_taken(board, row, column):
    '''
    Increases the number of checkers taken
    :param board:
    :param row:
    :param column:
    >>> count_the_number_of_checkers_taken([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 0, 0)
    Traceback (most recent call last):
    ...
    ValueError
    >>> count_the_number_of_checkers_taken([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 2, 7)

    >>> count_the_number_of_checkers_taken([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 6, 3)

    '''
    if get_checker_color(board, row, column) == BLACK:
        taken['taken_black'] += 1
    else:
        taken['taken_white'] += 1


def check_again_take_checker(board, start_row, start_column, end_row, end_column):
    '''
    :param board:
    :param start_row:
    :param start_column:
    :param end_row:
    :param end_column:
    >>> check_again_take_checker([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', ' ', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', 'B', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 5, 0, 3, 2)
    False
    >>> check_again_take_checker([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', 'B', ' ', 'B', ' ', 'B', ' '], [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', 'B', ' ', ' ', ' ', ' ', ' ', ' '], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']], 5, 0, 3, 2)
    True
    '''
    if check_take_checker(board, start_row, start_column, end_row, end_column):
        board_after_take = copy.deepcopy(board)
        make_take_checker(board_after_take, start_row, start_column, end_row, end_column)
        start_row, start_column = end_row, end_column
        for end_row, end_column in get_cells_after_take(board_after_take, start_row, start_column):
            if check_take_checker(board_after_take, start_row, start_column, end_row, end_column):
                return True
    return False


def turn_into_king(board, row, column):
    """
    Function that turns checker into a king
    :param board:
    :param row:
    :param column:
    :return:
    """
    if check_falling_into_field(row, column):
        if board[row][column] == BLACK_SHORT and row == BOARD_SIZE - 1:
            board[row][column] = BLACK_KING
        elif board[row][column] == WHITE_SHORT and row == 0:
            board[row][column] = WHITE_KING


def check_on_diagonal(start_row, start_column, end_row, end_column):
    return True if abs(end_row - start_row) == abs(end_column - start_column) else False


def check_move_kings(board, start_row, start_column, end_row, end_column):
    """
    Function that checks king's move
    :param board:
    :param start_row:
    :param start_column:
    :param end_row:
    :param end_column:
    :return: True or False
    """
    return (
        check_falling_into_field(end_row, end_column) and
        board[start_row][start_column] == BLACK_KING or board[start_row][start_column] == WHITE_KING and
        board[end_row][end_column] == EMPTY_CELL and
        check_on_diagonal(start_row, start_column, end_row, end_column))


def make_move_kings(board, start_row, start_column, end_row, end_column):
    """
    Function that makes king's move if possible
    :param board:
    :param start_row:
    :param start_column:
    :param end_row:
    :param end_column:
    :return:
    """
    if check_move_kings(board, start_row, start_column, end_row, end_column):
        board[end_row][end_column] = WHITE_KING if board[start_row][start_column] == WHITE_KING else BLACK_KING
        board[start_row][start_column] = EMPTY_CELL


def make_move(board, start_row, start_column, end_row, end_column):
    '''
    Make_move checker or kings
    '''
    if len(board[start_row][start_column]) == 1:
        make_move_checker(board, start_row, start_column, end_row, end_column)
    else:
        make_move_kings(board, start_row, start_column, end_row, end_column)


def get_cells_way_kings(board, start_row, start_column, end_row, end_column):
    '''
    Get list cells on way Kings
    '''
    way = []
    for number_row, row in enumerate(board):
        for number_column, cell in enumerate(row):
            if check_on_diagonal(start_row, start_column, number_row, number_column) and \
            check_on_diagonal(number_row, number_column, end_row, end_column) and \
            (start_row < number_row <= end_row or end_row <= number_row < start_row):
                way.append(cell)
    return way


def check_one_checker_on_way(board, start_row, start_column, end_row, end_column):
    '''
    check the presence of one checker
    '''
    way = get_cells_way_kings(board, start_row, start_column, end_row, end_column)
    return True if way.count(EMPTY_CELL) == len(way) - 1 else False


@use_observers
def check_take_kings(board, start_row, start_column, end_row, end_column):
    """
    Check the possibility of taking a checker by Kings
    :param board:
    :param start_row:
    :param start_column:
    :param end_row:
    :param end_column:
    >>> check_take_kings([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', 'B', ' '], [' ', 'B', ' ', ' ', ' ', 'B', ' ', 'B'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', ' ', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'bk', ' ']], 7, 6, 1, 0)
    True
    >>> check_take_kings([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', 'B', ' '], [' ', 'B', ' ', ' ', ' ', 'B', ' ', 'B'], ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'bk', ' ']], 7, 6, 1, 0)
    False
    >>> check_take_kings([[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', 'B', ' ', 'B', ' ', 'B'], [' ', ' ', ' ', ' ', ' ', ' ', 'B', ' '], [' ', 'B', ' ', ' ', ' ', 'B', ' ', 'B'], ['W', ' ', 'W', ' ', 'B', ' ', 'W', ' '], [' ', 'W', ' ', 'W', ' ', ' ', ' ', 'W'], ['W', ' ', 'W', ' ', 'W', ' ', 'bk', ' ']], 7, 6, 1, 0)
    False
    """
    return (
        check_falling_into_field(start_row, start_column) and
        check_falling_into_field(end_row, end_column) and
        (board[start_row][start_column] == BLACK_KING or board[start_row][start_column] == WHITE_KING) and
        board[end_row][end_column] == EMPTY_CELL and
        check_on_diagonal(start_row, start_column, end_row, end_column) and
        not check_checker_color_in_way(board, start_row, start_column, end_row, end_column) and
        board[start_row][start_column] not in get_cells_way_kings(board, start_row, start_column, end_row, end_column) and
        check_one_checker_on_way(board, start_row, start_column, end_row, end_column)
    )


def check_checker_color_in_way(board, start_row, start_column, number_row, number_column):
    return True if get_checker_color_short(get_checker_color(board, start_row, start_column)) \
                   in get_cells_way_kings(board, start_row, start_column, number_row, number_column) else False

def get_cells_after_take_kings(board, start_row, start_column):
    """
    Get the cells after take kings
    """
    cells_after_take_kings = []
    for number_row, row in enumerate(board):
        for number_column, cell in enumerate(row):
            if (board[start_row][start_column] == BLACK_KING or board[start_row][start_column] == WHITE_KING) and \
            check_on_diagonal(start_row, start_column, number_row, number_column) and \
            (board[start_row][start_column] not in get_cells_way_kings(board, start_row, start_column, number_row, number_column)) and \
            not check_checker_color_in_way(board, start_row, start_column, number_row, number_column) and \
            check_one_checker_on_way(board, start_row, start_column, number_row, number_column) and \
            board[number_row][number_column] == EMPTY_CELL:
                cells_after_take_kings.append([number_row, number_column])
    return cells_after_take_kings


def get_list_of_takes_kings(board, checker_color):
    """
    Return the list of possible takes for the kings of definite color
    """
    list_of_takes_kings = []
    list_of_cells = get_list_of_cells(board, checker_color)
    for [start_row, start_column] in list_of_cells:
        for [end_row, end_column] in get_cells_after_take_kings(board, start_row, start_column):
            if check_take_kings(board, start_row, start_column, end_row, end_column):
                list_of_takes_kings.append([end_row, end_column])
    return list_of_takes_kings


def check_take(board, checker_color):
    '''
    Return the possible takes for the checkers or kings of definite color
    '''
    return True if len(get_list_of_takes_checkers(board, checker_color)) > 0 or \
                   len(get_list_of_takes_kings(board, checker_color)) > 0 \
        else False


'''
if __name__ == "__main__":
    #import doctest
    #doctest.testmod()

    board = set_board()
    set_checkers(board)
    board = [[' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'],
             ['B', ' ', 'B', ' ', 'B', ' ', 'B', ' '],
             [' ', 'B', ' ', 'B', ' ', 'B', ' ', 'B'],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             ['W', ' ', 'wk', ' ', 'W', ' ', 'W', ' '],
             [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'],
             ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' ']]

    pprint.pprint(board)


    make_move_checker(board, 2, 1, 3, 2)
    make_move_checker(board, 3, 2, 4, 1)
    make_move_checker(board, 1, 0, 2, 1)
    make_move_checker(board, 2, 5, 3, 6)
    make_move_checker(board, 3, 6, 4, 7)
    make_move_checker(board, 1, 4, 2, 5)

    make_move_checker(board, 2, 3, 3, 4)
    make_move_checker(board, 3, 4, 4, 5)
    make_move_checker(board, 1, 2, 2, 3)
    make_move_checker(board, 2, 7, 3, 6)
    make_move_checker(board, 1, 6, 2, 7)
    pprint.pprint(board)

    #print('check_again_take_checker', check_again_take_2(board, 5, 0, 3, 2))
    print('check_again_take_checker', check_again_take_2(board, 5, 6, 3, 4))
    #pprint.pprint(board)


    make_take_checker(board, 5, 0, 3, 2)
    pprint.pprint(board)
    make_take_checker(board, 3, 2, 1, 0)
    pprint.pprint(board)
    print(taken)


    print_board(board)
    print(is_fight(board, WHITE_SHORT))
    row, column = get_input()
    print(board[row][column])
    print(get_list_of_takes(board, WHITE))
    print(get_list_of_squares(board, WHITE))
    print(get_cells_after_take2(board, row, column))
'''
