

PRINT_MATRIX = True

DIM_Y_MATRIX = 50
DIM_X_MATRIX = 200
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


def imprimir_matriz(matriz, apply_num_inicial_col=True):
    try:
        if not PRINT_MATRIX:
            return
        matriz = matriz.copy()
        matriz = reducir_tam_matriz(matriz)
        print("-----------------------------------------------------------------------")
        i, j = 0, 0
        print(f"    ", end="")
        for elemento in matriz[0]:
            print(f"{i:<4}", end="")
            i += 1
        print()

        for fila in matriz:
            print(f"{j:<4}", end="")
            num_col = 0
            for elemento in fila:
                if elemento == 0:
                    print(f"{elemento:<4}", end="")
                else:
                    print(f"{elemento:<4}", end="")
                num_col += 1
            j += 1
            print()
        print("-----------------------------------------------------------------------")
    except Exception as e:
        print(e)
        pass


def reducir_tam_matriz(matrix_dim):
    # Reducir Matriz
    matrix_dim = matrix_dim.copy()
    matrix_dim_copy = matrix_dim.copy()
    for x in matrix_dim_copy:
        if sum(x) == 0:
            matrix_dim.pop(0)
        else:
            break
    matrix_dim_reverse = matrix_dim.copy()
    matrix_dim_reverse.reverse()
    for x in matrix_dim_reverse:
        if sum(x) == 0:
            matrix_dim.pop()
        else:
            break
    matrix_dim_transpose = [list(fila) for fila in zip(*matrix_dim)]
    matrix_dim_transpose_copy = matrix_dim_transpose.copy()
    for x in matrix_dim_transpose_copy:
        if sum(x) == 0:
            matrix_dim_transpose.pop(0)
        else:
            break
    matrix_dim_transpose_reverse = matrix_dim_transpose.copy()
    matrix_dim_transpose_reverse.reverse()
    for x in matrix_dim_transpose_reverse:
        if sum(x) == 0:
            matrix_dim_transpose.pop()
        else:
            break
    matrix_dim = [list(fila) for fila in zip(*matrix_dim_transpose)]
    return matrix_dim



def ampliar_matriz(matrix_dim):
    AMPLIAR_X = 200
    AMPLIAR_Y = 50
    MARGEN_Y = 50
    MARGEN_X = 100
    print("################## Ampliando matriz")
    # comprueba los bordes de la matriz y en caso de existir alguno con un valor != 0

    # amplia la matriz en 250 en x y en y
    dim_y_matrix = len(matrix_dim)
    dim_x_matrix = len(matrix_dim[0])
    matrix_dim_copy = matrix_dim.copy()

    conteo_arriba = 0
    sumar_arriba = False
    for x in matrix_dim_copy:
        if sum(x) == 0:
            conteo_arriba +=1
        else:
            sumar_arriba = True
            break
        if conteo_arriba > MARGEN_Y:
            break


    conteo_abajo = 0
    sumar_abajo = False
    # recorrer la matriz al reves
    for x in matrix_dim_copy[::-1]:
        if sum(x) == 0:
            conteo_abajo +=1
        else:
            sumar_abajo = True
            break
        if conteo_arriba > MARGEN_Y:
            break

    conteo_dcha = 0
    sumar_dcha = False
    # recorrer la matriz al reves
    for x in matrix_dim_copy[::-1]:
        if sum(x) == 0:
            conteo_abajo += 1
        else:
            sumar_abajo = True
            break
        if conteo_arriba > MARGEN_Y:
            break

    matrix_dim_transpose = [list(fila) for fila in zip(*matrix_dim)]
    matrix_dim_transpose_copy = matrix_dim_transpose.copy()
    conteo_dcha = 0
    sumar_dcha = False
    for x in matrix_dim_transpose_copy:
        if sum(x) == 0:
            conteo_dcha += 1
        else:
            sumar_dcha = True
            break
        if conteo_dcha > MARGEN_X:
            break

    conteo_izq = 0
    sumar_izq = False
    for x in matrix_dim_transpose_copy[::-1]:
        if sum(x) == 0:
            conteo_izq += 1
        else:
            sumar_izq = True
            break
        if conteo_izq > MARGEN_X:
            break

    # Se suman en ambos lados lo mismo y asi la posicion media sigue siendo el centro :)
    if sumar_arriba or sumar_abajo:
        print("############# Sumando arriba")
        matrix_dim = [[0 for x in range(dim_x_matrix)] for y in range(AMPLIAR_Y)] + matrix_dim
    if sumar_abajo or sumar_arriba:
        print("############# Sumando abajo")
        matrix_dim = matrix_dim + [[0 for x in range(dim_x_matrix)] for y in range(AMPLIAR_Y)]
    if sumar_dcha or sumar_izq:
        print("############# Sumando dcha")
        matrix_dim = [x + [0 for x in range(AMPLIAR_X)] for x in matrix_dim]
    if sumar_izq or sumar_dcha:
        print("############# Sumando izq")
        matrix_dim = [[0 for x in range(AMPLIAR_X)] + x for x in matrix_dim]
    return matrix_dim


