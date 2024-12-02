class Main():
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
        self.printmenu = """
                        1-> GPS:
                                L1:  1575.42 MHz  +- 1Hz
                                L2:  1227.60 MHz  +- 1Hz
                                L5:  1176.45 MHz  +- 1Hz
                        2-> GLONASS:
                                L1:  1602 MHz +- 1MHz
                                L2:  1246 MHz +- 1MHz
                                L3:  1246 MHz +- 1MHz
                        3-> BeiDou:
                                B1:  1561.098 MHz +- 1Hz
                                B2:  1207.140 MHz +- 1Hz
                                B3:  1268.52 MHz  +- 1Hz
                        4-> Galileo:
                                E1:  1575.42 MHz  +- 1Hz
                                E5a: 1176.45 MHz  +- 1Hz
                                E5b: 1207.14 MHz  +- 1Hz
                                E6:  1278.75 MHz  +- 1Hz
                        5-> All
                        
                        """
        self.hola = "hola"
        self.adios = "adios"
    def All(self):

    def example_function(self):
        while True:
            try:
                for i in [100, 200, 300]:  # Corrected the iteration
                    print(i)
            except :
                print("Control+C detectado, saliendo del programa.")
                break
        self.menu()

Main().example_function()
