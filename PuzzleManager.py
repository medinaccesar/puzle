import collections
import timeit
from abc import ABCMeta, abstractmethod
from math import factorial

from Constantes import Configuracion as conf


class PuzzleManager(metaclass=ABCMeta):

    def __init__(self):
        self._tipoEstrategia = conf.ESTRATEGIA
        self.piezas = []
        self.repetidas = {}
        self.dimensiones = ()  # dimensiones del tapiz
        self.formas = {}  # diccionario de formas
        self.tapiz = []
        self.esquinas = []
        self.matrizPosiblidades = []
        self.matrizRotadasTresFormasIguales = []

        self.intentos = conf.MAX_INTENTOS_PERMITIDO

    @property
    def tipoEstrategia(self):
        return self._tipoEstrategia

    # @property
    # def intentos(self):
    #     return self._intentos

    # @intentos.setter
    # def intentos(self,intentos):
    #     self._intentos = intentos

    def leerFichero(self, rfichero):

        with open(rfichero, 'r') as fichero1:
            for index, linea in enumerate(fichero1.readlines()):
                if conf.COMENTARIOS:
                    print(index, '|', linea, end='')
                linea = linea.replace('\n', '')
                if (index > 0):
                    pieza = [int(x) for x in linea.split(' ')]
                    indexPiezaRepetida = self.getPiezaRepetida(pieza)
                    if indexPiezaRepetida:
                        if self.repetidas.get(indexPiezaRepetida):
                            self.repetidas[indexPiezaRepetida].append(index)
                        else:
                            self.repetidas[indexPiezaRepetida] = [index]
                    for forma in pieza:
                        if not self.formas.get(forma, False):
                            self.formas[forma] = [index]
                        else:
                            self.formas[forma].append(index)
                    self.piezas.append(pieza)

                else:
                    self.dimensiones = [int(x) for x in linea.split(' ')]
        self.crearTapiz()
        self.crearMatrizPosibilidades()
        self.crearMatrizRotadasTresFormasIguales()

    def escribirFichero():
        return True

    def getPiezaRepetida(self, piezaObjetivo):
        pRepetida = False
        for index, pieza in enumerate(self.piezas):
            if collections.Counter(pieza) == collections.Counter(piezaObjetivo):
                pRepetida = index + 1
                break
        return pRepetida

    def getPieza(self, nPieza):
        return self.piezas[nPieza-1]

    def getFormaPieza(self, nPieza, nLado):
        return self.piezas[nPieza-1][nLado]

    def getAnchoTapiz(self):
        return self.dimensiones[0]

    def getAltoTapiz(self):
        return self.dimensiones[1]

    def calcularEsquinas(self):
        self.esquinas = list(
            set([number for number in self.formas[0] if self.formas[0].count(number) > 1]))

    def crearTapiz(self):
        ancho = self.getAnchoTapiz()
        alto = self.getAltoTapiz()

        tapiz = []
        for j in range(0, ancho):
            casillas = []
            for i in range(0, alto):
                casillas.append(None)
            tapiz.append(casillas)

        self.tapiz = tapiz

    def crearMatrizPosibilidades(self):
        ancho = self.getAnchoTapiz()
        alto = self.getAltoTapiz()

        tapiz = []
        for j in range(0, ancho):
            casillas = []
            for i in range(0, alto):
                casillas.append([])
            tapiz.append(casillas)

        self.matrizPosiblidades = tapiz

    def crearMatrizRotadasTresFormasIguales(self):
        ancho = self.getAnchoTapiz()
        alto = self.getAltoTapiz()

        tapiz = []
        for j in range(0, ancho):
            casillas = []
            for i in range(0, alto):
                casillas.append([])
            tapiz.append(casillas)

        self.matrizRotadasTresFormasIguales = tapiz

    def esUltimaPieza(self, x, y, nMarco=0, estricto=True):
        ancho = self.getAnchoTapiz()
        alto = self.getAltoTapiz()
        if self._tipoEstrategia == conf.ESTRATEGIA_SECUENCIAL:
            return (x == ancho-1) and (y == alto-1)
        elif nMarco == 0 and self._tipoEstrategia == conf.ESTRATEGIA_MARCOS:
            # TODO: cambiar provisional marco ext
            return (x == nMarco + 1) and (y == nMarco)
        else:
            nPiezasTotales = ancho*alto
            nPiezasTapiz = 0
            for j in range(0, ancho):
                for i in range(0, alto):
                    if self.getNumPiezaTapiz(j, i) != None:
                        nPiezasTapiz += 1
            print(nPiezasTapiz, ' VS ', nPiezasTotales - 1)
            if not estricto:
                return nPiezasTapiz == nPiezasTotales - 1
            else:
                return nPiezasTapiz == nPiezasTotales

    def getPiezas(self):
        return self.piezas

    def getTapiz(self):
        return self.tapiz

    def getNumPiezaTapiz(self, x, y):
        return self.tapiz[x][y]

    def getFormas(self):
        return self.formas

    def getRepetidas(self):
        return self.repetidas

    def getEsquinas(self):
        return self.esquinas

    def colocarPieza(self, x, y, nPiezaPosible, nMarco=0):
        esUltimaPieza = self.esUltimaPieza(x, y, nMarco)
        esUltimaPiezaTablero = False
        if nMarco == 0:
            esUltimaPiezaTablero = esUltimaPieza
        esUltimaPiezaTablero = esUltimaPieza

        izda, encima, dcha, abajo = self.getFormasDondeEncajar(x, y, nMarco)
        nPieza = self.matrizPosiblidades[x][y].pop()

        if conf.COMENTARIOS:
            print('Colocando pieza', nPieza, 'en', x, y)

        self.rotarPieza(nPieza, izda, encima, dcha, abajo)
        self.tapiz[x][y] = nPieza

        if (not esUltimaPiezaTablero):
            self.establecerPosibilidades(x, y, nMarco)
        else:
            print()
            print('¡¡¡ÚLTIMA PIEZA COLOCADA!!!!')

        return esUltimaPiezaTablero

    def mostrarIntentos(self, intentos):
        if conf.MAX_INTENTOS_PERMITIDO == 0:
            totalIntentosPermitido = 'infinitos intentos'
        else:
            totalIntentosPermitido = self.intentos
        print('¡ÉXITO!', 'MÚM. INTENT.', intentos, 'de',
              totalIntentosPermitido, ' intentos permitidos.')
        print('Máx. intentos posibles por fuerza bruta:',
              factorial(self.dimensiones[0]*self.dimensiones[1]))
        return

    def esPosibleColocarPieza(self, pieza, x, y, nMarco=0):

        izda, encima, dcha, abajo = self.getFormasDondeEncajar(x, y, nMarco)
        esPosible = False
        posFin = len(pieza) - 1
        aux = pieza[3]

        if self.esMarcoInterior(x, y) and 0 in pieza:
            return False

        for ind, forma in enumerate(pieza):

            if (aux == izda and forma == encima):
                if (self.esMarcoDerecho(y)):

                    indice = ind+1
                    if indice > posFin:
                        indice = 0

                    if (pieza[indice] == dcha):  # dcha == 0

                        esPosible = True
                        break
                elif (self.esMarcoInferior(x)):

                    indice = ind+2
                    if indice > posFin:
                        indice = ind-2

                    if (pieza[indice] == abajo):  # abajo == 0

                        esPosible = True
                        break
                # Nota: no haría falta comprobar que abajo sea 0 en el marco inferior
                else:
                    esPosible = True
                    break
            aux = forma

        return esPosible

    def esPosibleColocarPosicionPiezaSiGira(self, pieza, x, y):

        izda, encima, dcha, abajo = self.getFormasDondeEncajar(x, y)
        nGiros = 1
        esPosible = False

        # giro o doble giro como las agujas de reloj o al contrario or (pieza[3] == izda and pieza[0]==encima)
        if ((pieza[1] == izda and pieza[2] == encima)):
            if self.esMarcoInferior(x):
                esPosible = pieza[0] == 0
            elif self.esMarcoDerecho(y):
                esPosible = pieza[3] == 0
            else:
                esPosible = True
        elif pieza[3] == izda and pieza[0] == encima:  # 0
            nGiros = 3
            if self.esMarcoInferior(x):
                esPosible = pieza[2] == 0  # 2
            elif self.esMarcoDerecho(y):
                esPosible = pieza[1] == 0
            else:
                esPosible = True
            # print(esPosible)

        return esPosible, nGiros

    def getFormasDondeEncajar(self, x, y, nMarco=0):
        if x == 0:
            encima = 0
        else:
            encima = self.piezas[self.tapiz[x-1][y]-1][3]
        if y == 0:
            izda = 0
        else:
            izda = self.piezas[self.tapiz[x][y-1]-1][2]
        dcha = None
        abajo = None
        if self.esMarcoInferior(x):
            abajo = 0
        if self.esMarcoDerecho(y):
            dcha = 0
        return izda, encima, dcha, abajo

    # Se coloca la esquina en el tapete y se establecen las posibilidades de todas las esquinas en la matrizDePosibilidades
    def colocarEsquina(self):
        # se elige la de conf., se puede mejorar eligiendo la que sus lados tengas menos posibles candidatos
        nEsquina = conf.ESQUINA
        if conf.CALCULAR_MEJOR_ESQUINA:
            nEsquina = self.calcularMejorEsquina()
            conf.ESQUINA = nEsquina

        print('Mejor esquina:', self.calcularMejorEsquina(),
              'Esquina usada', nEsquina)
        nPieza = self.esquinas[nEsquina]
        self.tapiz[0][0] = nPieza

        # se rota para que quede 0 [0,0,dcha,abajo]
        self.rotarPieza(nPieza, 0, 0, None, None)

        self.establecerPosibilidades(0, 0)

    def calcularMejorEsquina(self):
        nEsquina = 0
        posibilidadesAuxH = []
        posibilidadesAuxV = []
        for i in range(0, 4):
            nPieza = self.esquinas[i]
            self.rotarPieza(nPieza, 0, 0, None, None)
            posibilidades = self.getFormasPosibles(0)
            posibilidadesSinEsquinas = list(
                set(posibilidades) - set(self.esquinas))
            posibilidadesH = self.formas[self.getFormaPieza(nPieza, 2)]
            posibilidadesV = self.formas[self.getFormaPieza(nPieza, 3)]
            posibilidadesH = self.interseccion(
                posibilidadesSinEsquinas, posibilidadesH)
            posibilidadesV = self.interseccion(
                posibilidadesSinEsquinas, posibilidadesV)
            if i == 0:
                posibilidadesAuxH = posibilidadesH
                posibilidadesAuxV = posibilidadesV
            elif len(posibilidadesH) < len(posibilidadesAuxH):
                posibilidadesAuxH = posibilidadesH
                posibilidadesAuxV = posibilidadesV
                nEsquina = i
            elif len(posibilidadesH) == len(posibilidadesAuxH) and len(posibilidadesV) < len(posibilidadesAuxV):
                posibilidadesAuxH = posibilidadesH
                posibilidadesAuxV = posibilidadesV
                nEsquina = i

        return nEsquina
    # TODO: Ordenar las posibilidades
    def ordenarPosibilidades(self,x, y, posibilidades, nMarco):        
        pass
    
    # Establece posiblilidades en la matriz de posibilidades 
    def setPosibilidades(self, fila, columna, posibilidades):
        self.matrizPosiblidades[fila][columna] = posibilidades

    def setPosiblidadesEsquinas(self, nEsquina):
        # No hay posibilidades, ya está colocada la pieza
        self.setPosibilidades(0, 0, [])
        # Posibilidades para el resto de esquinas
        posibilidades = list(set(self.esquinas) -
                             set([self.esquinas[nEsquina]]))
        self.setPosibilidades(0, self.dimensiones[0]-1, posibilidades)
        self.setPosibilidades(self.dimensiones[0]-1, 0, posibilidades)
        self.setPosibilidades(
            self.dimensiones[0]-1, self.dimensiones[0]-1, posibilidades)

    # Rota la pieza en piezas[]
    def rotarPieza(self, nPieza, izda, arriba, dcha, abajo):
        nPieza = nPieza-1
        int = 0
        while not self.encajan(self.piezas[nPieza], izda, arriba, dcha, abajo):
            self.piezas[nPieza] = self.girarPieza(self.piezas[nPieza])
            int = int + 1
            if int == 6:
                # Si se produce: revisar la función esPosibleColocarPieza
                print('No debería llegar, exceso de rot.')
                exit()

        if conf.COMENTARIOS:
            print('Se ha rotado la pieza ', nPieza+1, ' ', self.piezas[nPieza])

    def encajan(self, pieza, izda, arriba, dcha, abajo):
        encaja = True
        if izda != None and pieza[0] != izda:
            encaja = False
        elif arriba != None and pieza[1] != arriba:
            encaja = False
        elif dcha != None and pieza[2] != dcha:
            encaja = False
        elif abajo != None and pieza[3] != abajo:
            encaja = False
        return encaja

    # Gira la pieza en sentido anti horario y la devuelve
    def girarPieza(self, pieza):
        piezaAux = pieza.pop(0)
        pieza.append(piezaAux)
        return pieza

    def rotarPiezaAnterior(self, x, y, nGiros):
        x, y = self.getCoordenadasAnteriorPieza(x, y)
        nPieza = self.tapiz[x][y]
        pieza = self.getPieza(nPieza)
        for i in range(0, nGiros):
            pieza = self.girarPieza(pieza)

        return x, y

    def resolverTiempos(self):
        tv1 = timeit.Timer(lambda: self.resolver()).timeit(1)
        if conf.COMENTARIOS:
            print('Tpo sol. ', self._tipoEstrategia, ':', tv1)
        self.convertirSegundos(tv1)

    @abstractmethod
    def resolver(self):
        pass

    @abstractmethod
    def quitarPiezaAnterior(self, x, y, nMarco=0):
        pass

    @abstractmethod
    def getCoordenadasSiguientePieza(self, x, y, nMarco=0):
        pass

    @abstractmethod
    def getCoordenadasAnteriorPieza(self, x, y, nMarco=0):
        pass

    @abstractmethod
    def _calcularPosibilidadesPosicion(self, x, y, nMarco=0):
        pass

    def tienePosiblesTresFormasIguales(self, x, y):
        res = False
        nGiros = 1
        x, y = self.getCoordenadasAnteriorPieza(x, y)
        nPieza = self.tapiz[x][y]
        pieza = self.getPieza(nPieza)
        if self.tieneTresFormasIgualesPieza(pieza) and nPieza not in self.matrizRotadasTresFormasIguales[x][y]:
            res, nGiros = self.esPosibleColocarPosicionPiezaSiGira(pieza, x, y)
            if res:
                self.matrizRotadasTresFormasIguales[x][y].append(nPieza)

        return res, nGiros

    def tieneTresFormasIgualesPieza(self, pieza):
        repes = 0
        for lado in pieza:
            num = pieza.count(lado)
            if num > repes:
                repes = num
        return repes == 3

    def establecerPosibilidades(self, x, y, nMarco=0):

        x, y = self.getCoordenadasSiguientePieza(x, y, nMarco)
        posibilidades = self._calcularPosibilidadesPosicion(x, y, nMarco)
        posibilidades = self.eliminarPosiblesPosibilidades(
            posibilidades,  x, y, nMarco)
        if conf.ORDENAR_POSIBILIDADES:
            posibilidades =  self.ordenarPosibilidades(x, y, posibilidades, nMarco)
        self.setPosibilidades(x, y, posibilidades)
        return posibilidades

    def getMatrizColocadas(self):
        colocadas = []
        ancho = self.getAnchoTapiz()
        alto = self.getAltoTapiz()

        for j in range(0, ancho):
            for i in range(0, alto):

                if (self.tapiz[j][i] != None):
                    colocadas.append(self.tapiz[j][i])

        return colocadas

    def esEsquinaSuperiorDcha(self, x, y):
        tope = self.getAltoTapiz()-1
        return x == 0 and y == tope

    def esEsquinaSuperiorIzda(self, x, y):
        return x == 0 and y == 0

    def esEsquinaInferiorDcha(self, x, y):
        tope = self.getAltoTapiz()-1
        return x == tope and y == tope

    def esEsquinaInferiorIzda(self, x, y):
        tope = self.getAltoTapiz()-1
        return x == tope and y == 0

    def esMarcoSuperior(self, x):
        return (x == 0)

    def esMarcoInferior(self, x):
        tope = self.getAltoTapiz()-1
        return (x == tope)

    def esMarcoIzquierdo(self, y):
        return (y == 0)

    def esMarcoDerecho(self, y):
        tope = self.getAltoTapiz()-1
        return (y == tope)

    def esMarcoExterior(self, x, y):
        return x == 0 or y == 0 or x == self.getAnchoTapiz()-1 or y == self.getAltoTapiz()-1

    def esMarcoInterior(self, x, y):
        return not self.esMarcoExterior(x, y)

    def getNumPiezaAnterior(self, x, y, nMarco=0):
        x, y = self.getCoordenadasAnteriorPieza(x, y, nMarco)
        return self.tapiz[x][y]

    # Elimina posibles posibilidades aunque la pieza tenga la forma si finalmente no puede encajarla
    def eliminarPosiblesPosibilidades(self, lista,  x, y, nMarco=0):
        posibilidades = []
        for nPieza in lista:
            if self.esPosibleColocarPieza(self.getPieza(nPieza), x, y, nMarco):
                posibilidades.append(nPieza)
        return posibilidades

    def interseccion(self, lst1, lst2):
        return list(set(lst1) & set(lst2))

    def noInterseccion(self, lst1, lst2):
        for i in list(lst2):
            if i in lst1:
                lst1.remove(i)

        return lst1

    def elegirCamino(self):
        mejorCamino = []
        x = 0
        y = 0
        for fila in range(self.dimensiones[0]):
            for columna in range(self.dimensiones[1]):
                casilla = self.matrizPosiblidades[fila][columna]
                if None not in casilla and len(casilla) != 0 and (len(mejorCamino) == 0 or len(casilla) < len(mejorCamino)):
                    mejorCamino = casilla
                    x = fila
                    y = columna
        return (x, y)

    def getFormasPosibles(self, claveForma):
        formasMarco = []
        for forma in self.formas[claveForma]:
            if forma not in self.getEsquinas():
                formasMarco.append(forma)
        return formasMarco

    def dibujarTapiz(self, dibujarMatrizPosibilidades = True):
        ancho = self.getAnchoTapiz()
        alto = self.getAltoTapiz()
        print()
        for i in range(0, ancho):
            fila = ''
            for j in range(0, alto):
                elemento = self.tapiz[i][j]
                if elemento != None:
                    fila = fila + ' ' + str(f"{self.tapiz[i][j]:02d}")
                else:
                    fila = fila + ' ' + str(self.tapiz[i][j])
            print(fila)

        for i in range(0, ancho):
            fila = []
            for j in range(0, alto):
                nPieza = self.tapiz[i][j]
                if (nPieza == None):
                    fila.append([None])
                else:
                    formato = '{:02d}'.format
                    p = self.getPieza(nPieza)
                    # fila.append(list(map(formato,p)))
                    fila.append(p)

            print(fila)
        if dibujarMatrizPosibilidades:    
            self.dibujarMatrizPosibilidades()

    def dibujarMatrizPosibilidades(self):
        print('MP:')
        for pos in self.matrizPosiblidades:
            print(pos)

    def getMatrizPosibilidades(self):
        return self.matrizPosiblidades

    def convertirSegundos(self, seconds):
        days = seconds // (24 * 3600)
        seconds %= (24 * 3600)
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        print("Total: ", days, ' días, ', hours, ' horas, ',
              minutes, ' minutos y ', seconds, ' segundos.')

    def creditos(self):
        print()
        print(conf.NOMBRE_AP, 'Versión', conf.VERSION)
        print('Por', conf.CREDITOS)
        print()