MARGIN_RELATION_ARRIBA = 2
MARGIN_RELATION_DCHA = 2
MARGIN_RELATION_DCHA_ARRIBA = 6
def is_empty_relation_in_matrix(matrix, y_dest, x_dest, relacion):
    if relacion.has_been_plotted:
       return True, matrix
    pal_origen = relacion.pal_origen
    pal_dest = relacion.pal_dest
    x_origen = pal_origen.pos_x
    y_origen = pal_origen.pos_y
    if x_origen is None or x_dest is None or y_origen is None or y_dest is None:
        return True, matrix

    try:
        y = min(y_origen, y_dest)
        x = min(x_origen, x_dest)
        x_repres = x
        y_repres = y

        if (x_dest - x_origen) == 0:  # ARRIBA O ABAJO
            pos_y = max(y_origen, y_dest) - y_repres
            is_empty, matrix = is_empty_pos_matrix(matrix, pos_y, x_origen, MARGIN_RELATION_ARRIBA, MARGIN_RELATION_ARRIBA, ampliar=False)
            return is_empty, matrix

        if (y_dest - y_origen) == 0: # DCHA O IZQ
            pos_x = max(x_origen, x_dest) - x_repres
            is_empty, matrix = is_empty_pos_matrix(matrix, y_origen, pos_x, MARGIN_RELATION_DCHA, MARGIN_RELATION_DCHA, ampliar=False)
            return is_empty, matrix

        # DCHA_ARRIBA o IZQ_ABAJO # DCHA_ABAJO o IZQ_ARRIBA
        if x_repres < max(x_origen, x_dest) and y_repres < max(y_origen, y_dest):
            pos_y = max(y_origen, y_dest) - y_repres
            pos_x = max(x_origen, x_dest) - x_repres
            is_empty, matrix = is_empty_pos_matrix(matrix, pos_y, pos_x, MARGIN_RELATION_DCHA_ARRIBA, MARGIN_RELATION_DCHA_ARRIBA, ampliar=False)
            return is_empty, matrix

        return True, matrix
    except:
        return True, matrix







def is_empty_pos_matrix(matrix, pos_y, pos_x, dim_y, dim_x, margen_x=0, ampliar=True):
    # Acuerdate que es la posicion centrada, es decir, da igual si es yendo a la izq o derecha o arriba o abajo
    try:
        dim_x_bis = dim_x
        pox_x_bis = pos_x
        if margen_x < 0:
            pox_x_bis = pos_x + margen_x  # asi empieza en una posicion anterior.
        elif margen_x > 0:
            dim_x_bis = dim_x + margen_x

        for axis_x_loop in range(pox_x_bis, pos_x + dim_x_bis):
            axis_x = axis_x_loop - dim_x // 2
            for axis_y_loop in range(pos_y, pos_y + dim_y):
                axis_y = axis_y_loop - dim_y // 2
                if matrix[axis_y][axis_x] != 0:
                    return False, matrix
        return True, matrix
    except:
        if ampliar:
            matrix = ampliar_matriz(matrix)
            return is_empty_pos_matrix(matrix, pos_y, pos_x, dim_y, dim_x, margen_x)
        else:
            return True, matrix
def find_better_center_position(matrix_dim, palabra, pos_y_media, pos_x_media):
    # TODO esta va a ser simple. Si el 0,0 esta ocupado, pones el -500, 0. Luego el -1000,0. Y asi sucesivamente,
    # haces una funcion de apliar matriz y ale. Y luego, reduces la matrix y las posiciones y ya está.

    pos_x = pos_x_media
    # Lo que hace es recorrer de 200 en 200 los elementos.
    for pos_y in range(pos_y_media, 0, -20):
        is_empty, matrix_dim = is_empty_pos_matrix(matrix_dim, pos_y, pos_x, dim_y=5, dim_x=10)
        if is_empty:
            return pos_y, pos_x, matrix_dim

    return pos_y_media, pos_x, matrix_dim
