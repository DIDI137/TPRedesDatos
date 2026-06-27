from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import json
import secrets
import time

app = FastAPI()

# =========================
# ARCHIVO JSON
# =========================
# Aqui es donde se abre y carga el archivo books.json
def cargar_libros():
    with open("books.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)

# =========================
# RATE LIMITING
# =========================
# Evita que una misma IP haga muchas solicitudes seguidas en poco tiempo.

ultima_solicitud = {} # Guarda la ultima solicitud de cada IP
LIMITE_SEGUNDOS = 1   # tiempo minimo entre requests

@app.middleware("http")
def limitar_requests(request: Request, call_next):

    # Excluir docs
    if request.url.path in ["/docs", "/openapi.json", "/redoc"]:
        return call_next(request)

    ip = request.client.host
    ahora = time.time()

    if ip in ultima_solicitud:
        diferencia = ahora - ultima_solicitud[ip]

        if diferencia < LIMITE_SEGUNDOS:
            raise HTTPException(
                status_code=429,
                detail="Demasiadas solicitudes. Intente mas tarde."
            )

    ultima_solicitud[ip] = ahora
    return call_next(request)

# =========================
# AUTENTICACIÓN BASIC
# =========================

security = HTTPBasic()

USUARIO = "alumno"
PASSWORD = "2026"

def verificar_credenciales(credentials: HTTPBasicCredentials = Depends(security)):

    usuario_correcto = secrets.compare_digest(credentials.username, USUARIO)
    password_correcta = secrets.compare_digest(credentials.password, PASSWORD)

    if not (usuario_correcto and password_correcta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )

# =========================
# MODELO
# =========================
# Da estructura y validacion de los datos cuando se tiene que agregar o modificar un libro
class Libro(BaseModel):
    author: str
    country: str
    imageLink: str
    language: str
    link: str
    pages: int
    title: str
    year: int

# =========================
#  GET
# =========================
# Se obtienen todos los libros de books.json
@app.get("/libros")
def obtener_libros():
    return cargar_libros()

# Se obtiene todos los libros de un autor 
@app.get("/autor/{nombre}")
def buscar_por_autor(nombre: str):
    libros = cargar_libros()

    resultado = []
    for libro in libros:
        if libro["author"].lower() == nombre.lower():
            resultado.append(libro)
    if resultado:
        return resultado
    else: 
        return {"error": "No encontrado"}

# Se obtiene un libro por el titulo
@app.get("/titulo/{titulo}")
def buscar_por_titulo(titulo: str):
    libros = cargar_libros()

    for libro in libros:
        if libro["title"].lower() == titulo.lower():
            return libro

    return {"error": "No encontrado"}

# Se obtiene u conjuntos de libros por pais
@app.get("/pais/{pais}")
def buscar_por_pais(pais: str):
    libros = cargar_libros()

    resultado = []
    for libro in libros:
        if libro["country"].lower() == pais.lower():
            resultado.append(libro)
    if resultado:
        return resultado
    else:
        return {"error": "No encontrado"}

# =========================
# POST (PROTEGIDO)
# =========================

@app.post("/libros")
def agregar_libro(libro: Libro, credentials: HTTPBasicCredentials = Depends(verificar_credenciales)):
    libros = cargar_libros()

    libros.append(libro.model_dump())

    with open("books.json", "w", encoding="utf-8") as archivo:
        json.dump(libros, archivo, indent=2)

    return {"message": "Libro agregado"}

# =========================
#  PUT (PROTEGIDO)
# =========================

@app.put("/libros/{titulo}")
def modificar_libro(titulo: str, datos: Libro, credentials: HTTPBasicCredentials = Depends(verificar_credenciales)):

    libros = cargar_libros()

    for i, libro in enumerate(libros):
        if libro["title"].lower() == titulo.lower():
            libros[i] = datos.model_dump()

            with open("books.json", "w", encoding="utf-8") as archivo:
                json.dump(libros, archivo, indent=2)

            return {
                "message": "Libro actualizado",
                "libro": libros[i]
            }

    return {"error": "No encontrado"}
# =========================
# DELETE 
# =========================

@app.delete("/libros/{titulo}")
def eliminar_libro(titulo: str, credentials: HTTPBasicCredentials = Depends(verificar_credenciales)):

    libros = cargar_libros()

    nuevos_libros = []

    for libro in libros:
        if libro["title"].lower() != titulo.lower():
            nuevos_libros.append(libro)

    if len(nuevos_libros) == len(libros):
        return {"error": "No encontrado"}

    with open("books.json", "w", encoding="utf-8") as archivo:
        json.dump(nuevos_libros, archivo, indent=2)

    return {"message": "Libro eliminado"}

if __name__ == "__main__":
    import uvicorn
    print("Iniciando servidor para toda la red local...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
