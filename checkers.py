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
    Set checks on board.
    """
    for row_number, row in enumerate(board):
        if 2 < row_number < 5:
            continue
        put_checks_on_row(
            row,
            (row_number + 1) % 2,
            BLACK_SHORT if row_number < 3 else WHITE_SHORT
        )


def get_checker_color(board, row, column):
    """
    Check checker color
    :param column: coordinate (0...7)
    :param row: coordinate (0...7)
    :param board: checkers board
    :return: BLACK or WHITE
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


def check_falling_into_field(board, row, column):
    try:
        board[row][column]
    except IndexError:
        return False
    return True


def possibility_to_go(board, start_row, start_column, end_row, end_column):
    """
    Check the possibility of movement on the specified square
    """
    return all((
        check_falling_into_field(board, start_row, start_column),
        check_falling_into_field(board, end_row, end_column),
        board[start_row][start_column] != EMPTY_CELL,
        board[end_row][end_column] == EMPTY_CELL,
        end_row == start_row + get_direction_of_motion(
            board, start_column, start_row),
        end_column in (start_column + 1, start_column - 1)
    ))


def print_board(checks):
    ind = 8
    print(" " + "+---" * 8 + "+")
    for i in checks:
        print(ind, end='')
        for j in i:
            print('| %s ' % j, end='')
        ind -= 1
        print("|\n" + " " + "+---" * 8 + "+")
    print('   A   B   C   D   E   F   G   H')


def get_input():  # Выбор шашки возвращает координаты
    coordinates = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
    while True:
        try:
            col = input('Столбец = ').upper()
            row = int(input('Строка = ')) - 1
            if col not in coordinates.keys():
                raise ValueError
            if row > 7:
                raise ValueError
            if row < 0:
                raise ValueError
        except ValueError:
            print('Неправильный ввод')
        except KeyError:
            print('Ужос')
        else:
            col = coordinates[col]
            return row, col


def get_cells_after_take(board, start_row, start_column):
    """
    Get the cells after take
    """
    cells_after_take = []
    end_rows = [start_row + 2, start_row + 2, start_row - 2, start_row - 2]
    end_columns = [start_column - 2, start_column + 2, start_column - 2, start_column + 2]
    for end_row, end_column in zip(end_rows, end_columns):
        if all((
            check_falling_into_field(board, start_row, start_column),
            check_falling_into_field(board, end_row, end_column),
            board[start_row][start_column] != EMPTY_CELL,
            board[end_row][end_column] == EMPTY_CELL,
            )):
            cells_after_take.append([end_row,end_column])
    return cells_after_take


if __name__ == "__main__":
    board = set_board()
    set_checkers(board)
    pprint.pprint(board)
