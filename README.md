# Calculadora de Redes

### Creado por: Omar Díaz Buzo

Este repositorio contiene dos aplicaciones con interfaz gráfica para cálculos de redes, VLSM y otras operaciones de subred. 

Con referencia al repositorio de [KatzeeDev](https://github.com/KatzeeDev/Calculadora-VLSM/blob/main/vlsm.py) para calcular VLSM.

## Aplicaciones

### Network_app.py

`Network_app.py` es una aplicación con interfaz gráfica para calcular:

- Máscara
- Wild Card
- Dirección de Red
- Dirección de Broadcast
- Rango de Hosts
- Número de Hosts Direccionables
- Número de Subredes
- Host específico por índice
- Subred específica por índice
- Host de subred específica por índice

### VLSM_app.py

`VLSM_app.py` es una aplicación con interfaz gráfica para calcular:

- Hosts Direccionables por Subred
- Dirección de Subred
- CIDR de Subred
- Máscara de Subred
- Rango IP de Subred
- Dirección de Broadcast de Subred

## Pasos para Ejecutar

1. **Descargar y descomprimir el repositorio.**

2. **Para la calculadora de VLSM:**
    - Abrir el archivo `VLSM_app.py` dentro de la carpeta y ejecutar el código.

3. **Para la calculadora de Redes:**
    - Abrir el archivo `Network_app.py` dentro de la carpeta y ejecutar el código.

## Requisitos

Asegúrate de tener instalados los siguientes paquetes antes de ejecutar las aplicaciones:

- `tkinter`
- `ipaddress`
- `math`
- `textwrap`

## Ejecución

Puedes ejecutar las aplicaciones utilizando Python 3.x. 
Ejemplo de cómo hacerlo desde la línea de comandos:
```bash
python VLSM_app.py
python Network_app.py
