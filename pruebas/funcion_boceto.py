from numpy import random, linspace, repeat, pad, cos, pi, array_split
from matplotlib.pyplot import imread, imshow, show, pause, clf, axis
from folium import Map, Marker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from os import path


# Variables para definir el rango geográfico
lon_min = -10.0 # Longitud mínima   EJE X
lon_max = 30.0  # Longitud máxima   EJE X
lat_min = 50.0  # Latitud mínima    EJE Y
lat_max = 70.0   # Latitud máxima   EJE Y


# Parámetros
frecuencia_portadora = 1e3
fs = 10e3
duracion = 0.01
longitud_mensaje = 32
max_puntos = 1
coordenadas = []

# Configurar Selenium para capturar imágenes
chrome_options = Options()
chrome_options.add_argument("--headless")
#chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)



# Paso 1: Generación de un mensaje binario con alta entropía
def generar_mensaje_binario(longitud=32):
    # Usamos np.random.randint para obtener una secuencia binaria más aleatoria
    return random.randint(0, 2, size=longitud)

# Paso 2: Modulación BPSK
def modular_bpsk(mensaje, frecuencia_portadora, fs, duracion):
    t = linspace(0, duracion, int(fs * duracion), endpoint=False)
    mensaje_expandido = repeat(mensaje, len(t) // len(mensaje))
    mensaje_expandido = pad(mensaje_expandido, (0, len(t) - len(mensaje_expandido)), mode='constant')
    portadora = cos(2 * pi * frecuencia_portadora * t)
    senal_modulada = (mensaje_expandido * 2 - 1) * portadora
    return t, senal_modulada

# Paso 3: Demodulación BPSK
def demodular_bpsk(senal_modulada, frecuencia_portadora, fs, duracion, longitud_mensaje):
    t = linspace(0, duracion, int(fs * duracion), endpoint=False)
    portadora = cos(2 * pi * frecuencia_portadora * t)
    senal_demodulada = senal_modulada * portadora
    senal_integrada = array_split(senal_demodulada, longitud_mensaje)
    mensaje_recuperado = [1 if sum(segmento) > 0 else 0 for segmento in senal_integrada]
    return mensaje_recuperado

# Paso 4: Decodificación en coordenadas GPS dentro del rango definido
def decodificar_coordenadas(mensaje_binario, lat_min, lat_max, lon_min, lon_max):
    # 16 bits para latitud y 16 bits para longitud
    lat_bin = mensaje_binario[:16]
    lon_bin = mensaje_binario[16:]
    
    # Convertir el binario a un número entero
    lat_int = int(''.join(map(str, lat_bin)), 2)
    lon_int = int(''.join(map(str, lon_bin)), 2)
    
    # Normalizar la latitud y longitud para que estén dentro de los límites
    latitud = (lat_int / 65535) * (lat_max - lat_min) + lat_min
    longitud = (lon_int / 65535) * (lon_max - lon_min) + lon_min
    
    return latitud, longitud





# Bucle principal
contador = 0
while True:
    mensaje = generar_mensaje_binario(longitud_mensaje)
    t, senal_modulada = modular_bpsk(mensaje, frecuencia_portadora, fs, duracion)
    mensaje_recuperado = demodular_bpsk(senal_modulada, frecuencia_portadora, fs, duracion, longitud_mensaje)
    
    # Decodificar las coordenadas dentro del rango
    latitud, longitud = decodificar_coordenadas(mensaje_recuperado, lat_min, lat_max, lon_min, lon_max)

    # Mostrar las coordenadas para verificar
    print(f"Coordenadas decodificadas: Latitud = {latitud:.6f}, Longitud = {longitud:.6f}")
    coordenadas.append((latitud, longitud))

    if len(coordenadas) > max_puntos:
        coordenadas.pop(0)

    contador += 1
    if contador % 10 == 0:
        # Crear el mapa con la coordenada actual
        mapa = Map(location=[(lat_min + lat_max) / 2, (lon_min + lon_max) / 2], zoom_start=4)
        
        for coord in coordenadas:
            Marker(location=coord).add_to(mapa)
        
        mapa.save("mapa_gps.html")

        # Capturar imagen del mapa
        driver.get("file://" + path.abspath("mapa_gps.html"))
        driver.save_screenshot("mapa_gps.png")

        # Mostrar la imagen del mapa usando matplotlib
        img = imread("mapa_gps.png")
        imshow(img)
        axis('off')
        show(block=False)
        pause(duracion)
        clf()