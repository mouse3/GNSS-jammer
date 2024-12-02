import threading
import numpy as np
import hackrf
import random
import time
import matplotlib.pyplot as plt

class Main:
    def __init__(self):
        self.FRECUENCIAS = {
            "GPS": {"L1": 1575.42e6, "L2": 1227.60e6, "L5": 1176.45e6},
            "GLONASS": {"L1": 1602e6, "L2": 1246e6, "L3": 1246e6},
            "BeiDou": {"B1": 1561.098e6, "B2": 1207.140e6, "B3": 1268.52e6},
            "Galileo": {"E1": 1575.42e6, "E5a": 1176.45e6, "E5b": 1207.14e6, "E6": 1278.75e6},
        }

    def menu(self):
        while True:
            print("\nSeleccione una opción:")
            print("1: GPS Jammer")
            print("2: GLONASS Jammer")
            print("3: BeiDou Jammer")
            print("4: Galileo Jammer")
            print("5: Emitir todas las señales")
            print("6: Ver espectrograma de señal")
            entrada = int(input("Seleccione una opción: "))

            if entrada == 1:
                self.GPSjammer()
            elif entrada == 2:
                self.GLONASSjammer()
            elif entrada == 3:
                self.BeiDoujammer()
            elif entrada == 4:
                self.Galileojammer()
            elif entrada == 5:
                self.All()
            elif entrada == 6:
                self.plot_spectrogram()
            else:
                print("Opción inválida. Intente nuevamente.")

    def plot_spectrogram(self, frecuencia: float = 1575.42e6, duracion: float = 0.5, tasa_muestreo: float = 10e6):
        """
        Función para mostrar el espectrograma de una señal senoidal en la frecuencia dada.
        """
        # Crear un vector de tiempo para la duración de la transmisión
        tiempo = np.arange(0, duracion, 1/tasa_muestreo)

        # Generar la onda senoidal
        onda_senoidal = np.sin(2 * np.pi * frecuencia * tiempo)

        # Modificar las amplitudes de la onda aleatoriamente
        amplitudes_aleatorias = [random.uniform(0.1, 1.0) for _ in range(len(onda_senoidal))]
        onda_modulada = onda_senoidal * amplitudes_aleatorias

        # Graficar el espectrograma
        plt.figure(figsize=(10, 6))
        plt.specgram(onda_modulada, NFFT=1024, Fs=tasa_muestreo, noverlap=512, scale='dB')
        plt.title(f"Espectrograma de la señal a {frecuencia / 1e6} MHz")
        plt.xlabel('Tiempo [s]')
        plt.ylabel('Frecuencia [Hz]')
        plt.colorbar(label='Intensidad [dB]')
        plt.show()

    def All(self):
        """
        Emitir señales en todas las frecuencias de GPS, GLONASS, BeiDou y Galileo simultáneamente.
        """
        # Crear hilos para transmitir las señales de cada sistema GNSS
        hilos = []

        # Emitir señales para todas las frecuencias de GPS
        hilo_gps = threading.Thread(target=self.transmitir_frecuencias, args=('GPS',))
        hilos.append(hilo_gps)

        # Emitir señales para todas las frecuencias de GLONASS
        hilo_glonass = threading.Thread(target=self.transmitir_frecuencias, args=('GLONASS',))
        hilos.append(hilo_glonass)

        # Emitir señales para todas las frecuencias de BeiDou
        hilo_beiDou = threading.Thread(target=self.transmitir_frecuencias, args=('BeiDou',))
        hilos.append(hilo_beiDou)

        # Emitir señales para todas las frecuencias de Galileo
        hilo_galileo = threading.Thread(target=self.transmitir_frecuencias, args=('Galileo',))
        hilos.append(hilo_galileo)

        # Iniciar los hilos
        for hilo in hilos:
            hilo.start()

        # Esperar a que todos los hilos terminen
        for hilo in hilos:
            hilo.join()

        print("Transmisión de todas las señales finalizada.")

    def transmitir_frecuencias(self, sistema: str):
        """
        Transmitir señales en las frecuencias de un sistema GNSS determinado.
        """
        for frecuencia in self.FRECUENCIAS[sistema].values():
            self.transmitir_senal(frecuencia)

    def transmitir_senal(self, frecuencia: float, duracion: float = 0.5, tasa_muestreo: float = 10e6, frecuencia_hackrf: float = 900000000, ganancia: int = 20):
        """
        Función que transmite una señal senoidal en una frecuencia determinada.
        """
        try:
            # Establecer la conexión con HackRF
            dev = hackrf.HackRF()
            dev.setup()
            dev.set_freq(frecuencia_hackrf)
            dev.set_sample_rate(tasa_muestreo)
            dev.set_lna_gain(16)
            dev.set_vga_gain(ganancia)

            # Crear un vector de tiempo para la duración de la transmisión
            tiempo = np.arange(0, duracion, 1/tasa_muestreo)

            # Generar una onda senoidal con la frecuencia deseada
            onda_senoidal = np.sin(2 * np.pi * frecuencia * tiempo)

            # Modificar las amplitudes de la onda aleatoriamente
            amplitudes_aleatorias = [random.uniform(0.1, 1.0) for _ in range(len(onda_senoidal))]
            onda_modulada = onda_senoidal * amplitudes_aleatorias

            # Convertir la señal a formato compatible con HackRF
            onda_final = np.int8(onda_modulada * 127 + 128)  # Escalar para que esté en el rango [0, 255]

            # Transmitir la señal
            dev.start_tx(onda_final)

            print(f"Transmisión de la frecuencia {frecuencia} finalizada.")
        except KeyboardInterrupt:
            print("Control+C detectado, deteniendo transmisión.")
            # Detener la transmisión y liberar el dispositivo
            dev.stop_tx()
            dev.close()

    def GPSjammer(self):
        for frecuencia in self.FRECUENCIAS['GPS'].values():
            self.transmitir_senal(frecuencia)

    def GLONASSjammer(self):
        for frecuencia in self.FRECUENCIAS['GLONASS'].values():
            self.transmitir_senal(frecuencia)

    def BeiDoujammer(self):
        for frecuencia in self.FRECUENCIAS['BeiDou'].values():
            self.transmitir_senal(frecuencia)

    def Galileojammer(self):
        for frecuencia in self.FRECUENCIAS['Galileo'].values():
            self.transmitir_senal(frecuencia)


# Crear una instancia de la clase
objeto = Main()

# Crear hilos para ejecutar el menú y las transmisiones simultáneamente
hilo_menu = threading.Thread(target=objeto.menu)

# Iniciar el hilo del menú
hilo_menu.start()

# Esperar a que el hilo termine (esto es opcional en este caso)
hilo_menu.join()
