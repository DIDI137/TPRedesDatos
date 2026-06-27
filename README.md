# TP Redes de Datos - API de Libros

Este proyecto es un Trabajo Práctico para la materia de Redes de Datos. Consiste en una API RESTful desarrollada con FastAPI que gestiona un catálogo de libros (`books.json`) y un cliente de consola para interactuar con ella.

## Características Principales

*   **API REST:** Construida con FastAPI.
*   **Accesible en Red Local:** El servidor se levanta en `0.0.0.0`, permitiendo que otras computadoras en la misma red Wi-Fi/LAN puedan conectarse (usando tu dirección IP).
*   **Autenticación:** Las rutas para modificar, agregar y eliminar libros están protegidas mediante HTTP Basic Auth.
*   **Rate Limiting:** El servidor incluye una protección para evitar múltiples peticiones rápidas desde una misma IP (límite de 1 petición por segundo).
*   **Cliente de Consola:** Un script interactivo (`cliente.py`) que maneja errores de red y permite consumir la API de manera sencilla.

## Requisitos Previos

*   Tener **Python 3.8+** instalado.
*   Tener instaladas las dependencias del proyecto.

## Instalación

1.  Clonar el repositorio o descargar los archivos.
2.  Abrir una terminal en la carpeta del proyecto (`TPRedesDatos`).
3.  Instalar las dependencias usando el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Cómo ejecutar el Servidor (API)

Para iniciar el servidor, abre una terminal en la carpeta del proyecto y ejecuta:

```bash
python libros.py
```

*Nota: Al ejecutarse, el servidor usará `uvicorn` para quedar escuchando en el puerto `8000` de tu red local (`0.0.0.0`).*

Puedes acceder a la documentación interactiva (Swagger UI) abriendo tu navegador en:
`http://localhost:8000/docs` (o reemplazando `localhost` por la IP local de la computadora servidor).

## Cómo ejecutar el Cliente

Para usar el menú interactivo que se conecta con la API, abre *otra* terminal y ejecuta:

```bash
python cliente.py
```

Si el servidor se está ejecutando en otra computadora de la red, deberás modificar la variable `URL` dentro de `cliente.py` con la IP correspondiente (por ejemplo: `URL = "http://192.168.1.5:8000"`).

## Credenciales de Acceso

Para usar las opciones de **Agregar, Modificar o Eliminar**, la API requiere credenciales (ya están configuradas por defecto en el cliente):

*   **Usuario:** `alumno`
*   **Contraseña:** `2026`

## Endpoints Disponibles

**Públicos:**
*   `GET /libros` - Devuelve todos los libros.
*   `GET /autor/{nombre}` - Busca libros por autor.
*   `GET /titulo/{titulo}` - Busca un libro específico.
*   `GET /pais/{pais}` - Busca libros por país.

**Protegidos (Requieren Auth):**
*   `POST /libros` - Agrega un nuevo libro.
*   `PUT /libros/{titulo}` - Modifica un libro existente.
*   `DELETE /libros/{titulo}` - Elimina un libro.
