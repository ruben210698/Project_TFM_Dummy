# Por orden de importancia y con el valor el grado en el circulo.
# No son grados precisos, simplemente son aproximaciones para hacerse una idea de la direccion si se ve como un circulo
CENTRO = "CENTRO"
DIR_DCHA = "0"
DIR_DCHA_ABAJO = "315"  # Abajo
DIR_DCHA_ARRIBA = "45"  # Arriba

DIR_ABAJO = "270"
DIR_ARRIBA = "90"

DIR_IZQ = "180"
DIR_IZQ_ARRIBA = "135"
DIR_IZQ_ABAJO = "225"

LIST_DIR_CENTRO_1 = [DIR_DCHA]
LIST_DIR_CENTRO_2 = [DIR_DCHA_ABAJO, DIR_DCHA_ARRIBA]
LIST_DIR_CENTRO_3 = [DIR_DCHA, DIR_ABAJO, DIR_ARRIBA]
LIST_DIR_CENTRO_4 = [DIR_DCHA, DIR_ABAJO, DIR_ARRIBA, DIR_IZQ]
LIST_DIR_CENTRO_5 = [DIR_DCHA, DIR_DCHA_ABAJO, DIR_DCHA_ARRIBA, DIR_IZQ, DIR_IZQ_ARRIBA]
LIST_DIR_CENTRO_6 = [DIR_DCHA, DIR_DCHA_ABAJO, DIR_DCHA_ARRIBA, DIR_ABAJO, DIR_ARRIBA, DIR_IZQ]
LIST_DIR_CENTRO_7 = [DIR_DCHA, DIR_DCHA_ABAJO, DIR_DCHA_ARRIBA, DIR_ABAJO, DIR_ARRIBA, DIR_IZQ_ARRIBA, DIR_IZQ_ABAJO]
LIST_DIR_CENTRO_8 = [DIR_DCHA, DIR_DCHA_ABAJO, DIR_DCHA_ARRIBA, DIR_ABAJO, DIR_ARRIBA, DIR_IZQ, DIR_IZQ_ARRIBA,
                     DIR_IZQ_ABAJO]

FIND_DIR_CENTRO = [LIST_DIR_CENTRO_1, LIST_DIR_CENTRO_2, LIST_DIR_CENTRO_3, LIST_DIR_CENTRO_4, LIST_DIR_CENTRO_5,
                   LIST_DIR_CENTRO_6, LIST_DIR_CENTRO_7, LIST_DIR_CENTRO_8]

LIST_DIR_DCHA_1 = [DIR_DCHA]
LIST_DIR_DCHA_2 = [DIR_DCHA_ABAJO, DIR_DCHA_ARRIBA]
LIST_DIR_DCHA_3 = [DIR_DCHA, DIR_ABAJO, DIR_ARRIBA]
LIST_DIR_DCHA_4 = [DIR_DCHA, DIR_DCHA_ARRIBA, DIR_ARRIBA, DIR_DCHA_ABAJO]
LIST_DIR_DCHA_5 = [DIR_DCHA, DIR_DCHA_ABAJO, DIR_DCHA_ARRIBA, DIR_ABAJO, DIR_ARRIBA]
LIST_DIR_DCHA_6 = [DIR_DCHA, DIR_DCHA_ABAJO, DIR_DCHA_ARRIBA, DIR_ABAJO, DIR_IZQ_ARRIBA, DIR_ARRIBA]
LIST_DIR_DCHA_7 = [DIR_DCHA, DIR_DCHA_ABAJO, DIR_DCHA_ARRIBA, DIR_IZQ_ARRIBA, DIR_ARRIBA, DIR_IZQ_ABAJO, DIR_ABAJO]

FIND_DIR_DCHA = [LIST_DIR_DCHA_1, LIST_DIR_DCHA_2, LIST_DIR_DCHA_3, LIST_DIR_DCHA_4, LIST_DIR_DCHA_5, LIST_DIR_DCHA_6,
                 LIST_DIR_DCHA_7]

