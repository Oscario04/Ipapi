# Ipapi

## Descripción general
Esta API permite trackear visitas de usuarios a través de una página web, almacenando información relevante como IP, ubicación, agente de usuario y ruta visitada. Los datos se almacenan en una base de datos MongoDB y también se suben a un bucket Wasabi S3 para respaldo.

### Flujo general
1. Un script JavaScript (`static/track_user.js`) obtiene la IP y datos geográficos del usuario usando el servicio externo ipapi.co.
2. El script envía estos datos al backend mediante una petición POST al endpoint `/track`.
3. El backend (FastAPI) recibe los datos, los almacena en MongoDB y los sube a Wasabi S3.
4. Se puede consultar la lista de usuarios trackeados mediante el endpoint `/all-users`.

## Endpoints principales

- `POST /track`
	- Recibe un JSON con los datos del usuario (IP, ciudad, región, país, timezone, organización, path, user_agent).
	- Almacena los datos en MongoDB y los sube a Wasabi S3 como respaldo.
	- Respuesta: `{ "message": "Usuario trackeado" }` o error.

- `GET /all-users`
	- Devuelve un listado de todos los usuarios trackeados en la base de datos.
	- Respuesta: lista de objetos usuario.

## Estructura de datos
El modelo de usuario (`UserVisit`) incluye:
- ip: str
- city: str (opcional)
- region: str (opcional)
- postal: str (opcional)
- country: str (opcional)
- timezone: str (opcional)
- org: str (opcional)
- path: str
- user_agent: str (opcional)

## Tecnologías utilizadas
- **FastAPI**: Framework principal del backend.
- **MongoDB**: Base de datos para almacenar los datos de tracking.
- **Wasabi S3**: Almacenamiento de respaldo de los datos en la nube.
- **Motor**: Cliente asíncrono para MongoDB.
- **boto3**: Cliente para Wasabi S3.
- **Pydantic**: Validación de modelos de datos.
- **JavaScript**: Script de tracking en el frontend.

## Archivos principales
- `app/main.py`: Lógica principal de la API y definición de endpoints.
- `app/models/user.py`: Modelo de datos del usuario.
- `app/db/mongodb.py`: Conexión a MongoDB.
- `app/wasabi.py`: Lógica para subir datos a Wasabi S3.
- `static/track_user.js`: Script que trackea y envía los datos al backend.

## Ejemplo de uso
1. El usuario visita una página que incluye el script de tracking.
2. El script obtiene los datos y los envía automáticamente al backend.
3. El backend almacena y respalda la información.
4. Se pueden consultar todos los registros vía `/all-users`.
