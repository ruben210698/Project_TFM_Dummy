from visualizacion.utils.matrix_functions import get_pos_media_matrix
from constants.direcciones_relaciones import DIR_DCHA, DIR_DCHA_ABAJO, DIR_DCHA_ARRIBA, DIR_ABAJO, DIR_ARRIBA, \
    DIR_IZQ, DIR_IZQ_ARRIBA, DIR_IZQ_ABAJO, FIND_DIR_CENTRO, FIND_DIR_DCHA, FIND_DIR_DCHA_ABAJO, FIND_DIR_DCHA_ARRIBA, \
    FIND_DIR_ABAJO, FIND_DIR_ARRIBA, FIND_DIR_IZQ, FIND_DIR_IZQ_ARRIBA, FIND_DIR_IZQ_ABAJO, DICT_DIR_BY_ORIGEN, CENTRO

def ampliar_matriz(matrix_dim):
    AMPLIAR_X = 250
    AMPLIAR_Y = 150
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

    if sumar_arriba:
        print("############# Sumando arriba")
        matrix_dim = [[0 for x in range(dim_x_matrix)] for y in range(AMPLIAR_Y)] + matrix_dim
    if sumar_abajo:
        print("############# Sumando abajo")
        matrix_dim = matrix_dim + [[0 for x in range(dim_x_matrix)] for y in range(AMPLIAR_Y)]
    if sumar_dcha:
        print("############# Sumando dcha")
        matrix_dim = [x + [0 for x in range(AMPLIAR_X)] for x in matrix_dim]
    if sumar_izq:
        print("############# Sumando izq")
        matrix_dim = [[0 for x in range(AMPLIAR_X)] + x for x in matrix_dim]
    return matrix_dim





def is_empty_pos_matrix(matrix, pos_y, pos_x, dim_y, dim_x, margen_x=0):
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
        matrix = ampliar_matriz(matrix)
        return is_empty_pos_matrix(matrix, pos_y, pos_x, dim_y, dim_x, margen_x)

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


def update_list_dir_order(relation):
    try:
        print(f"-----Fallo en la direccion {relation.pal_origen.texto} :: {relation.pal_dest.texto}")
    except:
        pass
    list_dir_origen_actual = relation.pal_origen.lista_direcciones_orden
    dir_pal_origen = relation.pal_origen.direccion_origen
    num_dir_pal_origen = len(list_dir_origen_actual)
    find_dir = DICT_DIR_BY_ORIGEN.get(dir_pal_origen)
    new_list_direcciones_orden = find_dir[num_dir_pal_origen]  # antes se le restaba 1
    relation.pal_origen.lista_direcciones_orden = new_list_direcciones_orden
    # relation.pal_origen.pos_actual_recorrer_dir_relaciones += 1  # de esta forma se salta el elemento actual
    ## No esto no lo hagas porque sino sumas 2, que ahora he puesto el bucle como While

    # No ha sido encontrado. Hay que buscar la siguiente posicion.
    # En caso de que falle, tengo que pasar a la siguiente lista de direccion y buscar la siguiente posicion.
    #  esto como se haria? pues se me ocurre:
    # 1. aqui haces eso de pasar a la siguiente lista de direccion.
    # 2. aumentas en 1 el numero de direccion de la palabra origen y luego en la funcion principal compruebas que
    # es ese el que tocaba o no
    # 3. Si no es el que tocaba, tienes que repetir esa relacion pero con esa nueva direccion que le vas a asignar
    # tal vez haya que sacar esa parte a una nueva funcion para poder llamarle aunque el bucle no lo permita.
    # Ya sabes, un while Dir_ok == False:  y dentro esa mierda :)



RECTA_DISTANCIA_DE_INTENTO_X = 15

def get_pos_dir_dcha(matrix_dim, palabra, relation):
    if relation is None:
        return None, None, matrix_dim
    pos_y = relation.pal_origen.pos_y
    pos_x = relation.pal_origen.pos_x + (relation.tam_text + relation.cte_sum_x)

    for x_loop in range(pos_x, pos_x + RECTA_DISTANCIA_DE_INTENTO_X, 1):
        is_empty, matrix_dim = is_empty_pos_matrix(
                matrix_dim, pos_y, x_loop,
                dim_y=palabra.dimension_y + palabra.cte_sum_y,
                dim_x=palabra.dimension + palabra.cte_sum_x)
        if is_empty:
            return pos_y, x_loop, matrix_dim

    update_list_dir_order(relation)

    return None, None, matrix_dim



RECTA_DISTANCIA_DE_INTENTO_Y = 15
RECTA_MARGIN = 40
ARRIBA_MARGIN_MIN = 3

