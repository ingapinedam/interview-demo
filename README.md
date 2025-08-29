# Agente Entrevistador IA - Sistema de Preguntas Técnicas

Sistema profesional para generar preguntas de entrevistas técnicas personalizado con soporte para **SQLite** y **PostgreSQL** con arquitectura modular.

## Características

- ✅ **130+ preguntas técnicas** curadas por expertos
- ✅ **12 tecnologías** principales (Python, JavaScript, React, SQL, Java, Docker, etc.)
- ✅ **3 niveles de dificultad** (básico, intermedio, avanzado)
- ✅ **Exportación múltiple** (TXT, JSON, CSV)
- ✅ **Selección inteligente** (por números, nombres, niveles, aleatoria)
- ✅ **Base de datos dual** (SQLite local + PostgreSQL remoto)
- ✅ **Arquitectura modular** y escalable
- ✅ **Interfaz web** responsive con Flask

## Instalación y Configuración

### Prerequisitos

- **Python 3.8+** (recomendado 3.10+)
- **PostgreSQL** (si planeas usarlo)
- **Terminal** con acceso a comandos básicos

### Paso 1: Verificar Python

```bash
# Verificar que tienes Python instalado
python3 --version
```

Si no tienes Python:
```bash
# Opción A: macOS con Homebrew
brew install python

# Opción B: Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-venv

# Opción C: Descargar desde python.org
# Ve a https://www.python.org/downloads/
```

### Paso 2: Crear Estructura del Proyecto

```bash
# Crear directorio principal
mkdir agente-entrevistador
cd agente-entrevistador

# Crear subdirectorio para código fuente
mkdir src
```

### Paso 3: Configurar Entorno Virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En macOS/Linux:
source venv/bin/activate

# En Windows:
# venv\Scripts\activate

# Verificar que está activado (debe mostrar (venv) al inicio)
which python
```

### Paso 4: Instalar Dependencias

```bash
# Activar entorno virtual si no está activo
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

**Si tienes problemas con psycopg2 en Python 3.13:**
```bash
# Opción 1: Usar versión más reciente
pip install "psycopg2-binary>=2.9.10"

# Opción 2: En macOS, instalar PostgreSQL primero
brew install postgresql@14
pip install psycopg2 --no-binary psycopg2

# Opción 3: Usar psycopg3 (más moderno)
pip install "psycopg[binary]>=3.1.0"
```

### Paso 5: Configurar Base de Datos

#### Opción A: SQLite (Por defecto - sin configuración)
No requiere configuración adicional. La base de datos se crea automáticamente.

#### Opción B: PostgreSQL (Recomendado para producción)

1. **Instalar PostgreSQL:**
```bash
# macOS con Homebrew
brew install postgresql@14
brew services start postgresql@14

# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

2. **Crear base de datos:**
```bash
# Conectar como superuser
sudo -u postgres psql

# Crear usuario y base de datos
CREATE USER tu_usuario WITH PASSWORD 'tu_password';
CREATE DATABASE preguntas_entrevista OWNER tu_usuario;
GRANT ALL PRIVILEGES ON DATABASE preguntas_entrevista TO tu_usuario;
\q
```

3. **Configurar variables de entorno:**
```bash
# Crear archivo .env en el directorio raíz
cp .env.example .env

# Editar .env con tus credenciales
DATABASE_TYPE=postgresql
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=preguntas_entrevista
POSTGRES_USER=tu_usuario
POSTGRES_PASSWORD=tu_password
```

### Paso 6: Crear los Archivos del Sistema

Crea los siguientes archivos en la carpeta `src/`:

#### Estructura Final

```
agente-entrevistador/
├── venv/                      # Entorno virtual
├── src/
│   ├── __init__.py           # Archivo vacío
│   ├── config.py             # Configuración de BD
│   ├── database_manager.py   # Gestor de BD (dual)
│   ├── data_loader.py        # Cargador de datos
│   ├── agente.py             # Aplicación CLI
│   ├── app.py                # Servidor web Flask
│   ├── test_migration.py     # Script de pruebas
│   └── templates/            # Templates HTML (opcional)
├── .env.example              # Template de configuración
├── .env                      # Tu configuración (no versionar)
├── requirements.txt          # Dependencias
└── README.md                 # Este archivo
```

## Ejecutar la Aplicación

### Modo CLI (Terminal)

```bash
# 1. Activar entorno virtual (si no está activo)
source venv/bin/activate

