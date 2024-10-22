# API Flask - Adopción de Perros

API Rest construida con Python y Flask para gestionar un catálogo de perros disponibles para adopción. El proyecto utiliza MongoDB para almacer la información de los perros y un sistemas de cache en Redis para optimizar consultas frecuentes.
El proyecto implementa contenedores en Docker para la ejecución del API, la base de datos de Mongo, y la cache de Redis. Además, hace uso de un volúmen para la persistencia de datos y una red para que los contenedores se comuniquen entre si.

## Características
- Operaciones CRUD (Create, Read, Update, Delete) para crear, leer, actualizar, y borrar datos de perros.
- Filtrar, buscar y ordenar perros por diversos atributos.
- Integración con MongoDb para almacenamiento de Datos
- Implementación de contenedores para la ejecución de los componenetes del proyecto
- Volúmenes en Docker para persistencia de Datos
- Sistema de cache con Redis para la optimización de consultas frecuentes

## Requisitos previos
- Python 3.x
- Pip (instalador de paquetes de python)
- Docker

## Estructura del proyecto

```bash
.
controllers
  dog_controller.py
errors
  error_handlers.py
infrastructure
  mongo.py
  swagger.py
models
  dog_model.py
services
  dog_service.py
static
  swagger.json
app.py
config.py
docker-compose.yml
Dockerfile
requirements.txt
README.md

```

## Instalación y ejecución

### 1. Clona el repositorio en la carpeta deseada

```bash
git clone https://github

cd

```
### 2. Crea y activa un entorno virtual en tu IDE

**Windows**

```bash

python -m venv venv

source venv/Scripts/activate

```

**Mac y Linux**

```bash
python -m venv venv

source venv/bin/activate
````

### 3. Ejecuta el archivo docker-compose.yml

```bash
docker-compose up --build -d
````

### 4. Ingresa a Swagger para probar los Endpoints

La API estará disponible en http://localhost:5000/swagger

## USO

- GET /dogs = Obtener todos los perros
- GET /dogs/{id} = Obtener perro por ID
- GET /dogs/search = Obtener perros por filtros
- POST /dogs = Crear un nuevo perro
- PUT /dogs/{id} = Actualizar información completa de un perro
- PATCH  /dogs/{id} = Actualizar campos específicos por ID
- PATCH /dogs/{id}/adopted = Cambiar estado de un perro a adoptado
- DELETE /dogs/{id} = Borrar un perro por ID