LIST_DIR_IZQ_1 = [DIR_IZQ]
LIST_DIR_IZQ_2 = [DIR_IZQ_ARRIBA, DIR_IZQ_ABAJO]
LIST_DIR_IZQ_3 = [DIR_IZQ, DIR_ABAJO, DIR_ARRIBA]
LIST_DIR_IZQ_4 = [DIR_IZQ, DIR_ABAJO, DIR_ARRIBA, DIR_ARRIBA]
LIST_DIR_IZQ_5 = [DIR_IZQ, DIR_IZQ_ARRIBA, DIR_IZQ_ABAJO, DIR_ABAJO, DIR_ARRIBA]
LIST_DIR_IZQ_6 = [DIR_IZQ, DIR_IZQ_ARRIBA, DIR_IZQ_ABAJO, DIR_ABAJO, DIR_DCHA_ARRIBA, DIR_ARRIBA]
LIST_DIR_IZQ_7 = [DIR_IZQ, DIR_IZQ_ARRIBA, DIR_IZQ_ABAJO, DIR_DCHA_ARRIBA, DIR_ARRIBA, DIR_DCHA_ABAJO, DIR_ABAJO]

FIND_DIR_IZQ = [LIST_DIR_IZQ_1, LIST_DIR_IZQ_2, LIST_DIR_IZQ_3, LIST_DIR_IZQ_4, LIST_DIR_IZQ_5, LIST_DIR_IZQ_6,
                LIST_DIR_IZQ_7]

LIST_DIR_ARRIBA_1 = [DIR_ARRIBA]
LIST_DIR_ARRIBA_2 = [DIR_DCHA_ARRIBA, DIR_IZQ_ARRIBA]
LIST_DIR_ARRIBA_3 = [DIR_ARRIBA, DIR_DCHA_ARRIBA, DIR_IZQ_ARRIBA]
LIST_DIR_ARRIBA_4 = [DIR_ARRIBA, DIR_DCHA_ARRIBA, DIR_IZQ_ARRIBA, DIR_DCHA]
LIST_DIR_ARRIBA_5 = [DIR_ARRIBA, DIR_DCHA_ARRIBA, DIR_IZQ_ARRIBA, DIR_DCHA, DIR_IZQ]
LIST_DIR_ARRIBA_6 = [DIR_ARRIBA, DIR_DCHA_ARRIBA, DIR_IZQ_ARRIBA, DIR_DCHA_ABAJO, DIR_DCHA, DIR_IZQ]
LIST_DIR_ARRIBA_7 = [DIR_ARRIBA, DIR_DCHA_ARRIBA, DIR_IZQ_ARRIBA, DIR_DCHA_ABAJO, DIR_DCHA, DIR_IZQ_ABAJO, DIR_IZQ]

FIND_DIR_ARRIBA = [LIST_DIR_ARRIBA_1, LIST_DIR_ARRIBA_2, LIST_DIR_ARRIBA_3, LIST_DIR_ARRIBA_4, LIST_DIR_ARRIBA_5,
                   LIST_DIR_ARRIBA_6, LIST_DIR_ARRIBA_7]

LIST_DIR_ABAJO_1 = [DIR_ABAJO]
LIST_DIR_ABAJO_2 = [DIR_DCHA_ABAJO, DIR_IZQ_ABAJO]
LIST_DIR_ABAJO_3 = [DIR_ABAJO, DIR_DCHA_ABAJO, DIR_IZQ_ABAJO]
LIST_DIR_ABAJO_4 = [DIR_ABAJO, DIR_DCHA_ABAJO, DIR_IZQ_ABAJO, DIR_DCHA]
LIST_DIR_ABAJO_5 = [DIR_ABAJO, DIR_DCHA_ABAJO, DIR_IZQ_ABAJO, DIR_DCHA, DIR_IZQ]
LIST_DIR_ABAJO_6 = [DIR_ABAJO, DIR_DCHA_ABAJO, DIR_IZQ_ABAJO, DIR_DCHA_ARRIBA, DIR_DCHA, DIR_IZQ]
LIST_DIR_ABAJO_7 = [DIR_ABAJO, DIR_DCHA_ABAJO, DIR_IZQ_ABAJO, DIR_DCHA_ARRIBA, DIR_DCHA, DIR_IZQ_ARRIBA, DIR_IZQ]

