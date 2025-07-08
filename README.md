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


## Instrucciones para el llenado de las evaluaciones de proveedores

1. **Acceso y autenticación:**
   - Inicia sesión con tu usuario y contraseña proporcionados por el administrador.
   - Si eres usuario tipo `user`, accederás al cuestionario de evaluación. Si eres `admin`, tendrás acceso al panel de administración.

2. **Evaluación de proveedores:**
   - Selecciona el proveedor a evaluar en el menú desplegable. Solo aparecerán los proveedores que aún no has evaluado.
   - Para cada proveedor, deberás responder una serie de bloques (criterios) y preguntas específicas.
   - Los bloques y criterios principales son:
     - Capacidades Técnicas y Funcionales
     - Fortaleza y cobertura del proveedor cloud (GCP / AWS)
     - Costo Total de Propiedad (TCO)
     - Gobierno de Datos y Cumplimiento
     - Capacidad de Soporte, Transferencia de Conocimiento y Acompañamiento
     - Reputación, experiencia y casos de éxito
     - Capacidades en analítica, IA y ML (valor añadido)
     - Propuesta Técnica y de Valor
   - Cada pregunta se responde seleccionando una opción de cumplimiento, de 1 (No cumple) a 5 (Cumple totalmente o excede expectativas).
   - Puedes avanzar bloque por bloque y proveedor por proveedor. Si cierras sesión, tu progreso se guarda y podrás continuar desde donde quedaste.

3. **Finalización y descarga de resultados:**
   - Cuando hayas evaluado a todos los proveedores, verás un mensaje de agradecimiento y un botón para descargar en Excel todas tus respuestas.
   - El archivo Excel contendrá todas tus respuestas cuantitativas y cualitativas por proveedor, bloque y pregunta.

4. **Notas adicionales:**
   - Si necesitas reiniciar tu evaluación, contacta a un administrador para que borre tus respuestas desde el panel de administración.
   - Puedes modificar los bloques, criterios y proveedores editando el archivo `evaluacion.py`.
   - El informe PDF de criterios debe estar en la ruta `pdf_content/Informe Criterios de Valor - Proveedores.pdf`.


## Créditos
Desarrollado por el equipo de Arquitectura y Gobierno de Datos.
