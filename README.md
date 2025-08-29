# 🎯 Agente Entrevistador IA - Sistema de Preguntas Técnicas

Sistema profesional para generar preguntas de entrevistas técnicas personalizado con base de datos SQLite y arquitectura modular.

## 📋 Características

- ✅ **130+ preguntas técnicas** curadas por expertos
- ✅ **12 tecnologías** principales (Python, JavaScript, React, SQL, Java, Docker, etc.)
- ✅ **3 niveles de dificultad** (básico, intermedio, avanzado)
- ✅ **Exportación múltiple** (TXT, JSON, CSV)
- ✅ **Selección inteligente** (por números, nombres, niveles, aleatoria)
- ✅ **Base de datos local** (sin dependencias externas)
- ✅ **Arquitectura modular** y escalable

## 🚀 Instalación y Configuración

### Prerequisitos

- **macOS** (probado en versiones recientes)
- **Python 3.8+** 
- **Terminal** con acceso a comandos básicos

### Paso 1: Verificar Python

```bash
# Verificar que tienes Python instalado
python3 --version
```

Si no tienes Python:
```bash
# Opción A: Instalar con Homebrew
brew install python

# Opción B: Descargar desde python.org
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
source venv/bin/activate

# Verificar que está activado (debe mostrar (venv) al inicio)
which python
```

### Paso 4: Crear los Archivos del Sistema

Crea los siguientes archivos en la carpeta `src/`:

#### 4.1 Crear `src/__init__.py`
```bash
touch src/__init__.py
```

#### 4.2 Crear `src/database_manager.py`
```python
# Copiar el código completo del database_manager.py
# (Disponible en los artifacts anteriores)
```

#### 4.3 Crear `src/data_loader.py`
```python
# Copiar el código completo del data_loader.py
# (Disponible en los artifacts anteriores)
```

#### 4.4 Crear `src/agente.py`
```python
# Copiar el código completo del agente.py
# (Disponible en los artifacts anteriores)
```

### Paso 5: Estructura Final

Tu estructura debe verse así:
```
agente-entrevistador/
├── venv/                      # Entorno virtual
├── src/
│   ├── __init__.py           # Archivo vacío
│   ├── database_manager.py   # Gestor de base de datos
│   ├── data_loader.py        # Cargador de datos
│   └── agente.py             # Aplicación principal
└── README.md                 # Este archivo
```

## ▶️ Ejecutar la Aplicación

### Primera Ejecución

```bash
# 1. Activar entorno virtual (si no está activo)
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Navegar al directorio src
cd src

# 4. Ejecutar la aplicación
python agente.py
```

### Ejecuciones Posteriores

```bash
# Desde el directorio raíz del proyecto
source venv/bin/activate
cd src
python agente.py
```

## 📖 Guía de Uso

### 1. Primera Vez que Ejecutas

```
🎯 AGENTE ENTREVISTADOR - ARQUITECTURA PROFESIONAL
================================================================
🆕 Primera ejecución detectada
🔄 Inicializando base de datos con preguntas predefinidas...
📚 Base de datos lista con 130+ preguntas
```

### 2. Selección de Habilidades

Tienes varias opciones para seleccionar habilidades:

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

### 3. Ejemplo de Salida

```
🎯 PYTHON:
  1. ¿Cuáles son las diferencias entre listas y tuplas en Python?
  2. Explica el concepto de decoradores en Python y da un ejemplo

🎯 REACT:
  1. ¿Cuál es la diferencia entre componentes funcionales y de clase?
  2. Explica cómo funciona el Virtual DOM

📈 ESTADÍSTICAS FINALES:
• Habilidades evaluadas: 2
• Total de preguntas: 4
• Promedio por habilidad: 2.0
```

### 4. Opciones del Menú Principal

1. **Ver resumen** - Muestra preguntas actuales
2. **Exportar** - Guarda en TXT, JSON o CSV
3. **Cambiar habilidades** - Nueva selección
4. **Configuración avanzada** - Filtros y opciones
5. **Estadísticas** - Info de la base de datos
6. **Herramientas BD** - Backup y mantenimiento
7. **Salir** - Termina la aplicación

## 🔧 Configuración Avanzada

### Filtrar por Nivel de Dificultad

```bash
# En configuración avanzada, opción 1
Nivel a filtrar: basico      # Solo preguntas básicas
Nivel a filtrar: intermedio  # Solo preguntas intermedias  
Nivel a filtrar: avanzado    # Solo preguntas avanzadas
Nivel a filtrar: ninguno     # Todos los niveles
```

