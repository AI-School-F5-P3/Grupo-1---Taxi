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


def calculador():
    #LogIn()
    conductor = input("Indica 'Taxista' o 'VTC'")
    if conductor.lower() == 'taxista':
        noche = input('¿Es de noche?(si/no)')
        if noche.lower() == 'si':
            tasa = input('Indica el procentaje extra de tarifa nocturna')
            mov = taxista(True, int(tasa))
        else:
            mov = taxista(False)
    else:
        desc_mov = input("Indica la tasa de descuento en movimiento")
        desc_par = input("Indica la tasa de descuento en parado")
        mov = VTC(int(desc_mov), int(desc_par))
    
