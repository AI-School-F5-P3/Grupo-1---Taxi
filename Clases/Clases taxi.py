'''
Definimos una clase principal conductor donde incluimos como atributos las tarifas estándar para todos los vehiculos tipo taxi.
Después con herencias, establecemos dos clases, VTC (uber, cabify, etc.) que heredan las tarifas de conductor pero que permiten establecer atributos distintos.
En el caso de los VTC, como quieren competir con los taxis, establecen el descuento que consideren necesario a sus tarifas, tanto en parado como en movimiento, pasando como argumentos los porcentajes de descuento para cada uno de ellos. Por defecto no hacen descuento.
En el caso de los taxi, su tarifa es fija, sin embargo por la noche cobran plus de nocturnidad, por lo tanto, cada taxista puede ajustar cuanto quiere cobrar extra por la noche. Para ello el primer argumento define si está en horario nocturno mediante True o False, y de ser noche, establece el procenatje (que por defecto es 0) que se debe sumar a la tarifa total.
'''

class conductor:
    tarifa_parado = 0.02
    tarifa_movimiento = 0.05

class VTC(conductor):
    def __init__(self, descuento_p = 0, descuento_m = 0):
        self.tarifa_movimiento += self.tarifa_movimiento * (descuento_m/100)
        self.tarifa_parado += self.tarifa_parado * (descuento_p/100)
        self.tarifa_movimiento = round(self.tarifa_movimiento, 2)
        self.tarifa_parado = round(self.tarifa_parado, 2)

class taxista(conductor):
    def __init__(self, noche, prcnt = 0):
        if noche:
            self.tarifa_parado += self.tarifa_parado * (prcnt/100)
            self.tarifa_movimiento += self.tarifa_movimiento * (prcnt/100)
            self.tarifa_parado = round(self.tarifa_parado, 2)
            self.tarifa_movimiento = round(self.tarifa_movimiento, 2)


taxi = taxista(True, 20)
uber = VTC(20, 30)