FIND_DIR_ABAJO = [LIST_DIR_ABAJO_1, LIST_DIR_ABAJO_2, LIST_DIR_ABAJO_3, LIST_DIR_ABAJO_4, LIST_DIR_ABAJO_5,
                  LIST_DIR_ABAJO_6, LIST_DIR_ABAJO_7]

LIST_DIR_DCHA_ARRIBA_1 = [DIR_DCHA]
LIST_DIR_DCHA_ARRIBA_2 = [DIR_DCHA, DIR_DCHA_ARRIBA]
LIST_DIR_DCHA_ARRIBA_3 = [DIR_DCHA, DIR_DCHA_ARRIBA, DIR_ARRIBA]
LIST_DIR_DCHA_ARRIBA_4 = [DIR_DCHA, DIR_DCHA_ARRIBA, DIR_ARRIBA, DIR_DCHA_ABAJO]
LIST_DIR_DCHA_ARRIBA_5 = [DIR_DCHA, DIR_DCHA_ARRIBA, DIR_ARRIBA, DIR_DCHA_ABAJO, DIR_ABAJO]
LIST_DIR_DCHA_ARRIBA_6 = [DIR_DCHA, DIR_DCHA_ARRIBA, DIR_ARRIBA, DIR_DCHA_ABAJO, DIR_ABAJO, DIR_IZQ_ABAJO]
LIST_DIR_DCHA_ARRIBA_7 = [DIR_DCHA, DIR_DCHA_ARRIBA, DIR_ARRIBA, DIR_DCHA_ABAJO, DIR_ABAJO, DIR_IZQ_ABAJO, DIR_IZQ]

FIND_DIR_DCHA_ARRIBA = [LIST_DIR_DCHA_ARRIBA_1, LIST_DIR_DCHA_ARRIBA_2, LIST_DIR_DCHA_ARRIBA_3, LIST_DIR_DCHA_ARRIBA_4,
                        LIST_DIR_DCHA_ARRIBA_5, LIST_DIR_DCHA_ARRIBA_6, LIST_DIR_DCHA_ARRIBA_7]

LIST_DIR_DCHA_ABAJO_1 = [DIR_DCHA]
LIST_DIR_DCHA_ABAJO_2 = [DIR_DCHA, DIR_DCHA_ABAJO]
LIST_DIR_DCHA_ABAJO_3 = [DIR_DCHA, DIR_DCHA_ABAJO, DIR_ABAJO]
LIST_DIR_DCHA_ABAJO_4 = [DIR_DCHA, DIR_DCHA_ABAJO, DIR_ABAJO, DIR_DCHA_ARRIBA]
LIST_DIR_DCHA_ABAJO_5 = [DIR_DCHA, DIR_DCHA_ABAJO, DIR_ABAJO, DIR_DCHA_ARRIBA, DIR_ARRIBA]
LIST_DIR_DCHA_ABAJO_6 = [DIR_DCHA, DIR_DCHA_ABAJO, DIR_ABAJO, DIR_DCHA_ARRIBA, DIR_ARRIBA, DIR_IZQ_ARRIBA]
LIST_DIR_DCHA_ABAJO_7 = [DIR_DCHA, DIR_DCHA_ABAJO, DIR_ABAJO, DIR_DCHA_ARRIBA, DIR_ARRIBA, DIR_IZQ_ARRIBA, DIR_IZQ]

FIND_DIR_DCHA_ABAJO = [LIST_DIR_DCHA_ABAJO_1, LIST_DIR_DCHA_ABAJO_2, LIST_DIR_DCHA_ABAJO_3, LIST_DIR_DCHA_ABAJO_4,
                       LIST_DIR_DCHA_ABAJO_5, LIST_DIR_DCHA_ABAJO_6, LIST_DIR_DCHA_ABAJO_7]

