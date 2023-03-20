import argparse
import sys

from Constantes import Configuracion as conf
from motores.MotorMarcos import MotorMarcos
from motores.MotorSecuencial import MotorSecuencial
from util.crear import Fabrica


class Puzzle():
    def __init__(self):

        if conf.ESTRATEGIA == conf.ESTRATEGIA_SECUENCIAL:
            self.pManager = MotorSecuencial()
        elif conf.ESTRATEGIA == conf.ESTRATEGIA_MARCOS:
            self.pManager = MotorMarcos()

    def cargarDatos(self):

        self.pManager.creditos()
        print('Archivo fuente:', conf.FUENTE, 'Estrategia:', conf.ESTRATEGIA)
        self.pManager.leerFichero(conf.FUENTE)
        self.pManager.calcularEsquinas()

        if conf.COMENTARIOS:
            self.resumen()

    def resumen(self):
        esquinas = self.pManager.getEsquinas()
        tapiz = self.pManager.getTapiz()
        formas = self.pManager.getFormas()
        print('Formas:', formas)
        print()
        print('Esquinas', esquinas)
        print('Piezas', self.pManager.getPiezas())
        print('Repetidas', self.pManager.getRepetidas())
        print('Tapiz', tapiz)

    def colocarEsquina(self):
        self.pManager.colocarEsquina()

    def mostrarAyuda(self):
        print('Ayuda:', 'por hacer...')

    def resolver(self):
        print()
        print('Déjame pensar...')
        self.pManager.resolverTiempos()

        self.pManager.dibujarTapiz(False)
        print('---------')
        # TODO: Mostrar las combinaciones de repetidas
        print('Repetidas', self.pManager.getRepetidas())

    # TODO: dividir el parser del main para dejarlo más legible
    def parseArgs(args=sys.argv[1:]):
        parser = argparse.ArgumentParser(
            description=conf.NOMBRE_AP+" "+str(conf.VERSION))
        subparsers = parser.add_subparsers(help='sub-command help')

        return parser.parse_args(args)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=conf.NOMBRE_AP+" "+str(conf.VERSION))
    parser.add_argument("-d", "--dimension", type=int,
                        help=" Se crean los ficheros fuente y solución  del tamaño que se le pase, por ejemplo:  python puzzle.p -d 10 ")
    parser.version = str(conf.VERSION)
    parser.add_argument('--version', action='version')

    parser.add_argument("-a", '--ayuda')
    args = parser.parse_args()
    if args.dimension:
        fabrica = Fabrica(args.dimension)
        print('Se crean los ficheros fuente y solución para un puzle de',
              args.dimension, 'x', args.dimension)
        fabrica.crearPuzle()
        fabrica.dibujarTapiz()
    elif args.ayuda:
        p = Puzzle()
        p.mostrarAyuda()
    else:

        p = Puzzle()
        p.cargarDatos()
        p.colocarEsquina()
        p.resolver()
