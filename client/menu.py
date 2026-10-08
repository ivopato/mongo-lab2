#!/usr/bin/env python3
"""
Menú simple de consola en Python para realizar peticiones REST.
Permite interactuar de forma interactiva y llamar a funciones para probar la API con MongoDB.
"""
import os
import sys
import requests

API_URL = os.getenv('API_URL', 'http://localhost:8001')


def verificar_salud():
    """Realiza una petición GET para comprobar el estado de la API."""
    url = f"{API_URL}/health"
    print(f"\n[INFO] Consultando estado en: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"Código de estado: {response.status_code}")
        print("Respuesta:", response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text)
    except requests.exceptions.RequestException as err:
        print(f"[ERROR] No se pudo conectar con el servidor: {err}")


def inicializar_bd():
    """Realiza una petición POST para inicializar la base de datos e índices."""
    url = f"{API_URL}/setup"
    print(f"\n[INFO] Solicitando setup en: {url}")
    try:
        response = requests.post(url, timeout=30)
        print(f"Código de estado: {response.status_code}")
        print("Respuesta:", response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text)
    except requests.exceptions.RequestException as err:
        print(f"[ERROR] Error al realizar la petición: {err}")


def consultar_registros():
    """Realiza una petición GET para consultar registros existentes."""
    url = f"{API_URL}/data"
    print(f"\n[INFO] Consultando datos en: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"Código de estado: {response.status_code}")
        print("Respuesta:", response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text)
    except requests.exceptions.RequestException as err:
        print(f"[ERROR] Error en petición REST: {err}")


def pedir_pelicula():
    """Pide los datos de una película y regresa un diccionario (solo campos con valor)."""
    nombre = input("Nombre: ").strip()
    director = input("Director: ").strip()
    genero = input("Género: ").strip()
    anio = input("Año: ").strip()

    pelicula = {
        "nombre": nombre,
        "director": director,
        "genero": genero,
        "anio": anio
    }
    # Enviar solo campos con valor
    return {k: v for k, v in pelicula.items() if v}


def insertar_registro():
    """Realiza una petición POST para insertar una película."""
    url = f"{API_URL}/data"
    print(f"\n[INFO] Insertar película en: {url}")
    payload = pedir_pelicula()
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"Código de estado: {response.status_code}")
        print("Respuesta:", response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text)
    except requests.exceptions.RequestException as err:
        print(f"[ERROR] Error en petición REST: {err}")


def insertar_varios():
    """Realiza una petición POST enviando una lista de películas."""
    url = f"{API_URL}/data"
    print(f"\n[INFO] Insertar varias películas en: {url}")
    cuantas = input("¿Cuántas películas quieres insertar? ").strip()
    if not cuantas.isdigit() or int(cuantas) == 0:
        print("[AVISO] Escribe un número mayor a 0.")
        return

    payload = []
    for i in range(int(cuantas)):
        print(f"\nPelícula {i + 1}:")
        payload.append(pedir_pelicula())
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"Código de estado: {response.status_code}")
        print("Respuesta:", response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text)
    except requests.exceptions.RequestException as err:
        print(f"[ERROR] Error en petición REST: {err}")


def consultar_por_campo(campo):
    """Realiza una petición GET filtrando por un campo (nombre, director o genero)."""
    valor = input(f"Valor de '{campo}' a buscar: ").strip()
    if not valor:
        print("[AVISO] El valor no puede estar vacío.")
        return
    url = f"{API_URL}/data"
    print(f"\n[INFO] Consultando películas en: {url}?{campo}={valor}")
    try:
        response = requests.get(url, params={campo: valor}, timeout=10)
        print(f"Código de estado: {response.status_code}")
        print("Respuesta:", response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text)
    except requests.exceptions.RequestException as err:
        print(f"[ERROR] Error en petición REST: {err}")