def get_pos_dir_arriba(matrix_dim, palabra, relation):
    if relation is None:
        return None, None, matrix_dim
    pos_y = relation.pal_origen.pos_y + (palabra.dimension_y + palabra.cte_sum_y)//2 + ARRIBA_MARGIN_MIN
    pos_x = relation.pal_origen.pos_x

    for y_loop in range(pos_y, pos_y + RECTA_DISTANCIA_DE_INTENTO_Y, 1):
        is_empty, matrix_dim = is_empty_pos_matrix(
                matrix_dim, y_loop, pos_x,
                dim_y=palabra.dimension_y + palabra.cte_sum_y,
                dim_x=palabra.dimension + palabra.cte_sum_x,
                margen_x=RECTA_MARGIN)
        if is_empty:
            return y_loop, pos_x, matrix_dim

    update_list_dir_order(relation)

    return None, None, matrix_dim


def get_pos_dir_abajo(matrix_dim, palabra, relation):
    if relation is None:
        return None, None, matrix_dim
    pos_y = relation.pal_origen.pos_y - (palabra.dimension_y + palabra.cte_sum_y)//2 - ARRIBA_MARGIN_MIN
    pos_x = relation.pal_origen.pos_x

    for y_loop in range(pos_y, pos_y - RECTA_DISTANCIA_DE_INTENTO_Y, -1):
        is_empty, matrix_dim = is_empty_pos_matrix(
                matrix_dim, y_loop, pos_x,
                dim_y=palabra.dimension_y + palabra.cte_sum_y,
                dim_x=palabra.dimension + palabra.cte_sum_x,
                margen_x=RECTA_MARGIN)  # va a la dcha
        if is_empty:
            return y_loop, pos_x, matrix_dim

    update_list_dir_order(relation)

    return None, None, matrix_dim


def get_pos_dir_izq(matrix_dim, palabra, relation):
    if relation is None:
        return None, None, matrix_dim
    pos_y = relation.pal_origen.pos_y
    pos_x = relation.pal_origen.pos_x - (relation.tam_text + relation.cte_sum_x)

    for x_loop in range(pos_x, pos_x - RECTA_DISTANCIA_DE_INTENTO_X, -1):
        is_empty, matrix_dim = is_empty_pos_matrix(
                matrix_dim, pos_y, x_loop,
                dim_y=palabra.dimension_y + palabra.cte_sum_y,
                dim_x=palabra.dimension + palabra.cte_sum_x)
        if is_empty:
            return pos_y, x_loop, matrix_dim

    update_list_dir_order(relation)

    return None, None, matrix_dim




DIAGONAL_DISTANCIA_DE_INTENTO_Y = 4
DIAGONAL_Y_1 = 4
DIAGONAL_Y_2 = 8
DIAGONAL_Y_3 = 12
DIAGONAL_LIST_YS = [DIAGONAL_Y_1, DIAGONAL_Y_2, DIAGONAL_Y_3]
DIAGONAL_DISTANCIA_DE_INTENTO_X = 5
DIAGONAL_X_1 = 3
DIAGONAL_X_2 = 8
DIAGONAL_X_3 = 13
DIAGONAL_LIST_XS = [DIAGONAL_X_1, DIAGONAL_X_2, DIAGONAL_X_3]
DIAGONAL_MARGIN_X = 20


def get_pos_dir_dcha_arriba(matrix_dim, palabra, relation):
    if relation is None:
        return None, None, matrix_dim

    for i in range(0, len(DIAGONAL_LIST_YS)):
        pos_y = relation.pal_origen.pos_y + DIAGONAL_LIST_YS[i]
        pos_x = relation.pal_origen.pos_x + relation.pal_origen.dimension + relation.pal_origen.cte_sum_x +  DIAGONAL_LIST_XS[i]

        for y_loop in range(pos_y, pos_y + DIAGONAL_DISTANCIA_DE_INTENTO_Y, 1):
            for x_loop in range(pos_x, pos_x + DIAGONAL_DISTANCIA_DE_INTENTO_X, 1):
                is_empty, matrix_dim = is_empty_pos_matrix(
                        matrix_dim, y_loop, x_loop,
                        dim_y=palabra.dimension_y + palabra.cte_sum_y,
                        dim_x=palabra.dimension + palabra.cte_sum_x,
                        margen_x=DIAGONAL_MARGIN_X)
                if is_empty:
                    return pos_y, x_loop, matrix_dim

    update_list_dir_order(relation)
    return None, None, matrix_dim


def get_pos_dir_dcha_abajo(matrix_dim, palabra, relation):
    if relation is None:
        return None, None, matrix_dim

    for i in range(0, len(DIAGONAL_LIST_YS)):
        pos_y = relation.pal_origen.pos_y - DIAGONAL_LIST_YS[i]
        pos_x = relation.pal_origen.pos_x + relation.pal_origen.dimension + relation.pal_origen.cte_sum_x + DIAGONAL_LIST_XS[i]


        for y_loop in range(pos_y, pos_y - DIAGONAL_DISTANCIA_DE_INTENTO_Y, -1):
            for x_loop in range(pos_x, pos_x + DIAGONAL_DISTANCIA_DE_INTENTO_X, 1):
                is_empty, matrix_dim = is_empty_pos_matrix(
                        matrix_dim, y_loop, x_loop,
                        dim_y=palabra.dimension_y + palabra.cte_sum_y,
                        dim_x=palabra.dimension + palabra.cte_sum_x,
                        margen_x=DIAGONAL_MARGIN_X)
                if is_empty:
                    return pos_y, x_loop, matrix_dim

    update_list_dir_order(relation)

    return None, None, matrix_dim


