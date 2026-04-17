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

    ORDEN_PRIORIDAD = ["derecha", "abajo", "izquierda", "arriba"]

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

            if self.visitas.get(self._destino(posicion, direccion), 0) == 0:
                self.ultima_accion = direccion
                return direccion

        mejor_direccion = None
        mejor_puntaje = None

        for direccion in self.ACCIONES:
            if percepcion[direccion] != "libre":
                continue

            destino = self._destino(posicion, direccion)
            puntaje = self._puntaje_movimiento(destino, direccion, preferidas)

            if mejor_puntaje is None or puntaje < mejor_puntaje:
                mejor_puntaje = puntaje
                mejor_direccion = direccion

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

    def _puntaje_movimiento(self, destino, direccion, preferidas):
        visitas_destino = self.visitas.get(destino, 0)
        retroceso = direccion == self.OPUESTAS.get(self.ultima_accion)
        alineado_meta = direccion in preferidas
        prioridad = self.ORDEN_PRIORIDAD.index(direccion)

        return (
            0 if alineado_meta else 1,
            1 if retroceso else 0,
            visitas_destino,
            prioridad,
        )
