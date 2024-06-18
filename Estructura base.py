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
taxi.tarifa_parado
uber = VTC(20, 30)
uber.tarifa_parado