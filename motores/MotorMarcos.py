from Constantes import Configuracion as conf
from PuzzleManager import PuzzleManager


class MotorMarcos(PuzzleManager):

    def __init__(self):
        super().__init__()
        self._tipoEstrategia = conf.ESTRATEGIA_MARCOS

    def resolver(self):
        if conf.COMENTARIOS:
            self.dibujarTapiz()
        self.resolverConMarcos()
        return None

    def resolverMarco(self, nMarco, intentos):
        # TODO
        pass

    def esPosibleColocarPieza(self, pieza, x, y, nMarco=0):
        # TODO:
        pass

    def getFormasDondeEncajar(self, x, y, nMarco=0):
        # TODO
        pass

    def inicializarFormasNone(self):
        return None, None, None, None

    def resolverConMarcos(self):
        # TODO
        pass

    def calcularNumeroMarcos(self):
        num = self.dimensiones[0]//2
        if (self.dimensiones[0]//2 != 0):
            num = num+1
        return num

    def colocarEsquinaInterior(self, nMarco):
        print('Se trata de colocar esquina interior', nMarco, nMarco, nMarco)
        posibilidades = self._calcularPosibilidadesPosicion(
            nMarco, nMarco, nMarco)
        nPieza = posibilidades.pop()
        while not self.esPosibleColocarPieza(self.getPieza(nPieza), nMarco, nMarco, nMarco):
            nPieza = posibilidades.pop()

        self.setPosibilidades(nMarco, nMarco, posibilidades)
        self.tapiz[nMarco][nMarco] = nPieza
        nPiezaIzda = self.tapiz[nMarco][nMarco-1]
        nPiezaArriba = self.tapiz[nMarco-1][nMarco]
        izda = self.getFormaPieza(nPiezaIzda, 2)
        arriba = self.getFormaPieza(nPiezaArriba, 3)
        # se rota para que quede 0 [0,0,dcha,abajo]
        self.rotarPieza(nPieza, izda, arriba, None, None)

        self.establecerPosibilidades(nMarco, nMarco, nMarco)

    def esEsquinaInteriorSuperiorDcha(self, x, y, nMarco):
        tope = self.getAltoTapiz()-1
        return x == nMarco and y == tope-nMarco

    def esEsquinaInteriorSuperiorIzda(self, x, y, nMarco):
        return x == nMarco and y == nMarco

    def esEsquinaInteriorInferiorDcha(self, x, y, nMarco):
        tope = self.getAltoTapiz()-1
        return x == tope-nMarco and y == tope-nMarco

    def esEsquinaInteriorInferiorIzda(self, x, y, nMarco):
        tope = self.getAltoTapiz()-1
        return x == tope-nMarco and y == nMarco

    def esMarcoInteriorSuperior(self, x, nMarco):
        return (x == nMarco)

    def esMarcoInteriorInferior(self, x, nMarco):
        tope = self.getAltoTapiz()-1
        return (x == tope-nMarco)

    def esMarcoInteriorIzquierdo(self, y, nMarco):
        return (y == nMarco)

    def esMarcoInteriorDerecho(self, y, nMarco):
        tope = self.getAltoTapiz()-1
        return (y == tope-nMarco)

    def getCoordenadasSiguientePieza(self, x, y, nMarco=0):
        pass

    def getCoordenadasAnteriorPieza(self, x, y, nMarco=0):
        pass

    def _calcularPosibilidadesPosicion(self, x, y, nMarco=0):
        pass

    # Obtiene las coordenadas de una pieza
    def obtenerCoordenadasPiezaMarco(self, nPieza, nMarco):
        res = False
        x = 0
        y = 0
        for ii, eleMarco in enumerate(self.obtenerMarco(nMarco)):
            if eleMarco[2] == nPieza:
                res = True
                x = eleMarco[0]
                y = eleMarco[1]
                break
        return res, x, y

    def obtenerMarco(self, nMarco):
        marco = []
        for x, fila in enumerate(self.tapiz):
            for y, nPieza in enumerate(fila):
                if (self.posicionEstaEnMarco(x, y, nMarco)):
                    marco.append([x, y, nPieza])

        return marco

    def posicionEstaEnMarco(self, x, y, nMarco):
        pertenece = False
        if (self.esMarcoInteriorDerecho(y, nMarco)
                or self.esMarcoInteriorInferior(x, nMarco)
                or self.esMarcoInteriorIzquierdo(y, nMarco)
                or self.esMarcoInteriorSuperior(x, nMarco)):
            pertenece = True

        return pertenece
    # Devuelve el número de marco dada una pocición.

    def getMarcoPosicion(self, x, y):
        for nMarco in range(self.calcularNumeroMarcos()):
            if self.posicionEstaEnMarco(x, y, nMarco):
                break
        return nMarco
