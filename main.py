import random


# Small class to store X a Y coordinate as one object
class Coordinates:
    mv_x: int
    mv_y: int

    def __init__(self, iv_x: int, iv_y: int):
        assert isinstance(iv_x, int)
        self.mv_x = iv_x
        assert isinstance(iv_y, int)
        self.mv_y = iv_y


class CoordinateProvider:
    ml_coordinates = []

    def __init__(self, iv_x: int, iv_y: int):
        for lv_x in range(iv_x):
            for lv_y in range(iv_y):
                coord = Coordinates(lv_x, lv_y)
                self.ml_coordinates.append(coord)

    def get_random_coords(self):
        random_posit = random.randrange(self.ml_coordinates.__len__())
        if gv_debug == 'X':
            print('Random position', random_posit)
            print('List size', self.ml_coordinates.__len__())
        rs_coords = self.ml_coordinates.__getitem__(random_posit)
        self.ml_coordinates.__delitem__(random_posit)
        return rs_coords


# Initialize matrix to iv_rows and iv_columns - set all values to iv_value
def init_matrix(iv_rows, iv_columns, iv_value):
    rm_matrix = []
    for i in range(iv_rows):
        rm_matrix.append([iv_value] * iv_columns)

    return rm_matrix


# Print whole matrix with separator space
def print_matrix(im_matrix):
    for lv_row in im_matrix:
        for lv_cell in lv_row:
            print(lv_cell, end=' ')
        print()


# Get random coordinates in matrix
def get_coordinates(iv_range_x, iv_range_y):
    ro_res = Coordinates(random.randrange(iv_range_x), random.randrange(iv_range_y))
    return ro_res


# Check if selected cell contains a mine
def contains_char(is_coordinates: Coordinates, im_matrix, iv_char):
    if im_matrix[is_coordinates.mv_x][is_coordinates.mv_y] == iv_char:
        rv_res = 'X'
    else:
        rv_res = ''
    return rv_res


# Place a single mine into the matrix
def place_char(is_coordinates: Coordinates, cm_matrix, iv_char):
    cm_matrix[is_coordinates.mv_x][is_coordinates.mv_y] = iv_char


# Check if cell is not out of matrix space
def is_valid_coordinate(is_coordinates: Coordinates, iv_range_x, iv_range_y):
    if is_coordinates.mv_x < 0 or is_coordinates.mv_y < 0 or is_coordinates.mv_x == iv_range_x or is_coordinates.mv_y == iv_range_y:
        rv_res = ''
    else:
        rv_res = 'X'
    return rv_res


# Small wrapper for creating surrounding cells - also checks if adjacent cell still belongs to the matrix
def prepare_cell(is_coordinates: Coordinates, offset_x: int, offset_y: int, iv_range_x, iv_range_y, cs_list: list):
    # Create new instance, so original input is not changed
    coordinates = Coordinates(is_coordinates.mv_x, is_coordinates.mv_y)
    coordinates.mv_x += offset_x
    coordinates.mv_y += offset_y
    if 'X' == is_valid_coordinate(coordinates, iv_range_x, iv_range_y):
        cs_list.append(coordinates)


# Get all adjacent cells for input cell
def get_surrounding_cells(is_coordinates: Coordinates, iv_range_x, iv_range_y):
    result = []
    prepare_cell(is_coordinates, -1, -1, iv_range_x, iv_range_y, result)
    prepare_cell(is_coordinates, -1, 0, iv_range_x, iv_range_y, result)
    prepare_cell(is_coordinates, -1, 1, iv_range_x, iv_range_y, result)
    prepare_cell(is_coordinates, 0, -1, iv_range_x, iv_range_y, result)
    prepare_cell(is_coordinates, 0, 1, iv_range_x, iv_range_y, result)
    prepare_cell(is_coordinates, 1, -1, iv_range_x, iv_range_y, result)
    prepare_cell(is_coordinates, 1, 0, iv_range_x, iv_range_y, result)
    prepare_cell(is_coordinates, 1, 1, iv_range_x, iv_range_y, result)
    return result


# Count mines around cell
def count_mines(is_coordinates: Coordinates, iv_range_x, iv_range_y, cm_matrix):
    if 'X' == contains_char(is_coordinates, cm_matrix, '*'):
        return
    else:
        nb_of_mines = 0
        surroundings = get_surrounding_cells(is_coordinates, iv_range_x, iv_range_y)
        for cell in surroundings:
            if 'X' == contains_char(cell, cm_matrix, '*'):
                nb_of_mines += 1
        cm_matrix[is_coordinates.mv_x][is_coordinates.mv_y] = str(nb_of_mines)


