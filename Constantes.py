import os

class Configuracion:

    __slots__ = ()
    NOMBRE_AP = 'Rompecabezas numérico'
    VERSION = 1.0
    CREDITOS = 'César Medina'

    # Estrategias de resolución planteadas:
    ESTRATEGIA_SECUENCIAL = 'Secuencial' # se resuelve de forma secuencial.
    ESTRATEGIA_MARCOS = 'Marcos'   # TODO se resolveía por marcos concéntricos
    ESTRATEGIA_CAMINOS = 'Caminos' # TODO se resolvería por todos los caminos posibles y dejéndolos morir o matando al resto cuando uno de ellos cumpla el objetivo.

    # Nombre del archivo fuente, (rompecabezas a resolver, descomentar el objetivo):
    #NOMBRE_FUENTE = 'f_4x4_20230129_141823.txt'  # solución en  < 1 s.
    #NOMBRE_FUENTE = 'f_5x5_20230226_212228.txt'  # solución en  < 1 s.
    #NOMBRE_FUENTE = 'f_8x8_20230130_002523.txt'  # solución en  < 1 s.
    NOMBRE_FUENTE = 'f_8x8_20230129_200306.txt'  # solución en  < 1 s.
    #NOMBRE_FUENTE = 'f_9x9_20230307_225530.txt'  # sol < 30 min
   

    # Tipo de estrategia de resolución elegida:
    # ESTRATEGIA = ESTRATEGIA_MARCOS
    # ESTRATEGIA = ESTRATEGIA_CAMINOS
    ESTRATEGIA = ESTRATEGIA_SECUENCIAL

    # Los recursos están en la carpeta rec
    RECURSOS = 'rec'+os.path.sep
    FUENTE = RECURSOS+NOMBRE_FUENTE  # ruta del Archivo fuente

    # Máximo de intentos permitido, si es 0 es infinito
    MAX_INTENTOS_PERMITIDO = 1000000000000000000000000

    CALCULAR_MEJOR_ESQUINA = True
    ESQUINA = 0  # Esquina por la que comienza, solo tiene efecto si CALCULAR_MEJOR_ESQUINA es falso

    COMENTARIOS = False  # Muestra el proceso, retarda mucho.

    # Permite ver el progreso cada x intentos aun con comentarios a Falso 
    PROGRESO_CADA_INTENTOS = 2000000
    
    # TODO: Ordena las posibilidades en la matriz de posbilidades priorizando las piezas más sencillas de colocar, a falso de momento.
    ORDENAR_POSIBILIDADES = False
