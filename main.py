import random


# Small class to store X a Y coordinate as one object
class Coordinates:
    def __init__(self, iv_x: int, iv_y: int):
        assert isinstance(iv_x, int)
        self.x = iv_x
        assert isinstance(iv_y, int)
        self.y = iv_y


# Initialize matrix to iv_rows and iv_columns - set all values to iv_value
def init_matrix(iv_rows, iv_columns, iv_value):
    em_matrix = []
    for i in range(iv_rows):
        em_matrix.append([iv_value] * iv_columns)

    return em_matrix


# Print whole matrix with separator space
def print_matrix(im_matrix):
    for row in im_matrix:
        for cell in row:
            print(cell, end=' ')
        print()


# Get random coordinates in matrix
def get_coordinates(iv_range_x, iv_range_y):
    res = Coordinates(random.randrange(iv_range_x), random.randrange(iv_range_y))
    return res


# Check if selected cell contains a mine
def contains_mine(is_coordinates: Coordinates, im_matrix):
    if im_matrix[is_coordinates.x][is_coordinates.y] == '*':
        res = 'X'
    else:
        res = ''
    return res


# Place a single mine into the matrix
def place_mine(is_coordinates: Coordinates, cm_matrix):
    cm_matrix[is_coordinates.x][is_coordinates.y] = '*'


# Check if cell is not out of matrix space
def is_valid_coordinate(is_coordinates: Coordinates, iv_range_x, iv_range_y):
    if is_coordinates.x < 0 or is_coordinates.y < 0 or is_coordinates.x == iv_range_x or is_coordinates.y == iv_range_y:
        res = ''
    else:
        res = 'X'
    return res


# Small wrapper for creating surrounding cells - also checks if adjacent cell still belongs to the matrix
def prepare_cell(is_coordinates: Coordinates, offset_x: int, offset_y: int, iv_range_x, iv_range_y, cs_list: list):
    # Create new instance, so original input is not changed
    coordinates = Coordinates(is_coordinates.x, is_coordinates.y)
    coordinates.x = coordinates.x + offset_x
    coordinates.y = coordinates.y + offset_y
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
    if 'X' == contains_mine(is_coordinates, cm_matrix):
        return
    else:
        nb_of_mines = 0
        surroundings = get_surrounding_cells(is_coordinates, iv_range_x, iv_range_y)
        for cell in surroundings:
            if 'X' == contains_mine(cell, cm_matrix):
                nb_of_mines = nb_of_mines + 1
        cm_matrix[is_coordinates.x][is_coordinates.y] = nb_of_mines


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
        if '' == contains_mine(cell, im_matrix):
            valid = 'X'
            break
        else:
            print("This is not a valid spot")
    return valid


# Place iv_mines mines into the matrix
def place_mines(iv_mines, iv_range_x, iv_range_y, cm_matrix):
    for i in range(iv_mines):
        # Use infinite loop to insert mines, since random position can already contain a mine
        while True:
            coordinates = get_coordinates(iv_range_x, iv_range_y)
            if '' == contains_mine(coordinates, cm_matrix) and 'X' == check_mine_spot(iv_range_x, iv_range_y, cm_matrix, coordinates):
                place_mine(coordinates, cm_matrix)
                break
            #else:
            #    print("This place already contains mine or its not valid place")

    count_surroundings(iv_range_x, iv_range_y, cm_matrix)


# Main function, that handles everything
def main(iv_range_x, iv_range_y, iv_nb_of_mines):
    lm_matrix = init_matrix(iv_range_x, iv_range_y, 0)
    place_mines(iv_nb_of_mines, iv_range_x, iv_range_y, lm_matrix)
    print_matrix(lm_matrix)


# Call main function
main(3, 3, 8)
