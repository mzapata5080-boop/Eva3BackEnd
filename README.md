# TCG League Master

TCG League Master es una plataforma web pensada para organizar torneos de juegos de cartas coleccionables de forma simple y ordenada.

La aplicación permite publicar torneos, administrar sus cupos y facilitar la pre-inscripción de jugadores. Está construida con **Django 6** y puede adaptarse a distintas comunidades y franquicias, como *Magic: The Gathering*, *Pokémon TCG*, *Yu-Gi-Oh!*, *Dragon Ball Super*, entre otras.

## ¿Qué se puede hacer en la plataforma?

- Explorar torneos disponibles y filtrarlos según tus intereses.
- Consultar información de cada torneo, sus cupos y la franquicia a la que pertenece.
- Reservar un cupo mediante una bolsa de pre-inscripción.
- Revisar el resumen de la reserva y el comprobante correspondiente.
- Crear una cuenta y administrar tu perfil de jugador.
- Gestionar franquicias y torneos desde el área administrativa.
- Consultar información general de la liga y su reglamento oficial.

La idea es que tanto los organizadores como los jugadores tengan un punto de encuentro claro: los primeros pueden mantener la oferta de torneos actualizada y los segundos pueden encontrar y reservar su próximo evento sin complicaciones.

## Puesta en marcha

### 1. Activar el entorno virtual

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar las dependencias

Desde la carpeta raíz del proyecto, ejecuta:

```bash
pip install -r tcg_league_master/requirements.txt
```

### 3. Preparar la base de datos

Ingresa a la carpeta que contiene el proyecto Django y ejecuta las migraciones:

```bash
cd tcg_league_master
python manage.py makemigrations
python manage.py migrate
```

### 4. Cargar datos de ejemplo

Este comando crea usuarios, franquicias y torneos iniciales para que puedas probar la aplicación rápidamente:

```bash
python manage.py poblar_datos
```

### 5. Iniciar el servidor

```bash
python manage.py runserver
```

Luego abre [http://127.0.0.1:8000/](http://127.0.0.1:8000/) en tu navegador.

## Cuentas de prueba

Al cargar los datos iniciales quedan disponibles las siguientes cuentas:

| Tipo de usuario | Usuario | Contraseña | Qué puede hacer |
| :--- | :--- | :--- | :--- |
| **Organizador / Superusuario** | `admin` | `admin` | Administrar torneos, gestionar el catálogo y acceder al panel de Django. |
| **Jugador** | `jugador1` | `jugador123` | Explorar torneos, pre-inscribirse y consultar su perfil y comprobante de cupo. |

Estas credenciales son solo para desarrollo y pruebas. No deben utilizarse tal cual en un entorno de producción.

## Cómo está organizado el proyecto

La aplicación se divide en módulos pequeños, cada uno con una responsabilidad concreta:

- **`apps/core`** concentra la página principal, los contadores generales de la liga y el reglamento oficial.
- **`apps/catalogo`** administra las franquicias y los torneos, incluyendo filtros, búsqueda, ordenamiento y las herramientas para el equipo organizador.
- **`apps/pedidos`** gestiona la bolsa de pre-inscripción, calcula el recargo de servicio del 5 % y confirma los cupos reservados.
- **`apps/usuarios`** se encarga del registro, el inicio de sesión y el perfil de cada jugador.

## Tecnologías principales

- Python
- Django 6
- SQLite para el entorno de desarrollo
- HTML, CSS y plantillas de Django

## Próximos pasos

Una vez que el proyecto esté funcionando, puedes iniciar sesión con una de las cuentas de prueba, recorrer el catálogo y crear una pre-inscripción como jugador. Si necesitas administrar el contenido, utiliza la cuenta de organizador para acceder al panel administrativo.
