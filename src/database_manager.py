"""
Gestor de Base de Datos para Preguntas de Entrevista
Maneja operaciones tanto en SQLite como PostgreSQL de forma desacoplada
"""

import sqlite3
import os
from typing import List, Optional, Tuple
from config import DatabaseConfig

# Importar psycopg2 solo si se usa PostgreSQL
if DatabaseConfig.is_postgresql():
    try:
        import psycopg2
        from psycopg2.extras import DictCursor
        from psycopg2 import sql
        POSTGRES_AVAILABLE = True
    except ImportError:
        print("❌ psycopg2 no instalado. Instala con: pip install psycopg2-binary")
        POSTGRES_AVAILABLE = False
else:
    POSTGRES_AVAILABLE = False


class DatabaseManager:
    def __init__(self, db_name: str = None):
        """
        Inicializa el gestor de base de datos
        db_name: nombre del archivo SQLite (ignorado si se usa PostgreSQL)
        """
        self.db_type = DatabaseConfig.DATABASE_TYPE.lower()

        if self.db_type == 'postgresql':
            if not POSTGRES_AVAILABLE:
                raise Exception("PostgreSQL configurado pero psycopg2 no disponible")
            self.connection_params = DatabaseConfig.get_postgres_connection_params()
            print(f"🗄️ Configurado para PostgreSQL: {self.connection_params['host']}:{self.connection_params['port']}")
        else:
            # Modo SQLite (legacy)
            self.db_name = db_name or DatabaseConfig.SQLITE_PATH
            print(f"🗄️ Configurado para SQLite: {self.db_name}")

        self.init_database()

    def get_connection(self):
        """Obtiene conexión según el tipo de base de datos"""
        if self.db_type == 'postgresql':
            return psycopg2.connect(**self.connection_params)
        else:
            return sqlite3.connect(self.db_name)

    def init_database(self):
        """Inicializa la base de datos y crea las tablas necesarias"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            if self.db_type == 'postgresql':
                # PostgreSQL con SERIAL para auto-increment
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS preguntas (
                        id SERIAL PRIMARY KEY,
                        habilidad VARCHAR(100) NOT NULL,
                        pregunta TEXT NOT NULL,
                        tipo VARCHAR(50) DEFAULT 'general',
                        nivel VARCHAR(50) DEFAULT 'intermedio',
                        categoria VARCHAR(50) DEFAULT 'tecnica',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        CONSTRAINT unique_pregunta UNIQUE(habilidad, pregunta)
                    )
                ''')

                # Crear índices optimizados para PostgreSQL
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_habilidad ON preguntas(habilidad)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_tipo_nivel ON preguntas(tipo, nivel)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_nivel ON preguntas(nivel)')

                # Índice de texto completo para PostgreSQL
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_full_search 
                    ON preguntas USING gin(to_tsvector('spanish', pregunta))
                ''')

            else:
                # SQLite (código original)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS preguntas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        habilidad TEXT NOT NULL,
                        pregunta TEXT NOT NULL,
                        tipo TEXT DEFAULT 'general',
                        nivel TEXT DEFAULT 'intermedio',
                        categoria TEXT DEFAULT 'tecnica',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                cursor.execute('CREATE INDEX IF NOT EXISTS idx_habilidad ON preguntas(habilidad)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_tipo_nivel ON preguntas(tipo, nivel)')

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"❌ Error inicializando base de datos: {e}")
            return False

    def agregar_pregunta(self, habilidad: str, pregunta: str,
                         tipo: str = "general", nivel: str = "intermedio",
                         categoria: str = "tecnica") -> bool:
        """Agrega una nueva pregunta a la base de datos"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            if self.db_type == 'postgresql':
                # PostgreSQL con ON CONFLICT para evitar duplicados
                cursor.execute('''
                    INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (habilidad, pregunta) DO NOTHING
                ''', (habilidad, pregunta, tipo, nivel, categoria))
            else:
                # SQLite (código original)
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
            conn = self.get_connection()
            cursor = conn.cursor()

            if self.db_type == 'postgresql':
                if nivel:
                    cursor.execute('''
                        SELECT pregunta
                        FROM preguntas
                        WHERE habilidad ILIKE %s AND nivel = %s
                        ORDER BY RANDOM() LIMIT %s
                    ''', (f'%{habilidad}%', nivel, cantidad))
                else:
                    cursor.execute('''
                        SELECT pregunta
                        FROM preguntas
                        WHERE habilidad ILIKE %s
                        ORDER BY RANDOM() LIMIT %s
                    ''', (f'%{habilidad}%', cantidad))
            else:
                # SQLite (código original)
                if nivel:
                    cursor.execute('''
                        SELECT pregunta
                        FROM preguntas
                        WHERE habilidad LIKE ? AND nivel = ?
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
            conn = self.get_connection()
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
            conn = self.get_connection()
            cursor = conn.cursor()

            placeholder = '%s' if self.db_type == 'postgresql' else '?'

            # Contar total
            cursor.execute(f'''
                SELECT COUNT(*)
                FROM preguntas
                WHERE habilidad = {placeholder}
            ''', (habilidad,))
            total = cursor.fetchone()[0]

            # Contar por nivel
            cursor.execute(f'''
                SELECT nivel, COUNT(*)
                FROM preguntas
                WHERE habilidad = {placeholder}
                GROUP BY nivel
            ''', (habilidad,))
            niveles = dict(cursor.fetchall())

            # Contar por tipo
            cursor.execute(f'''
                SELECT tipo, COUNT(*)
                FROM preguntas
                WHERE habilidad = {placeholder}
                GROUP BY tipo
            ''', (habilidad,))
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
            conn = self.get_connection()
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
            conn = self.get_connection()
            cursor = conn.cursor()

            placeholder = '%s' if self.db_type == 'postgresql' else '?'
            like_operator = 'ILIKE' if self.db_type == 'postgresql' else 'LIKE'

            cursor.execute(f'''
                SELECT COUNT(*)
                FROM preguntas
                WHERE habilidad {like_operator} {placeholder}
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
            conn = self.get_connection()
            cursor = conn.cursor()

            placeholder = '%s' if self.db_type == 'postgresql' else '?'
            like_operator = 'ILIKE' if self.db_type == 'postgresql' else 'LIKE'

            if self.db_type == 'postgresql':
                # Usar búsqueda de texto completo en PostgreSQL si está disponible
                cursor.execute(f'''
                    SELECT habilidad, pregunta, tipo, nivel
                    FROM preguntas
                    WHERE pregunta {like_operator} {placeholder}
                       OR habilidad {like_operator} {placeholder}
                    ORDER BY habilidad, pregunta LIMIT {placeholder}
                ''', (f'%{termino}%', f'%{termino}%', limit))
            else:
                cursor.execute(f'''
                    SELECT habilidad, pregunta, tipo, nivel
                    FROM preguntas
                    WHERE pregunta {like_operator} {placeholder}
                       OR habilidad {like_operator} {placeholder}
                    ORDER BY habilidad, pregunta LIMIT {placeholder}
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

            db_info = f"{self.db_type.upper()}"
            if self.db_type == 'postgresql':
                db_info += f" ({self.connection_params['host']}:{self.connection_params['port']}/{self.connection_params['database']})"
            else:
                db_info += f" ({self.db_name})"

            return {
                'total_preguntas': total_preguntas,
                'total_habilidades': len(habilidades),
                'habilidades': habilidades,
                'estadisticas': estadisticas_por_habilidad,
                'archivo_bd': db_info
            }

        except Exception as e:
            print(f"❌ Error obteniendo resumen: {e}")
            return {}

    def exportar_bd_a_sql(self, archivo_salida: str = "backup_preguntas.sql") -> bool:
        """Exporta toda la base de datos a un archivo SQL"""
        try:
            conn = self.get_connection()

            if self.db_type == 'postgresql':
                # Para PostgreSQL, hacer export manual
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT habilidad, pregunta, tipo, nivel, categoria, created_at
                    FROM preguntas ORDER BY id
                ''')
                registros = cursor.fetchall()

                with open(archivo_salida, 'w', encoding='utf-8') as f:
                    f.write("-- Backup PostgreSQL generado por DatabaseManager\n")
                    f.write(f"-- Base de datos: {self.connection_params['database']}\n")
                    f.write(f"-- Total registros: {len(registros)}\n\n")

                    for registro in registros:
                        habilidad, pregunta, tipo, nivel, categoria, created_at = registro
                        f.write(f"INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria, created_at) VALUES (")
                        f.write(f"'{habilidad}', '{pregunta.replace("'", "''")}', '{tipo}', '{nivel}', '{categoria}', '{created_at}');\n")
            else:
                # SQLite dump (código original)
                with open(archivo_salida, 'w', encoding='utf-8') as f:
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
            conn = self.get_connection()
            cursor = conn.cursor()

            if self.db_type == 'postgresql':
                cursor.execute('TRUNCATE TABLE preguntas RESTART IDENTITY CASCADE')
            else:
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
            conn = self.get_connection()
            cursor = conn.cursor()
            preguntas_resultado = {}

            if not habilidades:
                habilidades = self.obtener_todas_habilidades()

            placeholder = '%s' if self.db_type == 'postgresql' else '?'
            like_operator = 'ILIKE' if self.db_type == 'postgresql' else 'LIKE'

            for habilidad in habilidades:
                query = f"SELECT pregunta FROM preguntas WHERE habilidad = {placeholder}"
                params = [habilidad]

                if nivel:
                    query += f" AND nivel = {placeholder}"
                    params.append(nivel)

                if tipo:
                    query += f" AND tipo = {placeholder}"
                    params.append(tipo)

                query += f" ORDER BY RANDOM() LIMIT {placeholder}"
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
            conn = self.get_connection()
            cursor = conn.cursor()

            updates = []
            params = []
            placeholder = '%s' if self.db_type == 'postgresql' else '?'

            if nueva_pregunta:
                updates.append(f"pregunta = {placeholder}")
                params.append(nueva_pregunta)

            if nuevo_nivel:
                updates.append(f"nivel = {placeholder}")
                params.append(nuevo_nivel)

            if nuevo_tipo:
                updates.append(f"tipo = {placeholder}")
                params.append(nuevo_tipo)

            if not updates:
                print("⚠️ No hay cambios para actualizar")
                return False

            query = f"UPDATE preguntas SET {', '.join(updates)} WHERE id = {placeholder}"
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
            conn = self.get_connection()
            cursor = conn.cursor()

            placeholder = '%s' if self.db_type == 'postgresql' else '?'
            cursor.execute(f"DELETE FROM preguntas WHERE id = {placeholder}", (pregunta_id,))

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
            conn = self.get_connection()
            cursor = conn.cursor()

            placeholder = '%s' if self.db_type == 'postgresql' else '?'
            cursor.execute(f'''
                SELECT id, habilidad, pregunta, tipo, nivel, categoria, created_at
                FROM preguntas
                WHERE id = {placeholder}
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
            conn = self.get_connection()
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

            db_info = f"{self.db_type.upper()}"
            if self.db_type == 'postgresql':
                db_info += f" ({self.connection_params['database']})"
            else:
                db_info += f" ({self.db_name})"

            return {
                'total_preguntas': total_preguntas,
                'por_nivel': por_nivel,
                'por_tipo': por_tipo,
                'por_categoria': por_categoria,
                'top_habilidades': top_habilidades,
                'archivo_bd': db_info
            }

        except Exception as e:
            print(f"❌ Error obteniendo estadísticas generales: {e}")
            return {}

    def test_connection(self) -> bool:
        """Prueba la conexión a la base de datos"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            if self.db_type == 'postgresql':
                cursor.execute('SELECT version()')
                version = cursor.fetchone()[0]
                print(f"✅ Conexión PostgreSQL exitosa: {version}")
            else:
                cursor.execute('SELECT sqlite_version()')
                version = cursor.fetchone()[0]
                print(f"✅ Conexión SQLite exitosa: {version}")

            conn.close()
            return True

        except Exception as e:
            print(f"❌ Error conectando a la base de datos: {e}")
            return False

    def cerrar_conexion(self):
        """Método para limpiar recursos si es necesario"""
        pass


# Función utilitaria para pruebas independientes
def test_database_manager():
    """Función para probar el DatabaseManager independientemente"""
    print("🧪 PRUEBAS DEL DATABASE MANAGER")
    print("=" * 40)

    # Crear instancia
    db = DatabaseManager()

    # Probar conexión
    if not db.test_connection():
        print("❌ No se pudo establecer conexión")
        return

    # Mostrar estadísticas
    print("\n📊 Estadísticas:")
    stats = db.obtener_estadisticas_generales()
    print(f"Total preguntas: {stats['total_preguntas']}")
    print(f"Por nivel: {stats['por_nivel']}")
    print(f"Tipo de BD: {stats['archivo_bd']}")

    # Probar búsqueda
    print("\n🔍 Buscando 'Python':")
    resultados = db.buscar_preguntas("Python", limit=3)
    for hab, pregunta, tipo, nivel in resultados[:3]:
        print(f"• {hab} ({nivel}): {pregunta[:50]}...")

    print("\n✅ Pruebas completadas")


if __name__ == "__main__":
    # Ejecutar pruebas si se ejecuta directamente
    test_database_manager()