### Cambiar Cantidad de Preguntas

```bash
# En configuración avanzada, opción 2
Nueva cantidad por habilidad (1-10): 5
# Genera 5 preguntas por cada habilidad seleccionada
```

### Exportar Preguntas

```bash
# Opción 2 del menú principal
Formatos disponibles:
1. TXT (texto plano)
2. JSON (estructura de datos)  
3. CSV (hoja de cálculo)

Selecciona formato (1-3): 1
✅ Preguntas exportadas: entrevista_tecnica_20241201_143022.txt
```

## 🗃️ Gestión de Base de Datos

### Ver Estadísticas

```bash
# Opción 5 del menú principal
📊 ESTADÍSTICAS DETALLADAS DE LA BASE DE DATOS
============================================================
📁 Archivo: preguntas_entrevista.db
📚 Total de preguntas: 130
🎯 Total de habilidades: 12
```

### Backup de la Base de Datos

```bash
# En herramientas de BD, opción 2
✅ BD exportada a: backup_bd_20241201_143530.sql
```

### Buscar Preguntas

```bash
# En herramientas de BD, opción 4
Término a buscar: docker
🔍 Encontradas 15 preguntas:
• Docker (basico): ¿Qué es Docker y qué problema resuelve?
• Docker (intermedio): ¿Cuál es la diferencia entre una imagen y...
```

## ❌ Solución de Problemas

### Error: "No module named 'database_manager'"

```bash
# Verifica que estés en el directorio src
cd src
python agente.py

# Verifica que los archivos existan
ls -la
# Debe mostrar: database_manager.py, data_loader.py, agente.py
```

### Error: "command not found: python3"

```bash
# Instalar Python
brew install python
# O descargar desde python.org
```

### Error: "No such file or directory"

```bash
# Verifica que el entorno virtual esté activado
source venv/bin/activate

# Debe mostrar (venv) al inicio del prompt
```

### Base de Datos Corrupta

```bash
# Eliminar base de datos y reinicializar
rm preguntas_entrevista.db
python agente.py
# Se creará automáticamente una nueva BD
```

## 🎯 Habilidades Disponibles

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

## 📚 Ejemplos de Preguntas por Nivel

### Básico
- ¿Qué es Python y cuáles son sus características principales?
- ¿Cuáles son los tipos de datos primitivos en JavaScript?
- ¿Qué es React y cuáles son sus características principales?

### Intermedio  
- ¿Cuáles son las diferencias entre listas y tuplas en Python?
- ¿Cuál es la diferencia entre var, let y const en JavaScript?
- ¿Qué son los Hooks y cuáles son los más comunes en React?

### Avanzado
- ¿Cómo funciona el GIL (Global Interpreter Lock) en Python?
- ¿Cómo implementarías el patrón Observer en JavaScript?
- ¿Cómo optimizarías el rendimiento de una aplicación React?

## 🔄 Actualización y Mantenimiento

### Agregar Nuevas Preguntas

```bash
# En configuración avanzada, opción 4
Nombre de la habilidad: Flutter
Ingresa preguntas (escribe 'fin' para terminar):
1. ¿Qué es Flutter y cuáles son sus ventajas?
2. ¿Cómo manejas el estado en Flutter?
fin
Nivel (basico/intermedio/avanzado) [intermedio]: basico
✅ Se agregaron 2 preguntas para Flutter
```

### Backup Automático

El sistema crea automáticamente:
- `preguntas_entrevista.db` - Base de datos principal
- `entrevista_tecnica_FECHA.txt` - Exports de sesiones
- `backup_bd_FECHA.sql` - Backups completos

## 📞 Soporte

Si encuentras problemas:

1. **Verifica la estructura** de archivos
2. **Confirma que el entorno virtual** esté activo
3. **Revisa que todos los archivos** estén presentes
4. **Elimina la BD** y deja que se recree automáticamente

## 🏆 Casos de Uso

- **Reclutadores**: Generar preguntas personalizadas por rol
- **Equipos de desarrollo**: Preparar entrevistas técnicas
- **Candidatos**: Practicar para entrevistas
- **Empresas**: Estandarizar procesos de entrevistas
- **Bootcamps**: Material de evaluación técnica

## 📄 Licencia

Este proyecto es de uso libre para fines educativos y profesionales.

---

*Desarrollado con Python 3, SQLite y mucho ☕*
