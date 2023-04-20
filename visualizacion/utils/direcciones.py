from visualizacion.utils.matrix_functions import get_pos_media_matrix
from constants.direcciones_relaciones import DIR_DCHA, DIR_DCHA_ABAJO, DIR_DCHA_ARRIBA, DIR_ABAJO, DIR_ARRIBA, \
    DIR_IZQ, DIR_IZQ_ARRIBA, DIR_IZQ_ABAJO, FIND_DIR_CENTRO, FIND_DIR_DCHA, FIND_DIR_DCHA_ABAJO, FIND_DIR_DCHA_ARRIBA, \
    FIND_DIR_ABAJO, FIND_DIR_ARRIBA, FIND_DIR_IZQ, FIND_DIR_IZQ_ARRIBA, FIND_DIR_IZQ_ABAJO, DICT_DIR_BY_ORIGEN, CENTRO



def is_empty_pos_matrix(matrix, pos_y, pos_x, dim_y, dim_x):
    for axis_x_loop in range(pos_x, pos_x + dim_x):
        axis_x = axis_x_loop - dim_x//2
        for axis_y_loop in range(pos_y, pos_y + dim_y):
            axis_y = axis_y_loop - dim_y//2
            if matrix[axis_y][axis_x] != 0:
                return False
    return True


def find_better_center_position(matrix_dim, palabra, pos_y_media, pos_x_media):
    # TODO esta va a ser simple. Si el 0,0 esta ocupado, pones el -500, 0. Luego el -1000,0. Y asi sucesivamente,
    # haces una funcion de apliar matriz y ale. Y luego, reduces la matrix y las posiciones y ya está.

    pos_x = pos_x_media
    # Lo que hace es recorrer de 200 en 200 los elementos.
    for pos_y in range(pos_y_media, 0, -20):
        if is_empty_pos_matrix(matrix_dim, pos_y, pos_x, dim_y=5, dim_x=10):
            return pos_y, pos_x

    return pos_y_media, pos_x


def get_pos_dir_dcha(matrix_dim, palabra, relation):
    DISTANCIA_DE_INTENTO_X = 15
    DISTANCIA_DE_INTENTO_X = 1500
    pos_y = relation.pal_origen.pos_y + relation.cte_sum_y
    pos_x = relation.pal_origen.pos_x + (relation.tam_text + relation.cte_sum_x)

    for x_loop in range(pos_x, pos_x+DISTANCIA_DE_INTENTO_X):
        if is_empty_pos_matrix(
                matrix_dim, pos_y, x_loop,
                dim_y=palabra.dimension_y + palabra.cte_sum_y,
                dim_x=palabra.dimension + palabra.cte_sum_x):
            return pos_y, x_loop

    # No ha sido encontrado. Hay que buscar la siguiente posicion.
    #TODO:  en caso de que falle, tengo que pasar a la siguiente lista de direccion y buscar la siguiente posicion.
    #  esto como se haria? pues se me ocurre:
    # 1. aqui haces eso de pasar a la siguiente lista de direccion.
    # 2. aumentas en 1 el numero de direccion de la palabra origen y luego en la funcion principal compruebas que
    # es ese el que tocaba o no
    # 3. Si no es el que tocaba, tienes que repetir esa relacion pero con esa nueva direccion que le vas a asignar
    # tal vez haya que sacar esa parte a una nueva funcion para poder llamarle aunque el bucle no lo permita.
    # Ya sabes, un while Dir_ok == False:  y dentro esa mierda :)

    # num_dir_pal_origen = len(relation.pal_origen.lista_direcciones_orden)
    # find_dir = DICT_DIR_BY_ORIGEN.get(relation.pal_origen.direccion_origen)
    # list_direcciones_orden = find_dir[num_dir_pal_origen] # En esta ocasion no le resto 1


    return pos_y, pos_x




def get_pos_dir_dcha_arriba():
    pass


def get_next_location(matrix_dim, palabra, relation):
    pos_y_media, pos_x_media = get_pos_media_matrix(matrix_dim)
    dir_origen = palabra.direccion_origen
    pos_y, pos_x = pos_y_media, pos_x_media

    if dir_origen == CENTRO or relation is None:
        pos_y, pos_x = find_better_center_position(matrix_dim, palabra, pos_y_media, pos_x_media)

    elif dir_origen == DIR_DCHA:
        pos_y, pos_x = get_pos_dir_dcha(matrix_dim, palabra, relation)

    elif dir_origen == DIR_IZQ:
        pos_y = relation.pal_origen.pos_y
        pos_x = relation.pal_origen.pos_x - (relation.tam_text + 1) - (palabra.dimension + 2)

    elif dir_origen == DIR_ARRIBA:
        #TODO para abajo y arriba, acuerdate de poner que no haya nada en la fila en un margen amplio (40 casilla 'y')
        pos_y = relation.pal_origen.pos_y + (relation.tam_text + 4)
        pos_x = relation.pal_origen.pos_x

    elif dir_origen == DIR_ABAJO:
        # TODO para abajo y arriba, acuerdate de poner que no haya nada en la fila en un margen amplio (40 casilla 'y')
        pos_y = relation.pal_origen.pos_y - (relation.tam_text + 4)
        pos_x = relation.pal_origen.pos_x

    elif dir_origen == DIR_DCHA_ARRIBA:
        # TODO para abajo y arriba, acuerdate de poner que no haya nada en la fila en un margen amplio (20 casilla 'y')
        pos_y = relation.pal_origen.pos_y - (relation.tam_text + 1) - (palabra.dimension + 2)
        pos_x = relation.pal_origen.pos_x + (relation.tam_text + 1) + (palabra.dimension + 2)

    elif dir_origen == DIR_DCHA_ABAJO:
        # TODO para abajo y arriba, acuerdate de poner que no haya nada en la fila en un margen amplio (20 casilla 'y')
        pos_y = relation.pal_origen.pos_y + (relation.tam_text + 1) + (palabra.dimension + 2)
        pos_x = relation.pal_origen.pos_x + (relation.tam_text + 1) + (palabra.dimension + 2)

    elif dir_origen == DIR_IZQ_ARRIBA:
        # TODO para abajo y arriba, acuerdate de poner que no haya nada en la fila en un margen amplio (20 casilla 'y')
        pos_y = relation.pal_origen.pos_y - (relation.tam_text + 1) - (palabra.dimension + 2)
        pos_x = relation.pal_origen.pos_x - (relation.tam_text + 1) - (palabra.dimension + 2)

    elif dir_origen == DIR_IZQ_ABAJO:
        # TODO para abajo y arriba, acuerdate de poner que no haya nada en la fila en un margen amplio (20 casilla 'y')
        pos_y = relation.pal_origen.pos_y + (relation.tam_text + 1) + (palabra.dimension + 2)
        pos_x = relation.pal_origen.pos_x - (relation.tam_text + 1) - (palabra.dimension + 2)

    palabra.pos_x = pos_x
    palabra.pos_y = pos_y

    return pos_y, pos_x
