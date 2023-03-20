from Constantes import Configuracion as conf
from PuzzleManager import PuzzleManager


class MotorSecuencial(PuzzleManager):

    def __init__(self):
        super().__init__()
        self._tipoEstrategia = conf.ESTRATEGIA_SECUENCIAL

    def resolver(self):

        piezaPosibleColocada = False
        if conf.COMENTARIOS:
            self.dibujarTapiz()

        ancho = self.getAnchoTapiz()
        y = 1  # La primera esquina ya está colocada
        x = 0
        intentos = 0
        representarProgreso = 0
        while True:
            intentos += 1
            representarProgreso += 1
            if conf.PROGRESO_CADA_INTENTOS == representarProgreso:
                print('Intento: ', intentos, 'Coord.', x, y)
                self.dibujarTapiz()
                representarProgreso = 0

            piezaPosibleColocada = False
            continuar = True

            while (continuar and not piezaPosibleColocada):  # si quedan posibilidades

                pos = len(self.matrizPosiblidades[x][y])-1
                if (pos < 0):
                    break

                nPiezaPosible = self.matrizPosiblidades[x][y][pos]
                if conf.COMENTARIOS:
                    print(intentos, '\n--\nSe intenta posible', nPiezaPosible)
                if self.esPosibleColocarPieza(self.getPieza(nPiezaPosible), x, y):
                    esUltima = self.colocarPieza(x, y, nPiezaPosible)
                    if conf.COMENTARIOS:
                        print('Se coloca posible', nPiezaPosible)
                    piezaPosibleColocada = True
                    continuar = False

                else:
                    if conf.COMENTARIOS:
                        print(intentos, 'Se quita posible', nPiezaPosible)
                    self.matrizPosiblidades[x][y].remove(nPiezaPosible)
                    if (len(self.matrizPosiblidades[x][y]) == 0 or (len(self.matrizPosiblidades[x][y]) == 1 and self.matrizPosiblidades[x][y][0] == None)):
                        self.setPosibilidades(x, y, [None])
                        continuar = False
            if (not piezaPosibleColocada):

                tienePosiblesTresFormasiguales, nGiros = self.tienePosiblesTresFormasIguales(
                    x, y)
                if tienePosiblesTresFormasiguales:                   
                    xAnt, yAnt = self.rotarPiezaAnterior(x, y, nGiros)                    
                    self.establecerPosibilidades(xAnt, yAnt)
                    if conf.COMENTARIOS:
                        print('Se rota la anterior pues tiene 3 formas iguales ', xAnt, yAnt)

                else:
                    if conf.COMENTARIOS:
                        print('Se quita la anterior de ', x, y)
                    x, y = self.quitarPiezaAnterior(x, y)

            else:
                # La pieza se ha colocado
                if esUltima:
                    print()  # Reto conseguido
                    self.mostrarIntentos(intentos)
                    return
                y += 1
                if y > ancho-1:
                    y = 0
                    x += 1

            # Se alcanza el límite de intentos permitidos para resolver el puzle, no se ha conseguirdo el reto en ese número de intentos
            if (intentos == self.intentos):
                print('=============== ')
                print(intentos, 'intento |x,y ', x, y)
                self.dibujarMatrizPosibilidades()
                break

     # Se llega desde una posición en el que la pieza no ha podido colocarse, entonces se quita la pieza anterior
    def quitarPiezaAnterior(self, x, y, nMarco=0):
        if conf.COMENTARIOS:
            print('parametros QPA:', x, y, nMarco)
        while True:

            xAnt, yAnt = x, y
            x, y = self.getCoordenadasAnteriorPieza(x, y, nMarco)
            self.tapiz[x][y] = None
            self.matrizRotadasTresFormasIguales[x][y] = []

            if (len(self.matrizPosiblidades[x][y]) > 0 and self.matrizPosiblidades[x][y][0] != None):
                break
            else:

                tienePosiblesTresFormasiguales, nGiros = self.tienePosiblesTresFormasIguales(
                    x, y)
                if tienePosiblesTresFormasiguales:
                    xAnt, yAnt = self.rotarPiezaAnterior(x, y, nGiros)
                    self.establecerPosibilidades(xAnt, yAnt, nMarco)
                    if conf.COMENTARIOS:
                        self.dibujarTapiz()
                    break

        return x, y

    # nMarco es para el motor de resolución por marcos
    def getCoordenadasSiguientePieza(self, x, y, nMarco=0):
        if (self.esMarcoDerecho(y)):
            x += 1
            y = 0
        else:
            y += 1
        return x, y

    def getCoordenadasAnteriorPieza(self, x, y, nMarco=0):
        if (self.esMarcoIzquierdo(y)):
            tope = self.getAltoTapiz()-1
            x -= 1
            y = tope
        else:
            y -= 1
        return x, y

    def _calcularPosibilidadesPosicion(self, x, y, nMarco=0):

        nLado = 2
        colocadas = self.getMatrizColocadas()
        if conf.COMENTARIOS:
            print('Se calculan las posibilidades para la posición', x, y)
        if (self.esEsquinaSuperiorDcha(x, y) or self.esEsquinaInferiorDcha(x, y)):
            #  Se toman las posibilidades previamente establecidas para la esquina
            posibilidades = list(set(self.esquinas) -
                                 set([self.esquinas[conf.ESQUINA]]))
            if (len(colocadas) > 0):
                posibilidades = list(set(posibilidades) - set(colocadas))
            nPiezaAnterior = self.tapiz[x][y-1]
            posibilidadesAnterior = self.formas[self.getFormaPieza(
                nPiezaAnterior, nLado)]
            posibilidades = self.interseccion(
                posibilidades, posibilidadesAnterior)

        elif (self.esEsquinaInferiorIzda(x, y)):

            #  Se toman las posibilidades previamente establecidas para la esquina
            posibilidades = list(set(self.esquinas) -
                                 set([self.esquinas[conf.ESQUINA]]))
            if (len(colocadas) > 0):
                posibilidades = list(set(posibilidades) - set(colocadas))
            nPiezaAnterior = self.tapiz[x-1][y]
            nLado = 3
            posibilidadesAnterior = self.formas[self.getFormaPieza(
                nPiezaAnterior, nLado)]
            posibilidades = self.interseccion(
                posibilidades, posibilidadesAnterior)
        # TODO: mejorar con otra intersección
        elif (self.esMarcoSuperior(x) or self.esMarcoInferior(x) or self.esMarcoDerecho(y)):

            posibilidades = self.getFormasPosibles(0)
            posibilidades = list(set(posibilidades) - set(self.esquinas))

            if (len(colocadas) > 0):
                posibilidades = list(set(posibilidades) - set(colocadas))
            nPiezaAnterior = self.tapiz[x][y-1]
            nLado = 2
            if conf.COMENTARIOS:
                print(nPiezaAnterior, x, y)
            if conf.COMENTARIOS:
                self.dibujarTapiz()
            posibilidadesAnterior = self.formas[self.getFormaPieza(
                nPiezaAnterior, nLado)]
            posibilidades = self.interseccion(
                posibilidades, posibilidadesAnterior)
        elif (self.esMarcoIzquierdo(y)):

            posibilidades = self.getFormasPosibles(0)
            posibilidades = list(set(posibilidades) - set(self.esquinas))

            if (len(colocadas) > 0):
                posibilidades = list(set(posibilidades) - set(colocadas))

            nPiezaAnterior = self.tapiz[x-1][y]
            nLado = 3
            posibilidadesAnterior = self.formas[self.getFormaPieza(
                nPiezaAnterior, nLado)]
            posibilidades = self.interseccion(
                posibilidades, posibilidadesAnterior)
        else:

            nPiezaArriba = self.tapiz[x-1][y]
            posibilidades = self.getFormasPosibles(
                self.getFormaPieza(nPiezaArriba, 3))

            if (len(colocadas) > 0):
                posibilidades = list(set(posibilidades) - set(colocadas))
            nPiezaAnterior = self.tapiz[x][y-1]
            nLado = 2
            posibilidadesAnterior = self.formas[self.getFormaPieza(
                nPiezaAnterior, nLado)]
            posibilidades = self.interseccion(
                posibilidades, posibilidadesAnterior)

        return posibilidades