LIST_DIR_IZQ_ARRIBA_1 = [DIR_IZQ]
LIST_DIR_IZQ_ARRIBA_2 = [DIR_IZQ, DIR_IZQ_ARRIBA]
LIST_DIR_IZQ_ARRIBA_3 = [DIR_IZQ, DIR_IZQ_ARRIBA, DIR_ARRIBA]
LIST_DIR_IZQ_ARRIBA_4 = [DIR_IZQ, DIR_IZQ_ARRIBA, DIR_ARRIBA, DIR_IZQ_ABAJO]
LIST_DIR_IZQ_ARRIBA_5 = [DIR_IZQ, DIR_IZQ_ARRIBA, DIR_ARRIBA, DIR_IZQ_ABAJO, DIR_ABAJO]
LIST_DIR_IZQ_ARRIBA_6 = [DIR_IZQ, DIR_IZQ_ARRIBA, DIR_ARRIBA, DIR_IZQ_ABAJO, DIR_ABAJO, DIR_DCHA_ABAJO]
LIST_DIR_IZQ_ARRIBA_7 = [DIR_IZQ, DIR_IZQ_ARRIBA, DIR_ARRIBA, DIR_IZQ_ABAJO, DIR_ABAJO, DIR_DCHA_ABAJO, DIR_DCHA]

FIND_DIR_IZQ_ARRIBA = [LIST_DIR_IZQ_ARRIBA_1, LIST_DIR_IZQ_ARRIBA_2, LIST_DIR_IZQ_ARRIBA_3, LIST_DIR_IZQ_ARRIBA_4,
                       LIST_DIR_IZQ_ARRIBA_5, LIST_DIR_IZQ_ARRIBA_6, LIST_DIR_IZQ_ARRIBA_7]

LIST_DIR_IZQ_ABAJO_1 = [DIR_IZQ]
LIST_DIR_IZQ_ABAJO_2 = [DIR_IZQ, DIR_IZQ_ABAJO]
LIST_DIR_IZQ_ABAJO_3 = [DIR_IZQ, DIR_IZQ_ABAJO, DIR_ABAJO]
LIST_DIR_IZQ_ABAJO_4 = [DIR_IZQ, DIR_IZQ_ABAJO, DIR_ABAJO, DIR_IZQ_ARRIBA]
LIST_DIR_IZQ_ABAJO_5 = [DIR_IZQ, DIR_IZQ_ABAJO, DIR_ABAJO, DIR_IZQ_ARRIBA, DIR_ARRIBA]
LIST_DIR_IZQ_ABAJO_6 = [DIR_IZQ, DIR_IZQ_ABAJO, DIR_ABAJO, DIR_IZQ_ARRIBA, DIR_ARRIBA, DIR_DCHA_ARRIBA]
LIST_DIR_IZQ_ABAJO_7 = [DIR_IZQ, DIR_IZQ_ABAJO, DIR_ABAJO, DIR_IZQ_ARRIBA, DIR_ARRIBA, DIR_DCHA_ARRIBA, DIR_DCHA]

FIND_DIR_IZQ_ABAJO = [LIST_DIR_IZQ_ABAJO_1, LIST_DIR_IZQ_ABAJO_2, LIST_DIR_IZQ_ABAJO_3, LIST_DIR_IZQ_ABAJO_4,
                      LIST_DIR_IZQ_ABAJO_5, LIST_DIR_IZQ_ABAJO_6, LIST_DIR_IZQ_ABAJO_7]


DICT_DIR_BY_ORIGEN = \
    {
        CENTRO: FIND_DIR_CENTRO,
        DIR_DCHA: FIND_DIR_DCHA,
        DIR_DCHA_ABAJO: FIND_DIR_DCHA_ABAJO,
        DIR_DCHA_ARRIBA: FIND_DIR_DCHA_ARRIBA,
        DIR_ABAJO: FIND_DIR_ABAJO,
        DIR_ARRIBA: FIND_DIR_ARRIBA,
        DIR_IZQ: FIND_DIR_IZQ,
        DIR_IZQ_ARRIBA: FIND_DIR_IZQ_ARRIBA,
        DIR_IZQ_ABAJO: FIND_DIR_IZQ_ABAJO
    }