# 2. Navegar al directorio src
cd src

# 3. Primera ejecución - prueba la conexión
python test_migration.py

# 4. Ejecutar aplicación CLI
python agente.py
```

### Modo Web (Interfaz HTML)

```bash
# 1. Activar entorno virtual
source venv/bin/activate

# 2. Navegar al directorio src
cd src

# 3. Ejecutar servidor Flask
python app.py

# 4. Abrir navegador en: http://localhost:5000
```

## Configuración de Base de Datos

### Cambiar Tipo de Base de Datos

El sistema puede usar SQLite o PostgreSQL. Se configura mediante variables de entorno:

#### Para SQLite (por defecto):
```bash
# En .env
DATABASE_TYPE=sqlite
SQLITE_PATH=preguntas_entrevista.db
```

#### Para PostgreSQL:
```bash
# En .env
DATABASE_TYPE=postgresql
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=preguntas_entrevista
POSTGRES_USER=tu_usuario
POSTGRES_PASSWORD=tu_password
```

### Migrar de SQLite a PostgreSQL

```bash
# 1. Generar SQL desde SQLite existente
python generate_migration.py

# 2. Ejecutar en PostgreSQL
psql preguntas_entrevista < migracion_postgresql.sql

# 3. Cambiar configuración
# Editar .env: DATABASE_TYPE=postgresql

# 4. Probar conexión
python test_migration.py
```

## Guía de Uso

### Interfaz CLI

#### 1. Selección de Habilidades

```bash
# Por números
Tu selección: 1,3,5

# Por nombres
Tu selección: Python,React,JavaScript  

# Por rango
Tu selección: 1-5

# Filtrar por nivel
Tu selección: nivel:basico

# Todas las habilidades
Tu selección: todas

# Selección aleatoria
Tu selección: aleatorio:4
```

#### 2. Menú Principal

1. **Ver resumen** - Muestra preguntas actuales
2. **Exportar** - Guarda en TXT, JSON o CSV
3. **Cambiar habilidades** - Nueva selección
4. **Configuración avanzada** - Filtros y opciones
5. **Estadísticas** - Info de la base de datos
6. **Herramientas BD** - Backup y mantenimiento
7. **Salir** - Termina la aplicación

### Interfaz Web

1. Abre tu navegador en `http://localhost:5000`
2. Selecciona las habilidades que deseas evaluar
3. Configura filtros (nivel, cantidad por habilidad)
4. Genera preguntas
5. Exporta en el formato deseado

## Características Avanzadas

### Búsqueda de Texto Completo (PostgreSQL)

```sql
-- Buscar preguntas que contengan "docker"
SELECT * FROM preguntas 
WHERE to_tsvector('spanish', pregunta) @@ to_tsquery('spanish', 'docker');
```

### API REST (Modo Web)

```bash
# Obtener estado del sistema
curl http://localhost:5000/api/status

# Obtener todas las habilidades
curl http://localhost:5000/api/habilidades

# Generar preguntas
curl -X POST http://localhost:5000/api/generar-preguntas \
  -H "Content-Type: application/json" \
  -d '{"habilidades": ["Python", "React"], "cantidad_por_habilidad": 3}'
```

### Rendimiento y Escalabilidad

**SQLite (recomendado para):**
- Desarrollo local
- Equipos pequeños
- Hasta 1000 preguntas
- Sin concurrencia alta

**PostgreSQL (recomendado para):**
- Producción
- Equipos grandes
- Miles de preguntas
- Acceso concurrente
- Búsqueda avanzada
- Análisis de datos

## Solución de Problemas

### Error de Conexión PostgreSQL

```bash
# Verificar que PostgreSQL esté ejecutándose
brew services list | grep postgresql
# o en Linux:
sudo systemctl status postgresql

# Probar conexión manual
psql -h localhost -p 5432 -U tu_usuario preguntas_entrevista

# Verificar variables de entorno
python -c "from config import DatabaseConfig; print(DatabaseConfig.get_postgres_connection_params())"
```

### Error: "psycopg2 not found"

```bash
# Para Python 3.13 en macOS
brew install postgresql@14
pip install "psycopg2-binary>=2.9.10"

# Si sigue fallando, instalar desde fuente
pip install psycopg2 --no-binary psycopg2

# Alternativa moderna
pip install "psycopg[binary]>=3.1.0"
```