def get_pos_dir_izq_abajo(matrix_dim, palabra, relation):
    if relation is None:
        return None, None, matrix_dim

    for i in range(0, len(DIAGONAL_LIST_YS)):
        pos_y = relation.pal_origen.pos_y - DIAGONAL_LIST_YS[i]
        pos_x = relation.pal_origen.pos_x - (relation.pal_origen.dimension + relation.pal_origen.cte_sum_x) - DIAGONAL_LIST_XS[i]

        for y_loop in range(pos_y, pos_y - DIAGONAL_DISTANCIA_DE_INTENTO_Y, -1):
            for x_loop in range(pos_x, pos_x - DIAGONAL_DISTANCIA_DE_INTENTO_X, -1):
                is_empty, matrix_dim = is_empty_pos_matrix(
                        matrix_dim, y_loop, x_loop,
                        dim_y=palabra.dimension_y + palabra.cte_sum_y,
                        dim_x=palabra.dimension + palabra.cte_sum_x,
                        margen_x=-DIAGONAL_MARGIN_X)
                if is_empty:
                    return pos_y, x_loop, matrix_dim

    update_list_dir_order(relation)
    return None, None, matrix_dim


def get_pos_dir_izq_arriba(matrix_dim, palabra, relation):
    if relation is None:
        return None, None, matrix_dim

    for i in range(0, len(DIAGONAL_LIST_YS)):
        pos_y = relation.pal_origen.pos_y + DIAGONAL_LIST_YS[i]
        pos_x = relation.pal_origen.pos_x - (relation.pal_origen.dimension + relation.pal_origen.cte_sum_x) - DIAGONAL_LIST_XS[i]

        for y_loop in range(pos_y, pos_y + DIAGONAL_DISTANCIA_DE_INTENTO_Y, 1):
            for x_loop in range(pos_x, pos_x - DIAGONAL_DISTANCIA_DE_INTENTO_X, -1):
                is_empty, matrix_dim = is_empty_pos_matrix(
                        matrix_dim, y_loop, x_loop,
                        dim_y=palabra.dimension_y + palabra.cte_sum_y,
                        dim_x=palabra.dimension + palabra.cte_sum_x,
                        margen_x=-DIAGONAL_MARGIN_X)
                if is_empty:
                    return pos_y, x_loop, matrix_dim

    update_list_dir_order(relation)
    return None, None, matrix_dim

def get_next_location(matrix_dim, palabra, relation):
    pos_y_media, pos_x_media = get_pos_media_matrix(matrix_dim)
    dir_origen = palabra.direccion_origen
    pos_y, pos_x = pos_y_media, pos_x_media

    if dir_origen == CENTRO or relation is None:
        pos_y, pos_x, matrix_dim = find_better_center_position(matrix_dim, palabra, pos_y_media, pos_x_media)

    elif dir_origen == DIR_DCHA:
        pos_y, pos_x, matrix_dim = get_pos_dir_dcha(matrix_dim, palabra, relation)

    elif dir_origen == DIR_IZQ:
        pos_y, pos_x, matrix_dim = get_pos_dir_izq(matrix_dim, palabra, relation)

    elif dir_origen == DIR_ARRIBA:
        pos_y, pos_x, matrix_dim = get_pos_dir_arriba(matrix_dim, palabra, relation)

    elif dir_origen == DIR_ABAJO:
        pos_y, pos_x, matrix_dim = get_pos_dir_abajo(matrix_dim, palabra, relation)

    elif dir_origen == DIR_DCHA_ARRIBA:
        pos_y, pos_x, matrix_dim = get_pos_dir_dcha_arriba(matrix_dim, palabra, relation)

    elif dir_origen == DIR_DCHA_ABAJO:
        pos_y, pos_x, matrix_dim = get_pos_dir_dcha_abajo(matrix_dim, palabra, relation)

    elif dir_origen == DIR_IZQ_ARRIBA:
        pos_y, pos_x, matrix_dim = get_pos_dir_izq_arriba(matrix_dim, palabra, relation)

    elif dir_origen == DIR_IZQ_ABAJO:
        pos_y, pos_x, matrix_dim = get_pos_dir_izq_abajo(matrix_dim, palabra, relation)

    palabra.pos_x = pos_x
    palabra.pos_y = pos_y

    return pos_y, pos_x, matrix_dim
