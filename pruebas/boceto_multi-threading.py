import threading

class main:
    def __init__(self):
        self.FRECUENCIAS = {
            "GPS": {"L1": 1575.42e6,
                    "L2": 1227.60e6, 
                    "L5": 1176.45e6},
            "GLONASS": {"L1": 1602e6, 
                        "L2": 1246e6, 
                        "L3": 1246e6},
            "BeiDou": {"B1": 1561.098e6, 
                        "B2": 1207.140e6, 
                        "B3": 1268.52e6},
            "Galileo": {"E1": 1575.42e6, 
                        "E5a": 1176.45e6, 
                        "E5b": 1207.14e6, 
                        "E6": 1278.75e6},
        }
        self.valor1 = "Señal GPS activa"
        self.valor2 = "Señal GLONASS activa"
        self.valor3 = "Señal Galileo activa"

    def GPSjammer(self):
        while True:
            print(self.valor1)

    def GLONASSjammer(self):
        
        while True:
            print(self.valor2)
    
    def Galileojammer(self):
        while True:
            print(self.valor3)

# Crear una instancia de la clase
objeto = main()

# Crear hilos para ejecutar los métodos simultáneamente
hilo1 = threading.Thread(target=objeto.GPS)
hilo2 = threading.Thread(target=objeto.GLONASS)
hilo3 = threading.Thread(target=objeto.Galileo)

# Iniciar los hilos
hilo1.start()
hilo2.start()
hilo3.start()

# Esperar a que los hilos terminen (opcional, pero en este caso no terminarán debido a los bucles infinitos)
hilo1.join()
hilo2.join()
hilo3.join()
