# Portal de Selección de Proveedor - Arquitectura y Gobierno de Datos

Este proyecto es una aplicación web desarrollada en Streamlit para la evaluación y selección de proveedores cloud, con autenticación de usuarios, cuestionario de evaluación, panel de administración y visualización de resultados.

## Estructura del Proyecto

- `main.py`: Lógica principal de autenticación y enrutamiento según el rol del usuario (admin o usuario normal).
- `app.py`: Navegación principal de la app con menú horizontal (Inicio, Informe, Evaluación, Administración).
- `start.py`: Página de inicio e informe, con navegación tipo libro usando `streamlit_book` y extracción de bloques desde un PDF.
- `evaluacion.py`: Implementación del cuestionario de evaluación para cada proveedor y bloque, con guardado de respuestas y descarga en Excel.
- `admin.py`: Panel de administración para registrar nuevos usuarios y visualizar histogramas de votaciones por bloque y totales usando Plotly.
- `init_db.py`: Script para inicializar la base de datos SQLite (`database.db`), crear tablas y usuarios iniciales (incluyendo admin y usuario de pruebas).
- `database.db`: Base de datos SQLite con las tablas `usuarios` y `evaluacion`.
- `img/`: Carpeta para imágenes, como el logo de la organización.
- `style.css`: Estilos personalizados para la app.

## Funcionalidades

- **Inicio de sesión:**
  - Usuarios registrados pueden iniciar sesión.
  - Roles: `admin` y `user`.
- **Cuestionario de evaluación:**
  - Cada usuario puede evaluar a los proveedores (KEYRUS, EON, MULTIPLICA, SCANDA) en diferentes bloques y criterios.
  - Las respuestas se guardan en la base de datos y pueden descargarse en Excel.
- **Panel de administración:**
  - Solo accesible para usuarios con rol `admin`.
  - Permite registrar nuevos usuarios y visualizar gráficos de resultados.
- **Informe interactivo:**
  - Navegación por bloques del informe PDF usando `streamlit_book`.

## Instalación y Ejecución

1. **Clonar el repositorio y crear entorno virtual:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

3. **Inicializar la base de datos y usuarios:**

```bash
python init_db.py
```

4. **Ejecutar la aplicación:**

```bash
streamlit run main.py
```

## Dependencias principales
- streamlit
- streamlit-option-menu
- streamlit-book
- pandas
- openpyxl
- plotly
- bcrypt
- PyPDF2

## Usuarios iniciales
- Usuarios tipo `user` y un usuario `admin` (ver consola tras ejecutar `init_db.py` para contraseñas generadas).
- Usuario de pruebas: `prueba.test`
- Usuario administrador: `admin.app`

## Personalización
- Puedes modificar los bloques, criterios y proveedores en `evaluacion.py`.
- El informe PDF debe estar en la ruta `~/Documents/Informe Criterios de Valor - Proveedores.pdf`.

## Créditos
Desarrollado por el equipo de Arquitectura y Gobierno de Datos.
