import unittest
from taxi import Taxi

class TestTaxi(unittest.TestCase):

    def test_iniciar_carrera(self):
        taxi = Taxi()
        taxi.iniciar_carrera()
        self.assertIsNotNone(taxi.tiempo_inicio)
        self.assertEqual(taxi.estado_actual, 'parado')

    def test_cambiar_estado(self):
        taxi = Taxi()
        taxi.iniciar_carrera()
        taxi.cambiar_estado('movimiento')
        self.assertEqual(taxi.estado_actual, 'movimiento')
        taxi.cambiar_estado('parado')
        self.assertEqual(taxi.estado_actual, 'parado')

    def test_finalizar_carrera(self):
        taxi = Taxi()
        taxi.iniciar_carrera()
        taxi.cambiar_estado('movimiento')
        taxi.cambiar_estado('parado')
        costo_total = taxi.finalizar_carrera()
        self.assertGreaterEqual(costo_total, 0)

if __name__ == '__main__':
    unittest.main()
