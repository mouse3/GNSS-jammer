import threading
import numpy as np
import hackrf
import time
import matplotlib.pyplot as plt

class Main:
    def __init__(self):
        self.FRECUENCIAS = {
            "GPS": {"L1": 1575.42e6, "L2": 1227.60e6, "L5": 1176.45e6},
            "GLONASS": {"L1": 1602e6, "L2": 1246e6},
            "BeiDou": {"B1": 1561.098e6, "B2": 1207.140e6, "B3": 1268.52e6},
            "Galileo": {"E1": 1575.42e6, "E5a": 1176.45e6, "E5b": 1207.14e6, "E6": 1278.75e6},
        }

    def menu(self):
        while True:
            print("\nSeleccione una opción:")
            print("1: Ver espectrograma de señal")
            print("2: Salir")
            try:
                entrada = int(input("Seleccione una opción: "))

                if entrada == 1:
                    frecuencia = float(input("Ingrese la frecuencia (en Hz): "))
                    duracion = float(input("Ingrese la duración (en segundos): "))
                    tasa_muestreo = float(input("Ingrese la tasa de muestreo (en Hz): "))
                    self.plot_spectrogram(frecuencia, duracion, tasa_muestreo)
                elif entrada == 2:
                    print("Saliendo del programa.")
                    break
                else:
                    print("Opción inválida. Intente nuevamente.")
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número.")
            except Exception as e:
                print(f"Error inesperado: {e}")

    def plot_spectrogram(self, frecuencia: float, duracion: float, tasa_muestreo: float):
        """
        Función para mostrar el espectrograma de una señal senoidal en la frecuencia dada.
        """
        try:
            # Validar los parámetros de entrada
            if frecuencia <= 0 or duracion <= 0 or tasa_muestreo <= 0:
                raise ValueError("Frecuencia, duración y tasa de muestreo deben ser mayores que cero.")

            # Crear un vector de tiempo para la duración de la transmisión
            tiempo = np.arange(0, duracion, 1 / tasa_muestreo)

            # Generar la onda senoidal
            onda_senoidal = np.sin(2 * np.pi * frecuencia * tiempo)

            # Graficar el espectrograma
            plt.figure(figsize=(10, 6))
            plt.specgram(onda_senoidal, NFFT=1024, Fs=tasa_muestreo, noverlap=512, scale='dB')
            plt.title(f"Espectrograma de la señal a {frecuencia / 1e6} MHz")
            plt.xlabel('Tiempo [s]')
            plt.ylabel('Frecuencia [Hz]')
            plt.colorbar(label='Intensidad [dB]')
            plt.show()

        except Exception as e:
            print(f"Error al generar el espectrograma: {e}")

    def transmitir_senal(self, frecuencia: float, duracion: float = 0.5, tasa_muestreo: float = 10e6, ganancia: int = 20):
        """
        Función que transmite una señal senoidal en una frecuencia determinada.
        """
        try:
            # Validar los parámetros
            if frecuencia <= 0 or duracion <= 0 or tasa_muestreo <= 0 or ganancia < 0:
                raise ValueError("Parámetros de entrada no válidos.")

            # Establecer la conexión con HackRF
            dev = hackrf.HackRF()
            dev.setup()
            dev.set_freq(frecuencia)
            dev.set_sample_rate(tasa_muestreo)
            dev.set_lna_gain(16)
            dev.set_vga_gain(ganancia)

            # Crear un vector de tiempo para la duración de la transmisión
            tiempo = np.arange(0, duracion, 1 / tasa_muestreo)

            # Generar una onda senoidal con la frecuencia deseada
            onda_senoidal = np.sin(2 * np.pi * frecuencia * tiempo)

            # Convertir la señal a formato compatible con HackRF
            onda_final = np.int8(onda_senoidal * 127 + 128)  # Escalar para que esté en el rango [0, 255]

            # Transmitir la señal
            dev.start_tx(onda_final)

            print(f"Transmisión de la frecuencia {frecuencia} Hz finalizada.")

        except KeyboardInterrupt:
            print("Control+C detectado, deteniendo transmisión.")
        except Exception as e:
            print(f"Error durante la transmisión: {e}")
        finally:
            # Asegurar la liberación de recursos
            try:
                dev.stop_tx()
                dev.close()
            except:
                pass

# Crear una instancia de la clase
if __name__ == "__main__":
    objeto = Main()
    objeto.menu()
