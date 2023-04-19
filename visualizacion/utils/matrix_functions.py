

DIM_Y_MATRIX = 15
DIM_X_MATRIX = 100
DIM_Y_MATRIX = 500
DIM_X_MATRIX = 20000
def get_pos_media_matrix(matrix_dim):
    pos_y_media = len(matrix_dim) // 2
    pos_x_media = len(matrix_dim[0]) // 2
    return pos_y_media, pos_x_media

def generate_matrix(list_palabras):
    dim_y_matrix = 3 * len(list_palabras) + 50
    dim_x_matrix = 15 * len(list_palabras) + 500

    dim_y_matrix = DIM_Y_MATRIX
    dim_x_matrix = DIM_X_MATRIX
    matrix_dim = [[] for i in range(DIM_Y_MATRIX)]
    for y in range(dim_y_matrix):
        matrix_dim[y] += [0 for x in range(dim_x_matrix)]
    # print(matrix_dim)
    pos_y_media, pos_x_media = get_pos_media_matrix(matrix_dim)
    return matrix_dim, pos_y_media, pos_x_media