### Problemas de Migración

```bash
# Ejecutar suite completa de pruebas
python test_migration.py

# Si fallan las pruebas, revisar:
# 1. Conexión a PostgreSQL
# 2. Credenciales en .env
# 3. Permisos de usuario en PostgreSQL
```

### Base de Datos Corrupta

```bash
# SQLite
rm preguntas_entrevista.db
python agente.py  # Se recrea automáticamente

# PostgreSQL
psql preguntas_entrevista
DROP TABLE IF EXISTS preguntas;
\q
python agente.py  # Se recrea automáticamente
```

## Habilidades Disponibles

El sistema incluye preguntas para estas tecnologías:

1. **Python** - 13 preguntas (básico: 4, intermedio: 5, avanzado: 4)
2. **JavaScript** - 13 preguntas (básico: 4, intermedio: 5, avanzado: 4)  
3. **React** - 12 preguntas (básico: 4, intermedio: 5, avanzado: 3)
4. **SQL** - 13 preguntas (básico: 4, intermedio: 5, avanzado: 4)
5. **Java** - 13 preguntas (básico: 4, intermedio: 5, avanzado: 4)
6. **Docker** - 13 preguntas (básico: 4, intermedio: 5, avanzado: 4)
7. **Git** - 13 preguntas (básico: 4, intermedio: 5, avanzado: 4)
8. **Node.js** - 13 preguntas (básico: 4, intermedio: 5, avanzado: 4)
9. **Angular** - 12 preguntas (básico: 4, intermedio: 5, avanzado: 3)
10. **AWS** - 12 preguntas (básico: 4, intermedio: 5, avanzado: 3)
11. **CSS** - 12 preguntas (básico: 4, intermedio: 5, avanzado: 3)
12. **MongoDB** - 12 preguntas (básico: 4, intermedio: 5, avanzado: 3)

## Backup y Mantenimiento

### Backup Automático

```bash
# PostgreSQL
pg_dump preguntas_entrevista > backup_$(date +%Y%m%d).sql

# SQLite (desde la aplicación)
python agente.py
# Menú -> Herramientas BD -> Exportar BD completa
```

### Optimización PostgreSQL

```sql
-- Análizar tablas para optimizar consultas
ANALYZE preguntas;

-- Ver estadísticas de uso
SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del
FROM pg_stat_user_tables 
WHERE tablename = 'preguntas';

-- Reindexar si es necesario
REINDEX TABLE preguntas;
```

## Casos de Uso

- **Reclutadores**: Generar preguntas personalizadas por rol
- **Equipos de desarrollo**: Preparar entrevistas técnicas  
- **Candidatos**: Practicar para entrevistas
- **Empresas**: Estandarizar procesos de entrevistas
- **Bootcamps**: Material de evaluación técnica
- **Consultorías**: Evaluar competencias técnicas

## Desarrollo y Contribución

### Agregar Nuevas Tecnologías

```python
# En data_loader.py, agregar al diccionario preguntas_iniciales
"NuevaTecnologia": {
    "basico": [
        "¿Qué es NuevaTecnologia?",
        # ... más preguntas
    ],
    "intermedio": [
        # ... preguntas intermedias
    ],
    "avanzado": [
        # ... preguntas avanzadas  
    ]
}
```

### Ejecutar Pruebas

```bash
# Suite completa de pruebas
python test_migration.py

# Probar solo conexión
python database_manager.py

# Validar datos
python data_loader.py
```

## Arquitectura Técnica

### Componentes Principales

- **config.py**: Manejo de configuración dual SQLite/PostgreSQL
- **database_manager.py**: Abstracción de base de datos con soporte dual
- **data_loader.py**: Cargador de datos inicial con 130+ preguntas
- **agente.py**: Interfaz CLI interactiva
- **app.py**: Servidor web Flask con API REST

### Ventajas de PostgreSQL

- Búsqueda de texto completo en español
- Índices GIN para consultas rápidas  
- Transacciones ACID robustas
- Escalabilidad horizontal
- Análisis avanzado con SQL
- Conexiones concurrentes

### Compatibilidad

El código funciona con ambas bases de datos sin cambios. La migración es transparente cambiando solo variables de entorno.

---

*Desarrollado con Python 3, SQLite/PostgreSQL, Flask y arquitectura modular*