def actualizar_por_id():
    """Realiza una petición PUT para actualizar una película."""
    item_id = input("ID de la película a actualizar: ").strip()
    if not item_id:
        print("[AVISO] El ID no puede estar vacío.")
        return
    print("Escribe los nuevos datos (deja vacío lo que no quieras cambiar):")
    payload = pedir_pelicula()
    if not payload:
        print("[AVISO] No escribiste ningún dato para actualizar.")
        return
    url = f"{API_URL}/data/{item_id}"
    print(f"\n[INFO] Actualizando película en: {url}")
    try:
        response = requests.put(url, json=payload, timeout=10)
        print(f"Código de estado: {response.status_code}")
        print("Respuesta:", response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text)
    except requests.exceptions.RequestException as err:
        print(f"[ERROR] Error en petición REST: {err}")


def consultar_por_id():
    """Realiza una petición GET para consultar un registro específico."""
    item_id = input("ID del registro: ").strip()
    if not item_id:
        print("[AVISO] El ID no puede estar vacío.")
        return
    url = f"{API_URL}/data/{item_id}"
    print(f"\n[INFO] Consultando registro en: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"Código de estado: {response.status_code}")
        print("Respuesta:", response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text)
    except requests.exceptions.RequestException as err:
        print(f"[ERROR] Error en petición REST: {err}")


def eliminar_por_id():
    """Realiza una petición DELETE para eliminar un registro específico."""
    item_id = input("ID del registro a eliminar: ").strip()
    if not item_id:
        print("[AVISO] El ID no puede estar vacío.")
        return
    url = f"{API_URL}/data/{item_id}"
    print(f"\n[INFO] Eliminando registro en: {url}")
    try:
        response = requests.delete(url, timeout=10)
        print(f"Código de estado: {response.status_code}")
        print("Respuesta:", response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text)
    except requests.exceptions.RequestException as err:
        print(f"[ERROR] Error en petición REST: {err}")


def consultar_por_nombre():
    """Realiza una petición GET para consultar un registro por su nombre."""
    nombre = input("Nombre del registro a buscar: ").strip()
    if not nombre:
        print("[AVISO] El nombre no puede estar vacío.")
        return
    url = f"{API_URL}/data/name/{nombre}"
    print(f"\n[INFO] Consultando registro en: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"Código de estado: {response.status_code}")
        print("Respuesta:", response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text)
    except requests.exceptions.RequestException as err:
        print(f"[ERROR] Error en petición REST: {err}")


def mostrar_menu():
    """Despliega el menú de opciones en pantalla."""
    print("\n" + "=" * 45)
    print("        MENÚ PRINCIPAL - REST CLIENT")
    print("=" * 45)
    print(f" Servidor objetivo: {API_URL}")
    print("-" * 45)
    print(" 1. IGNORAR LAB 02 | Inicializar base de datos / índices (POST /setup)")
    print(" 2. Consultar todas las películas (GET /data)")
    print(" 3. Insertar una película (POST /data)")
    print(" 4. Consultar una película por ID (GET /data/{id})")
    print(" 5. Eliminar una película por ID (DELETE /data/{id})")
    print(" 6. Consultar películas por nombre (GET /data?nombre=)")
    print(" 7. Consultar películas por director (GET /data?director=)")
    print(" 8. Consultar películas por género (GET /data?genero=)")
    print(" 9. Insertar varias películas (POST /data con lista)")
    print("10. Actualizar una película por ID (PUT /data/{id})")
    print(" 0. Salir")
    print("=" * 45)


def main():
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción [0-10]: ").strip()

        if opcion == '1':
            inicializar_bd()
        elif opcion == '2':
            consultar_registros()
        elif opcion == '3':
            insertar_registro()
        elif opcion == '4':
            consultar_por_id()
        elif opcion == '5':
            eliminar_por_id()
        elif opcion == '6':
            consultar_por_campo('nombre')
        elif opcion == '7':
            consultar_por_campo('director')
        elif opcion == '8':
            consultar_por_campo('genero')
        elif opcion == '9':
            insertar_varios()
        elif opcion == '10':
            actualizar_por_id()
        elif opcion == '0':
            print("\nSaliendo del programa. ¡Hasta luego!")
            sys.exit(0)
        else:
            print("\n[AVISO] Opción no válida. Por favor, ingresa un número del 0 al 10.")


if __name__ == '__main__':
    main()
