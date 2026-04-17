"""
mi_agente.py - Aqui defines tu agente.

Tu agente debe:
    1. Heredar de la clase Agente
    2. Implementar el metodo decidir(percepcion)
    3. Retornar: 'arriba', 'abajo', 'izquierda' o 'derecha'

Lo que recibes en 'percepcion':
percepcion = {
    'posicion':       (3, 5),
    'arriba':         'libre',
    'abajo':          'pared',
    'izquierda':      'libre',
    'derecha':        None,
    'direccion_meta': ('abajo', 'derecha'),
}
"""

from entorno import Agente


class MiAgente(Agente):
    """
    Tu agente de navegacion.

    Implementa el metodo decidir() para que el agente
    llegue del punto A al punto B en el grid.
    """

    def __init__(self):
        super().__init__(nombre="Mi Agente")
        # Puedes agregar atributos aqui si los necesitas.
        # Ejemplo:
        # self.pasos = 0
        # self.memoria = {}

    def al_iniciar(self):
        """Se llama una vez al iniciar la simulacion. Opcional."""
        pass

    def decidir(self, percepcion):
        """
        Decide la siguiente accion del agente.

        Parametros:
            percepcion - diccionario con lo que el agente puede ver

        Retorna:
            'arriba', 'abajo', 'izquierda' o 'derecha'
        """
        for direccion in self.ACCIONES:
            if percepcion[direccion] == "meta":
                return direccion

        vertical, horizontal = percepcion["direccion_meta"]

        for direccion in (horizontal, vertical):
            if direccion in self.ACCIONES and percepcion[direccion] == "libre":
                return direccion

        for direccion in self.ACCIONES:
            if percepcion[direccion] == "libre":
                return direccion

        return "abajo"
