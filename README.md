# TCG League Master - Plataforma de Gestión de Torneos TCG

Plataforma web desarrollada en **Django 6** para la administración, publicación y reserva de cupos en torneos oficiales de juegos de cartas coleccionables (*Magic: The Gathering*, *Pokémon TCG*, *Yu-Gi-Oh!*, *Dragon Ball Super*, entre otros).

---

## 🚀 Requisitos e Instalación

1. **Activar el entorno virtual**:
   ```bash
   # En Windows PowerShell:
   .\.venv\Scripts\Activate.ps1
   ```

2. **Instalar dependencias** (si no están instaladas):
   ```bash
   pip install -r tcg_league_master/requirements.txt
   ```

3. **Migraciones y Base de Datos**:
   ```bash
   cd tcg_league_master
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Poblar datos de prueba** (Crea usuarios, franquicias y torneos iniciales):
   ```bash
   python manage.py poblar_datos
   ```

5. **Iniciar el servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```
   Accede en tu navegador a: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 👤 Cuentas de Acceso Preconfiguradas

| Rol | Usuario | Contraseña | Permisos |
| :--- | :--- | :--- | :--- |
| **Organizador / Superusuario** | `admin` | `admin` | Acceso total al panel de control, gestión de torneos y Django Admin. |
| **Jugador Estándar** | `jugador1` | `jugador123` | Pre-inscripción de torneos, comprobante de cupo y perfil de jugador. |

---

## 🛠️ Estructura del Proyecto

* **`apps/core`**: Landing page institucional, contadores globales de liga y reglamento oficial.
* **`apps/catalogo`**: Modelos de franquicias y torneos TCG, catálogo con filtros, búsqueda, ordenamiento y CRUD backoffice para staff.
* **`apps/pedidos`**: Carro/bolsa de pre-inscripción en sesión, cálculo de recargo de servicio (5%) y liquidación de cupos.
* **`apps/usuarios`**: Registro de nuevos jugadores, autenticación y panel de perfil.
