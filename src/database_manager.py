"""
Gestor de Base de Datos para Preguntas de Entrevista
Maneja todas las operaciones de SQLite de forma desacoplada
"""

import sqlite3
import os
from typing import List, Optional, Tuple


class DatabaseManager:
    def __init__(self, db_name: str = "preguntas_entrevista.db"):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        """Inicializa la base de datos y crea las tablas necesarias"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Crear tabla principal de preguntas
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS preguntas
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               habilidad
                               TEXT
                               NOT
                               NULL,
                               pregunta
                               TEXT
                               NOT
                               NULL,
                               tipo
                               TEXT
                               DEFAULT
                               'general',
                               nivel
                               TEXT
                               DEFAULT
                               'intermedio',
                               categoria
                               TEXT
                               DEFAULT
                               'tecnica',
                               created_at
                               TIMESTAMP
                               DEFAULT
                               CURRENT_TIMESTAMP
                           )
                           ''')

            # Crear índices para mejorar rendimiento
            cursor.execute('''
                           CREATE INDEX IF NOT EXISTS idx_habilidad
                               ON preguntas(habilidad)
                           ''')

            cursor.execute('''
                           CREATE INDEX IF NOT EXISTS idx_tipo_nivel
                               ON preguntas(tipo, nivel)
                           ''')

            conn.commit()
            conn.close()

            return True

        except Exception as e:
            print(f"❌ Error inicializando base de datos: {e}")
            return False

    def ejecutar_sql_desde_archivo(self, archivo_sql: str) -> bool:
        """Ejecuta comandos SQL desde un archivo externo"""
        try:
            if not os.path.exists(archivo_sql):
                print(f"⚠️ Archivo SQL no encontrado: {archivo_sql}")
                return False

            with open(archivo_sql, 'r', encoding='utf-8') as file:
                sql_content = file.read()

            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Ejecutar múltiples comandos SQL
            cursor.executescript(sql_content)

            conn.commit()
            conn.close()

            print(f"✅ Archivo SQL ejecutado correctamente: {archivo_sql}")
            return True

        except Exception as e:
            print(f"❌ Error ejecutando archivo SQL: {e}")
            return False

    def agregar_pregunta(self, habilidad: str, pregunta: str,
                         tipo: str = "general", nivel: str = "intermedio",
                         categoria: str = "tecnica") -> bool:
        """Agrega una nueva pregunta a la base de datos"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute('''
                           INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria)
                           VALUES (?, ?, ?, ?, ?)
                           ''', (habilidad, pregunta, tipo, nivel, categoria))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"❌ Error agregando pregunta: {e}")
            return False

    def obtener_preguntas_por_habilidad(self, habilidad: str,
                                        cantidad: int = 2,
                                        nivel: Optional[str] = None) -> List[str]:
        """Obtiene preguntas de una habilidad específica"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            if nivel:
                cursor.execute('''
                               SELECT pregunta
                               FROM preguntas
                               WHERE habilidad LIKE ?
                                 AND nivel = ?
                               ORDER BY RANDOM() LIMIT ?
                               ''', (f'%{habilidad}%', nivel, cantidad))
            else:
                cursor.execute('''
                               SELECT pregunta
                               FROM preguntas
                               WHERE habilidad LIKE ?
                               ORDER BY RANDOM() LIMIT ?
                               ''', (f'%{habilidad}%', cantidad))

            preguntas = [row[0] for row in cursor.fetchall()]
            conn.close()

            return preguntas

        except Exception as e:
            print(f"❌ Error obteniendo preguntas: {e}")
            return []

    def obtener_todas_habilidades(self) -> List[str]:
        """Obtiene lista de todas las habilidades disponibles"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute('''
                           SELECT DISTINCT habilidad
                           FROM preguntas
                           ORDER BY habilidad
                           ''')

            habilidades = [row[0] for row in cursor.fetchall()]
            conn.close()

            return habilidades

        except Exception as e:
            print(f"❌ Error obteniendo habilidades: {e}")
            return []

    def obtener_estadisticas_habilidad(self, habilidad: str) -> dict:
        """Obtiene estadísticas detalladas de una habilidad"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Contar total
            cursor.execute('''
                           SELECT COUNT(*)
                           FROM preguntas
                           WHERE habilidad LIKE ?
                           ''', (f'%{habilidad}%',))
            total = cursor.fetchone()[0]

            # Contar por nivel
            cursor.execute('''
                           SELECT nivel, COUNT(*)
                           FROM preguntas
                           WHERE habilidad LIKE ?
                           GROUP BY nivel
                           ''', (f'%{habilidad}%',))
            niveles = dict(cursor.fetchall())

            # Contar por tipo
            cursor.execute('''
                           SELECT tipo, COUNT(*)
                           FROM preguntas
                           WHERE habilidad LIKE ?
                           GROUP BY tipo
                           ''', (f'%{habilidad}%',))
            tipos = dict(cursor.fetchall())

            conn.close()

            return {
                'habilidad': habilidad,
                'total': total,
                'por_nivel': niveles,
                'por_tipo': tipos
            }

        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
            return {}

    def contar_preguntas(self) -> int:
        """Cuenta el total de preguntas en la base de datos"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) FROM preguntas')
            total = cursor.fetchone()[0]
            conn.close()

            return total

        except Exception as e:
            print(f"❌ Error contando preguntas: {e}")
            return 0

    def contar_preguntas_por_habilidad(self, habilidad: str) -> int:
        """Cuenta preguntas de una habilidad específica"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute('''
                           SELECT COUNT(*)
                           FROM preguntas
                           WHERE habilidad LIKE ?
                           ''', (f'%{habilidad}%',))

            total = cursor.fetchone()[0]
            conn.close()

            return total

        except Exception as e:
            print(f"❌ Error contando preguntas: {e}")
            return 0

    def buscar_preguntas(self, termino: str, limit: int = 10) -> List[Tuple]:
        """Busca preguntas que contengan un término específico"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute('''
                           SELECT habilidad, pregunta, tipo, nivel
                           FROM preguntas
                           WHERE pregunta LIKE ?
                              OR habilidad LIKE ?
                           ORDER BY habilidad, pregunta LIMIT ?
                           ''', (f'%{termino}%', f'%{termino}%', limit))

            resultados = cursor.fetchall()
            conn.close()

            return resultados

        except Exception as e:
            print(f"❌ Error buscando preguntas: {e}")
            return []

    def obtener_resumen_completo(self) -> dict:
        """Obtiene un resumen completo de la base de datos"""
        try:
            total_preguntas = self.contar_preguntas()
            habilidades = self.obtener_todas_habilidades()

            estadisticas_por_habilidad = {}
            for habilidad in habilidades:
                estadisticas_por_habilidad[habilidad] = self.obtener_estadisticas_habilidad(habilidad)

            return {
                'total_preguntas': total_preguntas,
                'total_habilidades': len(habilidades),
                'habilidades': habilidades,
                'estadisticas': estadisticas_por_habilidad,
                'archivo_bd': self.db_name
            }

        except Exception as e:
            print(f"❌ Error obteniendo resumen: {e}")
            return {}

    def exportar_bd_a_sql(self, archivo_salida: str = "backup_preguntas.sql") -> bool:
        """Exporta toda la base de datos a un archivo SQL"""
        try:
            conn = sqlite3.connect(self.db_name)

            with open(archivo_salida, 'w', encoding='utf-8') as f:
                # Escribir esquema y datos
                for linea in conn.iterdump():
                    f.write('%s\n' % linea)

            conn.close()
            print(f"✅ Base de datos exportada a: {archivo_salida}")
            return True

        except Exception as e:
            print(f"❌ Error exportando BD: {e}")
            return False

    def limpiar_base_datos(self) -> bool:
        """Limpia completamente la base de datos"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute('DELETE FROM preguntas')
            conn.commit()
            conn.close()

            print("✅ Base de datos limpiada")
            return True

        except Exception as e:
            print(f"❌ Error limpiando BD: {e}")
            return False

    def obtener_preguntas_por_criterios(self,
                                        habilidades: List[str] = None,
                                        nivel: str = None,
                                        tipo: str = None,
                                        cantidad_por_habilidad: int = 2) -> dict:
        """Obtiene preguntas basado en múltiples criterios"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            preguntas_resultado = {}

            # Si no se especifican habilidades, usar todas
            if not habilidades:
                habilidades = self.obtener_todas_habilidades()

            for habilidad in habilidades:
                # Construir query dinámicamente
                query = "SELECT pregunta FROM preguntas WHERE habilidad LIKE ?"
                params = [f'%{habilidad}%']

                if nivel:
                    query += " AND nivel = ?"
                    params.append(nivel)

                if tipo:
                    query += " AND tipo = ?"
                    params.append(tipo)

                query += " ORDER BY RANDOM() LIMIT ?"
                params.append(cantidad_por_habilidad)

                cursor.execute(query, params)
                preguntas = [row[0] for row in cursor.fetchall()]

                if preguntas:
                    preguntas_resultado[habilidad] = preguntas

            conn.close()
            return preguntas_resultado

        except Exception as e:
            print(f"❌ Error obteniendo preguntas por criterios: {e}")
            return {}

    def actualizar_pregunta(self, pregunta_id: int, nueva_pregunta: str = None,
                            nuevo_nivel: str = None, nuevo_tipo: str = None) -> bool:
        """Actualiza una pregunta existente"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            updates = []
            params = []

            if nueva_pregunta:
                updates.append("pregunta = ?")
                params.append(nueva_pregunta)

            if nuevo_nivel:
                updates.append("nivel = ?")
                params.append(nuevo_nivel)

            if nuevo_tipo:
                updates.append("tipo = ?")
                params.append(nuevo_tipo)

            if not updates:
                print("⚠️ No hay cambios para actualizar")
                return False

            query = f"UPDATE preguntas SET {', '.join(updates)} WHERE id = ?"
            params.append(pregunta_id)

            cursor.execute(query, params)

            if cursor.rowcount > 0:
                conn.commit()
                conn.close()
                print(f"✅ Pregunta actualizada (ID: {pregunta_id})")
                return True
            else:
                conn.close()
                print(f"❌ No se encontró pregunta con ID: {pregunta_id}")
                return False

        except Exception as e:
            print(f"❌ Error actualizando pregunta: {e}")
            return False

    def eliminar_pregunta(self, pregunta_id: int) -> bool:
        """Elimina una pregunta específica"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute("DELETE FROM preguntas WHERE id = ?", (pregunta_id,))

            if cursor.rowcount > 0:
                conn.commit()
                conn.close()
                print(f"✅ Pregunta eliminada (ID: {pregunta_id})")
                return True
            else:
                conn.close()
                print(f"❌ No se encontró pregunta con ID: {pregunta_id}")
                return False

        except Exception as e:
            print(f"❌ Error eliminando pregunta: {e}")
            return False

    def obtener_pregunta_por_id(self, pregunta_id: int) -> dict:
        """Obtiene una pregunta específica por ID"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute('''
                           SELECT id, habilidad, pregunta, tipo, nivel, categoria, created_at
                           FROM preguntas
                           WHERE id = ?
                           ''', (pregunta_id,))

            resultado = cursor.fetchone()
            conn.close()

            if resultado:
                return {
                    'id': resultado[0],
                    'habilidad': resultado[1],
                    'pregunta': resultado[2],
                    'tipo': resultado[3],
                    'nivel': resultado[4],
                    'categoria': resultado[5],
                    'created_at': resultado[6]
                }
            else:
                return {}

        except Exception as e:
            print(f"❌ Error obteniendo pregunta por ID: {e}")
            return {}

    def obtener_estadisticas_generales(self) -> dict:
        """Obtiene estadísticas generales de toda la base de datos"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Total de preguntas
            cursor.execute("SELECT COUNT(*) FROM preguntas")
            total_preguntas = cursor.fetchone()[0]

            # Preguntas por nivel
            cursor.execute("SELECT nivel, COUNT(*) FROM preguntas GROUP BY nivel")
            por_nivel = dict(cursor.fetchall())

            # Preguntas por tipo
            cursor.execute("SELECT tipo, COUNT(*) FROM preguntas GROUP BY tipo")
            por_tipo = dict(cursor.fetchall())

            # Preguntas por categoría
            cursor.execute("SELECT categoria, COUNT(*) FROM preguntas GROUP BY categoria")
            por_categoria = dict(cursor.fetchall())

            # Top habilidades
            cursor.execute('''
                           SELECT habilidad, COUNT(*) as total
                           FROM preguntas
                           GROUP BY habilidad
                           ORDER BY total DESC LIMIT 5
                           ''')
            top_habilidades = cursor.fetchall()

            conn.close()

            return {
                'total_preguntas': total_preguntas,
                'por_nivel': por_nivel,
                'por_tipo': por_tipo,
                'por_categoria': por_categoria,
                'top_habilidades': top_habilidades,
                'archivo_bd': self.db_name
            }

        except Exception as e:
            print(f"❌ Error obteniendo estadísticas generales: {e}")
            return {}

    def cerrar_conexion(self):
        """Método para limpiar recursos si es necesario"""
        # SQLite se cierra automáticamente, pero podemos agregar logging aquí
        pass


# Función utilitaria para pruebas independientes
def test_database_manager():
    """Función para probar el DatabaseManager independientemente"""
    print("🧪 PRUEBAS DEL DATABASE MANAGER")
    print("=" * 40)

    # Crear instancia
    db = DatabaseManager("test_preguntas.db")

    # Agregar algunas preguntas de prueba
    test_preguntas = [
        ("Python", "¿Qué es una lista?", "conceptual", "basico"),
        ("Python", "¿Cómo implementas una función recursiva?", "practica", "avanzado"),
        ("JavaScript", "¿Qué es closure?", "conceptual", "intermedio"),
        ("React", "¿Cómo creas un Hook personalizado?", "practica", "avanzado")
    ]

    print("📝 Agregando preguntas de prueba...")
    for habilidad, pregunta, tipo, nivel in test_preguntas:
        db.agregar_pregunta(habilidad, pregunta, tipo, nivel)

    # Mostrar estadísticas
    print("\n📊 Estadísticas:")
    stats = db.obtener_estadisticas_generales()
    print(f"Total preguntas: {stats['total_preguntas']}")
    print(f"Por nivel: {stats['por_nivel']}")

    # Probar búsqueda
    print("\n🔍 Buscando 'Python':")
    resultados = db.buscar_preguntas("Python")
    for hab, pregunta, tipo, nivel in resultados:
        print(f"• {hab} ({nivel}): {pregunta}")

    # Obtener preguntas por habilidad
    print("\n🎯 Preguntas de Python:")
    preguntas_python = db.obtener_preguntas_por_habilidad("Python", cantidad=2)
    for i, pregunta in enumerate(preguntas_python, 1):
        print(f"  {i}. {pregunta}")

    print("\n✅ Pruebas completadas")


if __name__ == "__main__":
    # Ejecutar pruebas si se ejecuta directamente
    test_database_manager()