# For all cells that are not mines, count mines that surround them
def count_surroundings(iv_range_x, iv_range_y, cm_matrix):
    for x in range(iv_range_x):
        for y in range(iv_range_y):
            coordinates = Coordinates(x, y)
            count_mines(coordinates, iv_range_x, iv_range_y, cm_matrix)


# Check if spot for a mine is a valid one
def check_mine_spot(iv_range_x, iv_range_y, im_matrix, is_coordinates: Coordinates):
    valid = ''
    surroundings = get_surrounding_cells(is_coordinates, iv_range_x, iv_range_y)
    for cell in surroundings:
        if '' == contains_char(cell, im_matrix, '*'):
            valid = 'X'
            break
        elif gv_debug == 'X':
            print("This is not a valid spot")
    return valid


# Place iv_mines mines into the matrix
def place_mines(iv_mines, iv_range_x, iv_range_y, cm_matrix):
    # Local instance of coordinate provider
    lv_coordProvider = CoordinateProvider(iv_range_x, iv_range_y)
    for i in range(iv_mines):
        # Use infinite loop to insert mines, since random position can already contain a mine
        while True:
            # coordinates = get_coordinates(iv_range_x, iv_range_y)
            coordinates = lv_coordProvider.get_random_coords()
            if 'X' == check_mine_spot(iv_range_x, iv_range_y, cm_matrix, coordinates):
                place_char(coordinates, cm_matrix, '*')
                break

    count_surroundings(iv_range_x, iv_range_y, cm_matrix)


def get_field_value(im_matrix, is_coordinates: Coordinates):
    return im_matrix[is_coordinates.mv_x][is_coordinates.mv_y]


def reveal_fields(im_matrix_hidden, im_matrix_gameboard, is_coordinates: Coordinates, iv_range_x, iv_range_y):
    ll_field = []
    ll_field.append(is_coordinates)
    for ls_field in ll_field:
        lv_revealed_field = get_field_value(im_matrix_hidden, ls_field)
        # lv_revealed_field = str(lv_revealed_field)
        place_char(ls_field, im_matrix_gameboard, lv_revealed_field)
        if lv_revealed_field == '0':
            surroundings = get_surrounding_cells(ls_field, iv_range_x, iv_range_y)
            for cell in surroundings:
                if 'X' == contains_char(cell, im_matrix_gameboard, '?'):
                    ll_field.append(cell)



# Main function, that handles everything
def main():
    lv_range_x = int(input("Enter number of rows: "))
    lv_range_y = int(input('Enter number of columns: '))
    lv_nb_of_mines = int(input("Enter number of mines: "))
    print(lv_range_x)

    lm_matrix_hidden = init_matrix(lv_range_x, lv_range_y, 0)
    place_mines(lv_nb_of_mines, lv_range_x, lv_range_y, lm_matrix_hidden)
    print_matrix(lm_matrix_hidden)
    lm_matrix_gameboard = init_matrix(lv_range_x, lv_range_y, '?')

    while True:
        print()
        print()
        print_matrix(lm_matrix_gameboard)
        lv_option = input("R - Reveal spot, M - Place mine to spot, X - Exit")
        if lv_option == 'X':
            print("See you soon!")
            break
        elif lv_option != 'R' and lv_option != 'M':
            continue

        lv_pos_x = int(input("Enter number of row to be revealed: "))
        lv_pos_y = int(input("Enter number of column to be revealed: "))
        # Do the adjustment, so user doesnt have to index from 0
        lv_coords = Coordinates(lv_pos_x - 1, lv_pos_y - 1)

        # TODO: Check if selected field is not revealed field and check for index leakage
        if 'X' != contains_char(lv_coords, lm_matrix_gameboard, '?'):
            print("Already revealed / mine is placed here")

        if lv_option == 'M':
            place_char(lv_coords, lm_matrix_gameboard, '+')
            continue

        reveal_fields(lm_matrix_hidden, lm_matrix_gameboard, lv_coords, lv_range_x, lv_range_y)
        if 'X' == contains_char(lv_coords, lm_matrix_gameboard, '*'):
            print("You have found a mine, you have lost")
            break


# Call main function
gv_debug = ''
main()
