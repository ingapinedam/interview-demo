#!/usr/bin/env python3
"""
Generador de archivo SQL para migración
Convierte datos de SQLite a SQL compatible con PostgreSQL
"""

import sqlite3
import os
from datetime import datetime


def escapar_sql(texto):
    """Escapar comillas simples para SQL"""
    if texto is None:
        return 'NULL'
    return "'" + str(texto).replace("'", "''") + "'"


def generar_sql_migracion(sqlite_path, sql_output):
    """
    Genera archivo SQL con INSERT statements desde SQLite
    """
    try:
        # Verificar que el archivo SQLite existe
        if not os.path.exists(sqlite_path):
            print(f"❌ Archivo SQLite no encontrado: {sqlite_path}")
            return False

        # Conectar a SQLite
        print(f"📖 Leyendo datos de: {sqlite_path}")
        conn = sqlite3.connect(sqlite_path)
        cursor = conn.cursor()

        # Verificar si la tabla existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='preguntas'")
        if not cursor.fetchone():
            print("❌ Tabla 'preguntas' no encontrada en SQLite")
            return False

        # Obtener estructura de la tabla y determinar columnas disponibles
        cursor.execute("PRAGMA table_info(preguntas)")
        columnas = cursor.fetchall()
        columnas_nombres = [col[1] for col in columnas]

        print(f"📋 Estructura de tabla encontrada: {len(columnas)} columnas")
        print(f"📋 Columnas disponibles: {', '.join(columnas_nombres)}")

        # Verificar qué columnas existen
        tiene_categoria = 'categoria' in columnas_nombres
        tiene_tipo = 'tipo' in columnas_nombres

        # Obtener todos los datos con las columnas disponibles
        if tiene_categoria and tiene_tipo:
            cursor.execute("SELECT habilidad, pregunta, tipo, nivel, categoria FROM preguntas")
        elif tiene_tipo:
            cursor.execute("SELECT habilidad, pregunta, tipo, nivel FROM preguntas")
        else:
            cursor.execute("SELECT habilidad, pregunta, nivel FROM preguntas")

        registros = cursor.fetchall()
        total_registros = len(registros)
        print(f"📊 Registros encontrados: {total_registros}")

        if total_registros == 0:
            print("⚠️ No hay datos para migrar")
            return False

        # Generar archivo SQL
        print(f"📝 Generando archivo SQL: {sql_output}")

        with open(sql_output, 'w', encoding='utf-8') as f:
            # Header del archivo
            f.write("-- =====================================================\n")
            f.write("-- MIGRACIÓN DE PREGUNTAS DE ENTREVISTA\n")
            f.write("-- =====================================================\n")
            f.write(f"-- Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"-- Origen: {sqlite_path}\n")
            f.write(f"-- Total registros: {total_registros}\n")
            f.write("-- =====================================================\n\n")

            # Crear tabla (compatible con PostgreSQL)
            f.write("-- Crear tabla si no existe\n")
            f.write("CREATE TABLE IF NOT EXISTS preguntas (\n")
            f.write("    id SERIAL PRIMARY KEY,\n")
            f.write("    habilidad VARCHAR(100) NOT NULL,\n")
            f.write("    pregunta TEXT NOT NULL,\n")
            f.write("    tipo VARCHAR(50) DEFAULT 'general',\n")
            f.write("    nivel VARCHAR(50) DEFAULT 'intermedio',\n")
            f.write("    categoria VARCHAR(50) DEFAULT 'tecnica',\n")
            f.write("    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n")
            f.write("    CONSTRAINT unique_pregunta UNIQUE(habilidad, pregunta)\n")
            f.write(");\n\n")

            # Crear índices
            f.write("-- Crear índices para optimizar consultas\n")
            f.write("CREATE INDEX IF NOT EXISTS idx_habilidad ON preguntas(habilidad);\n")
            f.write("CREATE INDEX IF NOT EXISTS idx_nivel ON preguntas(nivel);\n")
            f.write("CREATE INDEX IF NOT EXISTS idx_tipo ON preguntas(tipo);\n")
            f.write(
                "CREATE INDEX IF NOT EXISTS idx_full_search ON preguntas USING gin(to_tsvector('spanish', pregunta));\n\n")

            # Limpiar datos existentes (opcional)
            f.write("-- Opcional: Limpiar datos existentes\n")
            f.write("-- DELETE FROM preguntas;\n\n")

            # Iniciar transacción
            f.write("-- Iniciar transacción para inserción segura\n")
            f.write("BEGIN;\n\n")

            # Agrupar por habilidad para mejor organización
            cursor.execute("SELECT DISTINCT habilidad FROM preguntas ORDER BY habilidad")
            habilidades = [row[0] for row in cursor.fetchall()]

            contador_total = 0

            for habilidad in habilidades:
                f.write(f"-- ===============================\n")
                f.write(f"-- HABILIDAD: {habilidad.upper()}\n")
                f.write(f"-- ===============================\n\n")

                # Obtener estructura real de la tabla primero
                cursor.execute("PRAGMA table_info(preguntas)")
                columnas_info = {col[1]: col[2] for col in cursor.fetchall()}

                # Determinar qué columnas existen
                tiene_categoria = 'categoria' in columnas_info
                tiene_tipo = 'tipo' in columnas_info

                # Construir query según columnas disponibles
                if tiene_categoria and tiene_tipo:
                    query = "SELECT habilidad, pregunta, tipo, nivel, categoria FROM preguntas WHERE habilidad = ? ORDER BY nivel, pregunta"
                elif tiene_tipo:
                    query = "SELECT habilidad, pregunta, tipo, nivel FROM preguntas WHERE habilidad = ? ORDER BY nivel, pregunta"
                else:
                    query = "SELECT habilidad, pregunta, nivel FROM preguntas WHERE habilidad = ? ORDER BY nivel, pregunta"

                cursor.execute(query, (habilidad,))
                preguntas_habilidad = cursor.fetchall()
                contador_habilidad = 0

                for registro in preguntas_habilidad:
                    if tiene_categoria and tiene_tipo:
                        habilidad_val, pregunta_val, tipo_val, nivel_val, categoria_val = registro
                    elif tiene_tipo:
                        habilidad_val, pregunta_val, tipo_val, nivel_val = registro
                        categoria_val = 'tecnica'  # Valor por defecto
                    else:
                        habilidad_val, pregunta_val, nivel_val = registro
                        tipo_val = 'general'  # Valor por defecto
                        categoria_val = 'tecnica'  # Valor por defecto

                    # Escapar valores para SQL
                    habilidad_sql = escapar_sql(habilidad_val)
                    pregunta_sql = escapar_sql(pregunta_val)
                    tipo_sql = escapar_sql(tipo_val)
                    nivel_sql = escapar_sql(nivel_val)
                    categoria_sql = escapar_sql(categoria_val)

                    # Generar INSERT con ON CONFLICT para evitar duplicados
                    f.write(f"INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES\n")
                    f.write(f"({habilidad_sql}, {pregunta_sql}, {tipo_sql}, {nivel_sql}, {categoria_sql})\n")
                    f.write(f"ON CONFLICT (habilidad, pregunta) DO NOTHING;\n\n")

                    contador_habilidad += 1
                    contador_total += 1

                f.write(f"-- Total {habilidad}: {contador_habilidad} preguntas\n\n")

            # Finalizar transacción
            f.write("-- Confirmar transacción\n")
            f.write("COMMIT;\n\n")

            # Estadísticas finales
            f.write("-- =====================================================\n")
            f.write("-- VERIFICACIÓN Y ESTADÍSTICAS\n")
            f.write("-- =====================================================\n\n")

            f.write("-- Contar registros insertados\n")
            f.write("SELECT COUNT(*) as total_preguntas FROM preguntas;\n\n")

            f.write("-- Preguntas por habilidad\n")
            f.write("SELECT habilidad, COUNT(*) as total\n")
            f.write("FROM preguntas\n")
            f.write("GROUP BY habilidad\n")
            f.write("ORDER BY total DESC;\n\n")

            f.write("-- Preguntas por nivel\n")
            f.write("SELECT nivel, COUNT(*) as total\n")
            f.write("FROM preguntas\n")
            f.write("GROUP BY nivel\n")
            f.write("ORDER BY total DESC;\n\n")

            f.write(f"-- Total de INSERT statements generados: {contador_total}\n")
            f.write(f"-- Archivo generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Cerrar conexión
        conn.close()

        print(f"✅ Migración SQL generada exitosamente!")
        print(f"📁 Archivo: {sql_output}")
        print(f"📊 Total INSERT statements: {contador_total}")
        print(f"🎯 Habilidades procesadas: {len(habilidades)}")

        return True

    except Exception as e:
        print(f"❌ Error generando migración: {e}")
        return False


def mostrar_estadisticas_sqlite(sqlite_path):
    """Mostrar estadísticas del archivo SQLite"""
    try:
        conn = sqlite3.connect(sqlite_path)
        cursor = conn.cursor()

        print("\n📊 ESTADÍSTICAS DE SQLITE:")
        print("=" * 40)

        # Total de registros
        cursor.execute("SELECT COUNT(*) FROM preguntas")
        total = cursor.fetchone()[0]
        print(f"Total preguntas: {total}")

        # Por habilidad
        print(f"\nPor habilidad:")
        cursor.execute("""
                       SELECT habilidad, COUNT(*) as total
                       FROM preguntas
                       GROUP BY habilidad
                       ORDER BY total DESC
                       """)
        for habilidad, count in cursor.fetchall():
            print(f"  • {habilidad}: {count}")

        # Por nivel
        print(f"\nPor nivel:")
        cursor.execute("""
                       SELECT nivel, COUNT(*) as total
                       FROM preguntas
                       GROUP BY nivel
                       ORDER BY total DESC
                       """)
        for nivel, count in cursor.fetchall():
            print(f"  • {nivel}: {count}")

        conn.close()

    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {e}")


def main():
    print("🎯 GENERADOR DE MIGRACIÓN SQL")
    print("=" * 50)

    # Rutas de archivos
    sqlite_path = "../preguntas_entrevista.db"  # Relativo a src/
    sql_output = "migracion_postgresql.sql"

    # Verificar si existe SQLite
    if not os.path.exists(sqlite_path):
        print(f"❌ Archivo SQLite no encontrado en: {sqlite_path}")
        print("💡 Asegúrate de que el archivo existe o ajusta la ruta")

        # Buscar el archivo en ubicaciones comunes
        posibles_rutas = [
            "preguntas_entrevista.db",
            "../preguntas_entrevista.db",
            "../../preguntas_entrevista.db"
        ]

        print("\n🔍 Buscando archivo en ubicaciones comunes:")
        for ruta in posibles_rutas:
            if os.path.exists(ruta):
                print(f"✅ Encontrado en: {ruta}")
                sqlite_path = ruta
                break
            else:
                print(f"❌ No encontrado: {ruta}")

        if not os.path.exists(sqlite_path):
            print("\n💡 Ejecuta primero tu aplicación Flask para generar la BD SQLite")
            return

    # Mostrar estadísticas del archivo origen
    mostrar_estadisticas_sqlite(sqlite_path)

    # Generar migración
    print(f"\n🔄 Generando archivo SQL...")
    if generar_sql_migracion(sqlite_path, sql_output):
        print("\n🎉 ¡Migración generada exitosamente!")
        print(f"\n📋 PRÓXIMOS PASOS:")
        print(f"1. Abrir PostgreSQL (Postico, pgAdmin, o psql)")
        print(f"2. Conectar a la base de datos 'preguntas_entrevista'")
        print(f"3. Ejecutar el archivo: {sql_output}")
        print(f"4. Verificar que los datos se insertaron correctamente")

        print(f"\n💡 COMANDO PARA PSQL:")
        print(f"psql preguntas_entrevista < {sql_output}")

    else:
        print("❌ Error generando la migración")


if __name__ == "__main__":
    main()