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

    OPUESTAS = {
        "arriba": "abajo",
        "abajo": "arriba",
        "izquierda": "derecha",
        "derecha": "izquierda",
    }

    def __init__(self):
        super().__init__(nombre="Mi Agente")
        self.visitas = {}
        self.ultima_accion = None

    def al_iniciar(self):
        """Se llama una vez al iniciar la simulacion. Opcional."""
        self.visitas = {}
        self.ultima_accion = None

    def decidir(self, percepcion):
        """
        Decide la siguiente accion del agente.

        Parametros:
            percepcion - diccionario con lo que el agente puede ver

        Retorna:
            'arriba', 'abajo', 'izquierda' o 'derecha'
        """
        posicion = percepcion["posicion"]
        self.visitas[posicion] = self.visitas.get(posicion, 0) + 1

        for direccion in self.ACCIONES:
            if percepcion[direccion] == "meta":
                self.ultima_accion = direccion
                return direccion

        vertical, horizontal = percepcion["direccion_meta"]
        preferidas = [
            direccion
            for direccion in (horizontal, vertical)
            if direccion in self.ACCIONES
        ]

        for direccion in preferidas:
            if percepcion[direccion] != "libre":
                continue

            destino = self._destino(posicion, direccion)
            if self.visitas.get(destino, 0) == 0:
                self.ultima_accion = direccion
                return direccion

        mejor_direccion = self._buscar_menos_visitada(posicion, percepcion, evitar_retroceso=True)
        if mejor_direccion is None:
            mejor_direccion = self._buscar_menos_visitada(posicion, percepcion, evitar_retroceso=False)

        if mejor_direccion is not None:
            self.ultima_accion = mejor_direccion
            return mejor_direccion

        for direccion in self.ACCIONES:
            if percepcion[direccion] == "libre":
                self.ultima_accion = direccion
                return direccion

        return "abajo"

    def _destino(self, posicion, direccion):
        delta_fila, delta_columna = self.DELTAS[direccion]
        fila, columna = posicion
        return fila + delta_fila, columna + delta_columna

    def _buscar_menos_visitada(self, posicion, percepcion, evitar_retroceso):
        mejor_direccion = None
        menor_visita = None

        for direccion in self.ACCIONES:
            if percepcion[direccion] != "libre":
                continue

            if evitar_retroceso and direccion == self.OPUESTAS.get(self.ultima_accion):
                continue

            destino = self._destino(posicion, direccion)
            visitas = self.visitas.get(destino, 0)

            if menor_visita is None or visitas < menor_visita:
                menor_visita = visitas
                mejor_direccion = direccion

        return mejor_direccion
