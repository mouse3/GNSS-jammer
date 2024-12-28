## Correcciones y Mejoras Técnicas
### Gestión de Excepciones:

- Se manejan excepciones en todo el código para evitar cierres abruptos.
- Se captura KeyboardInterrupt para detener la transmisión de forma segura.
### Gestión de Recursos:

- Se asegura que los dispositivos HackRF se cierren correctamente en el bloque finally.
### Validación de Entradas:

- Validación en el menú para manejar entradas no numéricas o fuera de rango.
### Multihilo Seguro:

- El método All utiliza hilos correctamente y espera su finalización con join().
