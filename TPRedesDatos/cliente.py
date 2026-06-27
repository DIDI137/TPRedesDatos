import requests
import webbrowser

URL = "http://127.0.0.1:8000"

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


def mostrar_libros(datos):

    if isinstance(datos, dict):

        if "error" in datos:
            print("\n", datos["error"])
            return

        datos = [datos]

    for i, libro in enumerate(datos, start=1):

        print("\n" + "=" * 50)
        print(f"LIBRO {i}")
        print("=" * 50)
        print(f"Título     : {libro['title']}")
        print(f"Autor      : {libro['author']}")
        print(f"País       : {libro['country']}")
        print(f"Idioma     : {libro['language']}")
        print(f"Páginas    : {libro['pages']}")
        print(f"Año        : {libro['year']}")
        print(f"Imagen     : {libro['imageLink']}")
        print(f"Link       : {libro['link']}")
        print("=" * 50)


def obtener_libros():
    r = requests.get(f"{URL}/libros")
    mostrar_libros(r.json())


def buscar_autor():
    autor = input("Ingrese autor: ")
    r = requests.get(f"{URL}/autor/{autor}")
    mostrar_libros(r.json())


def buscar_titulo():
    titulo = input("Ingrese titulo: ")
    r = requests.get(f"{URL}/titulo/{titulo}")
    mostrar_libros(r.json())


def agregar_libro():

    libro = {
        "author": input("Autor: "),
        "country": input("Pais: "),
        "imageLink": input("Imagen (ruta): "),
        "language": input("Idioma: "),
        "link": input("Link: "),
        "pages": int(input("Paginas: ")),
        "title": input("Titulo: "),
        "year": int(input("Año: "))
    }

    r = requests.post(f"{URL}/libros",json=libro,auth=(USUARIO, PASSWORD))
    print(r.json())


def modificar_libro():

    titulo = input("Titulo del libro a modificar: ")

    libro = {
        "author": input("Nuevo autor: "),
        "country": input("Nuevo pais: "),
        "imageLink": input("Nueva imagen: "),
        "language": input("Nuevo idioma: "),
        "link": input("Nuevo link: "),
        "pages": int(input("Nuevas paginas: ")),
        "title": titulo,
        "year": int(input("Nuevo año: "))
    }

    r = requests.put(f"{URL}/libros/{titulo}",json=libro,auth=(USUARIO, PASSWORD))

    print(r.json())


def eliminar_libro():

    titulo = input("Titulo a eliminar: ")

    r = requests.delete(f"{URL}/libros/{titulo}",auth=(USUARIO, PASSWORD))

    print(r.json())


def abrir_api():

    webbrowser.open(f"{URL}/docs")
    print("Abriendo documentación de la API...")


def mostrar_menu():

    while True:

        print("\n===== MENU LIBROS API =====")
        print("1. Ver todos los libros")
        print("2. Buscar por autor")
        print("3. Buscar por titulo")
        print("4. Agregar libro")
        print("5. Modificar libro")
        print("6. Eliminar libro")
        print("7. Abrir documentación API")
        print("0. Salir")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            obtener_libros()

        elif opcion == "2":
            buscar_autor()

        elif opcion == "3":
            buscar_titulo()

        elif opcion == "4":
            agregar_libro()

        elif opcion == "5":
            modificar_libro()

        elif opcion == "6":
            eliminar_libro()

        elif opcion == "7":
            abrir_api()

        elif opcion == "0":
            print("Saliendo...")
            break

        else:
            print("Opción inválida")


if __name__ == "__main__":

    if login():
        mostrar_menu()