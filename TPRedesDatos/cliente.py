import requests
import webbrowser

print("=== CONFIGURACIÓN DE CONEXIÓN ===")
ip_ingresada = input("Ingrese la IP del servidor (Presione Enter para probar en la misma PC): ").strip()
IP_SERVIDOR = ip_ingresada if ip_ingresada else "127.0.0.1"
URL = f"http://{IP_SERVIDOR}:8000"
print(f"Conectando a {URL}...\n")

USUARIO = ""
PASSWORD = ""


def login():

    usuario_correcto = "alumno"
    password_correcta = "2026"

    intentos = 3

    while intentos > 0:

        usuario = input("Usuario: ")
        password = input("Contraseña: ")

        if usuario == usuario_correcto and password == password_correcta:

            global USUARIO, PASSWORD
            USUARIO = usuario
            PASSWORD = password

            print("\n✓ Acceso concedido")
            return True

        intentos -= 1
        print(f"\n✗ Credenciales incorrectas. Intentos restantes: {intentos}")

    print("\nDemasiados intentos fallidos. Cerrando programa...")
    return False


def pedir_entero(mensaje):
    """Pide un valor entero y vuelve a preguntar si se ingresa texto por error."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("[Error] Por favor, ingrese solo números enteros.")


def manejar_respuesta(r):
    """Maneja los distintos códigos de estado HTTP que puede devolver el servidor."""
    if r.status_code == 429:
        print("\n[Alerta] Estás haciendo consultas muy rápido. Esperá 1 segundo.")
        return None
    elif r.status_code != 200:
        detalle = "Error desconocido"
        try:
            detalle = r.json().get('detail', 'Error desconocido')
        except:
            pass
        print(f"\n[Error HTTP {r.status_code}] {detalle}")
        return None
    return r.json()


def hacer_peticion(metodo, endpoint, **kwargs):
    """Función central para manejar todas las peticiones y atajar errores de red."""
    try:
        if metodo == 'GET':
            r = requests.get(f"{URL}{endpoint}", **kwargs)
        elif metodo == 'POST':
            r = requests.post(f"{URL}{endpoint}", **kwargs)
        elif metodo == 'PUT':
            r = requests.put(f"{URL}{endpoint}", **kwargs)
        elif metodo == 'DELETE':
            r = requests.delete(f"{URL}{endpoint}", **kwargs)
        else:
            return None
        return manejar_respuesta(r)
    
    except requests.exceptions.ConnectionError:
        print("\n[Error] No se pudo conectar con el servidor. Verifique que esté encendido (uvicorn).")
        return None
    except Exception as e:
        print(f"\n[Error Inesperado] {e}")
        return None


def mostrar_libros(datos):

    if datos is None:
        return

    if isinstance(datos, dict):
        if "error" in datos:
            print("\n" + datos["error"])
            return
        datos = [datos]

    if not datos:
        print("\nNo se encontraron libros.")
        return

    for i, libro in enumerate(datos, start=1):
        print("\n" + "=" * 50)
        print(f"LIBRO {i}")
        print("=" * 50)
        print(f"Título     : {libro.get('title', '')}")
        print(f"Autor      : {libro.get('author', '')}")
        print(f"País       : {libro.get('country', '')}")
        print(f"Idioma     : {libro.get('language', '')}")
        print(f"Páginas    : {libro.get('pages', '')}")
        print(f"Año        : {libro.get('year', '')}")
        print(f"Imagen     : {libro.get('imageLink', '')}")
        print(f"Link       : {libro.get('link', '')}")
        print("=" * 50)


def obtener_libros():
    datos = hacer_peticion('GET', "/libros")
    mostrar_libros(datos)


def buscar_autor():
    autor = input("Ingrese autor: ")
    datos = hacer_peticion('GET', f"/autor/{autor}")
    mostrar_libros(datos)


def buscar_titulo():
    titulo = input("Ingrese titulo: ")
    datos = hacer_peticion('GET', f"/titulo/{titulo}")
    mostrar_libros(datos)


def buscar_pais():
    pais = input("Ingrese pais: ")
    datos = hacer_peticion('GET', f"/pais/{pais}")
    mostrar_libros(datos)


def agregar_libro():
    libro = {
        "author": input("Autor: "),
        "country": input("Pais: "),
        "imageLink": input("Imagen (ruta): "),
        "language": input("Idioma: "),
        "link": input("Link: "),
        "pages": pedir_entero("Paginas: "),
        "title": input("Titulo: "),
        "year": pedir_entero("Año: ")
    }

    datos = hacer_peticion('POST', "/libros", json=libro, auth=(USUARIO, PASSWORD))
    if datos:
        print(f"\nRespuesta del servidor: {datos}")


def modificar_libro():
    titulo = input("Titulo del libro a modificar: ")

    # Primero verificamos si el libro existe en el servidor
    verificacion = hacer_peticion('GET', f"/titulo/{titulo}")
    if verificacion is None:
        return
    if "error" in verificacion:
        print(f"\n[Error] No se encontró ningún libro con el título '{titulo}'.")
        return

    print("\nLibro encontrado. Ingrese los nuevos datos:")
    libro = {
        "author": input("Nuevo autor: "),
        "country": input("Nuevo pais: "),
        "imageLink": input("Nueva imagen: "),
        "language": input("Nuevo idioma: "),
        "link": input("Nuevo link: "),
        "pages": pedir_entero("Nuevas paginas: "),
        "title": titulo,
        "year": pedir_entero("Nuevo año: ")
    }

    datos = hacer_peticion('PUT', f"/libros/{titulo}", json=libro, auth=(USUARIO, PASSWORD))
    if datos:
        print(f"\nRespuesta del servidor: {datos}")


def eliminar_libro():
    titulo = input("Titulo a eliminar: ")
    
    datos = hacer_peticion('DELETE', f"/libros/{titulo}", auth=(USUARIO, PASSWORD))
    if datos:
        print(f"\nRespuesta del servidor: {datos}")


def abrir_api():
    webbrowser.open(f"{URL}/docs")
    print("Abriendo documentación de la API...")


def mostrar_menu():
    while True:
        print("\n===== MENU LIBROS API =====")
        print("1. Ver todos los libros")
        print("2. Buscar por autor")
        print("3. Buscar por titulo")
        print("4. Buscar por pais")
        print("5. Agregar libro")
        print("6. Modificar libro")
        print("7. Eliminar libro")
        print("8. Abrir documentación API")
        print("0. Salir")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            obtener_libros()
        elif opcion == "2":
            buscar_autor()
        elif opcion == "3":
            buscar_titulo()
        elif opcion == "4":
            buscar_pais()
        elif opcion == "5":
            agregar_libro()
        elif opcion == "6":
            modificar_libro()
        elif opcion == "7":
            eliminar_libro()
        elif opcion == "8":
            abrir_api()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida")


if __name__ == "__main__":
    if login():
        mostrar_menu()