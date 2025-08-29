"""
Cargador de Datos Iniciales para Preguntas de Entrevista
Contiene todas las preguntas predefinidas y métodos para cargarlas
"""

from database_manager import DatabaseManager
import os
from datetime import datetime


class DataLoader:
    def __init__(self):
        self.preguntas_iniciales = self.get_preguntas_iniciales()

    def get_preguntas_iniciales(self) -> dict:
        """Retorna diccionario con todas las preguntas iniciales organizadas por habilidad"""
        return {
            "Python": {
                "basico": [
                    "¿Cuáles son los tipos de datos básicos en Python?",
                    "¿Qué es una lista en Python y cómo se diferencia de una tupla?",
                    "¿Cómo se manejan las cadenas de texto en Python?",
                    "¿Qué son las funciones lambda en Python?"
                ],
                "intermedio": [
                    "¿Cuáles son las diferencias entre listas y tuplas en Python?",
                    "Explica el concepto de decoradores en Python y da un ejemplo",
                    "¿Cómo manejas las excepciones en Python?",
                    "¿Qué son los generadores y cuándo los usarías?",
                    "Describe la diferencia entre métodos de clase y métodos estáticos"
                ],
                "avanzado": [
                    "¿Cómo funciona el GIL (Global Interpreter Lock) en Python?",
                    "Explica el concepto de metaclases en Python",
                    "¿Qué son los context managers y cómo implementarías uno?",
                    "¿Cómo optimizarías el rendimiento de una aplicación Python?"
                ]
            },

            "JavaScript": {
                "basico": [
                    "¿Cuáles son los tipos de datos primitivos en JavaScript?",
                    "¿Qué es una función en JavaScript?",
                    "¿Cómo funcionan los arrays en JavaScript?",
                    "¿Qué es el DOM y cómo interactúas con él?"
                ],
                "intermedio": [
                    "¿Cuál es la diferencia entre var, let y const?",
                    "Explica el concepto de closures en JavaScript",
                    "¿Cómo funciona el hoisting en JavaScript?",
                    "¿Qué es el Event Loop y cómo funciona?",
                    "Describe las diferencias entre == y === en JavaScript"
                ],
                "avanzado": [
                    "¿Cómo implementarías el patrón Observer en JavaScript?",
                    "Explica el concepto de currying y sus ventajas",
                    "¿Qué son los Web Workers y cuándo los usarías?",
                    "¿Cómo manejas la programación asíncrona con async/await?"
                ]
            },

            "React": {
                "basico": [
                    "¿Qué es React y cuáles son sus características principales?",
                    "¿Qué es JSX y por qué se usa en React?",
                    "¿Cómo creas un componente simple en React?",
                    "¿Qué son las props en React?"
                ],
                "intermedio": [
                    "¿Cuál es la diferencia entre componentes funcionales y de clase?",
                    "Explica cómo funciona el Virtual DOM",
                    "¿Qué son los Hooks y cuáles son los más comunes?",
                    "¿Cómo manejas el estado en una aplicación React compleja?",
                    "Explica el ciclo de vida de un componente React"
                ],
                "avanzado": [
                    "¿Cómo implementarías un Hook personalizado?",
                    "¿Qué es React Suspense y cómo se usa?",
                    "¿Cómo optimizarías el rendimiento de una aplicación React?",
                    "Explica el patrón de render props en React"
                ]
            },

            "SQL": {
                "basico": [
                    "¿Qué es SQL y para qué se utiliza?",
                    "¿Cuáles son los comandos básicos de SQL?",
                    "¿Qué es una tabla en una base de datos relacional?",
                    "¿Cómo realizas consultas básicas con SELECT?"
                ],
                "intermedio": [
                    "¿Cuál es la diferencia entre INNER JOIN y LEFT JOIN?",
                    "¿Qué son las transacciones y cuáles son sus propiedades ACID?",
                    "Explica la diferencia entre índices clustered y non-clustered",
                    "¿Cómo optimizarías una consulta SQL lenta?",
                    "¿Qué es la normalización de bases de datos?"
                ],
                "avanzado": [
                    "¿Cómo implementarías procedimientos almacenados complejos?",
                    "¿Qué son las funciones de ventana (window functions) en SQL?",
                    "¿Cómo manejas la concurrencia en bases de datos?",
                    "Explica las estrategias de particionamiento de tablas"
                ]
            },

            "Java": {
                "basico": [
                    "¿Qué es Java y cuáles son sus características principales?",
                    "¿Cuál es la diferencia entre JDK, JRE y JVM?",
                    "¿Qué son las clases y objetos en Java?",
                    "¿Cómo funciona la herencia en Java?"
                ],
                "intermedio": [
                    "¿Cuál es la diferencia entre abstract class e interface?",
                    "Explica el concepto de polimorfismo en Java",
                    "¿Qué son las Collections y cuáles son las más importantes?",
                    "¿Cómo funciona el Garbage Collector en Java?",
                    "Explica la diferencia entre String, StringBuilder y StringBuffer"
                ],
                "avanzado": [
                    "¿Cómo implementarías un patrón Singleton thread-safe?",
                    "¿Qué son las anotaciones en Java y cómo crearías una personalizada?",
                    "¿Cómo funciona la programación concurrente con ExecutorService?",
                    "Explica el concepto de generics y wildcards en Java"
                ]
            },

            "Docker": {
                "basico": [
                    "¿Qué es Docker y qué problema resuelve?",
                    "¿Cuál es la diferencia entre virtualización y containerización?",
                    "¿Qué son los contenedores Docker?",
                    "¿Cómo ejecutas tu primer contenedor Docker?"
                ],
                "intermedio": [
                    "¿Cuál es la diferencia entre una imagen y un contenedor?",
                    "¿Qué es un Dockerfile y cuáles son sus principales instrucciones?",
                    "Explica qué son los volumes en Docker",
                    "¿Cómo manejas las variables de entorno en Docker?",
                    "¿Qué es Docker Compose y cuándo lo usarías?"
                ],
                "avanzado": [
                    "¿Cómo implementarías una estrategia de multi-stage builds?",
                    "¿Cómo optimizarías el tamaño de las imágenes Docker?",
                    "¿Qué son los health checks y cómo los implementas?",
                    "¿Cómo manejas secretos en Docker de forma segura?"
                ]
            },

            "Git": {
                "basico": [
                    "¿Qué es Git y para qué se utiliza?",
                    "¿Cuáles son los comandos básicos de Git?",
                    "¿Qué es un repositorio Git?",
                    "¿Cómo haces tu primer commit?"
                ],
                "intermedio": [
                    "¿Cuál es la diferencia entre merge y rebase?",
                    "¿Cómo resuelves conflictos en Git?",
                    "Explica qué son las ramas (branches) y cómo las usas",
                    "¿Qué comandos usas para deshacer cambios en Git?",
                    "¿Cómo manejas un repositorio con múltiples colaboradores?"
                ],
                "avanzado": [
                    "¿Cuándo y cómo usarías git cherry-pick?",
                    "¿Qué es git bisect y cómo lo usarías para debugging?",
                    "¿Cómo implementarías una estrategia de branching como GitFlow?",
                    "¿Cómo manejas releases y tags en proyectos grandes?"
                ]
            },

            "Node.js": {
                "basico": [
                    "¿Qué es Node.js y cuáles son sus características?",
                    "¿Cuál es la diferencia entre Node.js y JavaScript del navegador?",
                    "¿Qué es npm y cómo lo usas?",
                    "¿Cómo creas un servidor HTTP básico en Node.js?"
                ],
                "intermedio": [
                    "¿Qué es el Event Loop en Node.js?",
                    "¿Cuál es la diferencia entre require() e import?",
                    "Explica qué son los middlewares en Express",
                    "¿Cómo manejas operaciones asíncronas en Node.js?",
                    "¿Cómo gestionas las dependencias con package.json?"
                ],
                "avanzado": [
                    "¿Cómo implementarías clustering en Node.js?",
                    "¿Qué son los streams en Node.js y cómo los usas?",
                    "¿Cómo manejas el debugging y profiling en aplicaciones Node.js?",
                    "¿Qué estrategias usas para el manejo de errores en aplicaciones Node.js?"
                ]
            },

            "Angular": {
                "basico": [
                    "¿Qué es Angular y cuáles son sus características principales?",
                    "¿Qué es TypeScript y por qué Angular lo usa?",
                    "¿Cómo creas un componente en Angular?",
                    "¿Qué son los servicios en Angular?"
                ],
                "intermedio": [
                    "¿Cómo funciona la inyección de dependencias en Angular?",
                    "¿Qué son los observables y cómo se usan en Angular?",
                    "¿Cómo implementas routing en una aplicación Angular?",
                    "¿Qué son las directivas y cómo creas una personalizada?",
                    "¿Cómo manejas formularios reactivos en Angular?"
                ],
                "avanzado": [
                    "¿Cómo implementas lazy loading en Angular?",
                    "¿Qué son los guards y cuándo los usarías?",
                    "¿Cómo optimizas el rendimiento de una aplicación Angular?",
                    "¿Cómo implementas testing unitario e integración en Angular?"
                ]
            },

            "AWS": {
                "basico": [
                    "¿Qué es AWS y cuáles son sus servicios principales?",
                    "¿Qué es EC2 y para qué se utiliza?",
                    "¿Qué es S3 y cuáles son sus casos de uso?",
                    "¿Qué son las regiones y zonas de disponibilidad en AWS?"
                ],
                "intermedio": [
                    "¿Cuál es la diferencia entre ELB y Auto Scaling?",
                    "¿Qué es Lambda y cuándo usarías funciones serverless?",
                    "¿Cómo implementas una VPC en AWS?",
                    "¿Qué es RDS y cómo configurarías una base de datos?",
                    "¿Cómo manejas la seguridad con IAM en AWS?"
                ],
                "avanzado": [
                    "¿Cómo diseñarías una arquitectura de microservicios en AWS?",
                    "¿Cómo implementas CI/CD con AWS CodePipeline?",
                    "¿Qué estrategias usas para optimizar costos en AWS?",
                    "¿Cómo implementas monitoring y logging con CloudWatch?"
                ]
            },

            "CSS": {
                "basico": [
                    "¿Qué es CSS y para qué se utiliza?",
                    "¿Cuáles son los selectores básicos de CSS?",
                    "¿Qué es el modelo de caja (box model) en CSS?",
                    "¿Cómo aplicas estilos en línea, internos y externos?"
                ],
                "intermedio": [
                    "¿Cuál es la diferencia entre margin y padding?",
                    "¿Qué son los pseudo-elementos y pseudo-clases?",
                    "¿Cómo funciona el sistema de layout con Flexbox?",
                    "¿Qué es CSS Grid y cuándo lo usarías?",
                    "¿Cómo manejas la responsividad con media queries?"
                ],
                "avanzado": [
                    "¿Cómo implementas animaciones complejas con CSS?",
                    "¿Qué son las variables CSS y cómo las usas?",
                    "¿Cómo optimizas el rendimiento de CSS en aplicaciones grandes?",
                    "¿Qué metodologías usas para organizar CSS (BEM, SMACSS)?"
                ]
            },

            "MongoDB": {
                "basico": [
                    "¿Qué es MongoDB y cuáles son sus características?",
                    "¿Cuál es la diferencia entre bases de datos relacionales y NoSQL?",
                    "¿Qué son los documentos y colecciones en MongoDB?",
                    "¿Cómo insertas y consultas documentos básicos?"
                ],
                "intermedio": [
                    "¿Cómo realizas consultas complejas con agregaciones?",
                    "¿Qué son los índices en MongoDB y cómo los creas?",
                    "¿Cómo manejas las relaciones entre documentos?",
                    "¿Qué es el sharding y cuándo lo implementarías?",
                    "¿Cómo realizas operaciones de actualización complejas?"
                ],
                "avanzado": [
                    "¿Cómo implementas replicación en MongoDB?",
                    "¿Qué estrategias usas para optimizar consultas?",
                    "¿Cómo manejas transacciones en MongoDB?",
                    "¿Cómo implementas seguridad y autenticación en MongoDB?"
                ]
            }
        }

    def cargar_datos_iniciales(self, db_manager: DatabaseManager, forzar_recarga: bool = False) -> bool:
        """Carga las preguntas iniciales en la base de datos"""
        try:
            # Verificar si ya hay datos
            if db_manager.contar_preguntas() > 0 and not forzar_recarga:
                print("📚 La base de datos ya contiene preguntas")
                return True

            if forzar_recarga:
                print("🔄 Forzando recarga de datos...")
                db_manager.limpiar_base_datos()

            print("📝 Cargando preguntas iniciales en la base de datos...")
            total_cargadas = 0

            for habilidad, niveles in self.preguntas_iniciales.items():
                print(f"  🔄 Cargando {habilidad}...")

                for nivel, preguntas in niveles.items():
                    for pregunta in preguntas:
                        if db_manager.agregar_pregunta(
                                habilidad=habilidad,
                                pregunta=pregunta,
                                tipo="conceptual" if "concepto" in pregunta.lower() else "practica",
                                nivel=nivel,
                                categoria="tecnica"
                        ):
                            total_cargadas += 1

                print(f"  ✅ {habilidad}: {sum(len(p) for p in niveles.values())} preguntas")

            print(f"✅ Carga completada: {total_cargadas} preguntas cargadas")
            return True

        except Exception as e:
            print(f"❌ Error cargando datos iniciales: {e}")
            return False

    def generar_archivo_sql(self, archivo_salida: str = "preguntas_iniciales.sql") -> bool:
        """Genera un archivo SQL con todas las preguntas iniciales"""
        try:
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                # Header del archivo
                f.write("-- Preguntas Iniciales para Entrevistas Técnicas\n")
                f.write("-- Generado automáticamente por DataLoader\n")
                f.write("-- Fecha: " + str(datetime.now()) + "\n\n")

                # Crear tabla
                f.write("""
                        -- Crear tabla de preguntas
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
                        );

-- Crear índices
                        CREATE INDEX IF NOT EXISTS idx_habilidad ON preguntas(habilidad);
                        CREATE INDEX IF NOT EXISTS idx_tipo_nivel ON preguntas(tipo, nivel);

                        -- Limpiar datos existentes (opcional)
-- DELETE FROM preguntas;

-- Insertar preguntas
                        """)

                # Insertar preguntas
                for habilidad, niveles in self.preguntas_iniciales.items():
                    f.write(f"\n-- {habilidad} --\n")

                    for nivel, preguntas in niveles.items():
                        for pregunta in preguntas:
                            tipo = "conceptual" if "concepto" in pregunta.lower() else "practica"
                            f.write(
                                f"INSERT INTO preguntas (habilidad, pregunta, tipo, nivel, categoria) VALUES ('{habilidad}', '{pregunta.replace("'", "''")}', '{tipo}', '{nivel}', 'tecnica');\n")

                f.write(
                    f"\n-- Total de preguntas: {sum(len(p) for niveles in self.preguntas_iniciales.values() for p in niveles.values())}\n")

            print(f"✅ Archivo SQL generado: {archivo_salida}")
            return True

        except Exception as e:
            print(f"❌ Error generando archivo SQL: {e}")
            return False

    def obtener_estadisticas_datos(self) -> dict:
        """Obtiene estadísticas de los datos iniciales"""
        total_preguntas = 0
        estadisticas = {}

        for habilidad, niveles in self.preguntas_iniciales.items():
            total_habilidad = sum(len(preguntas) for preguntas in niveles.values())
            estadisticas[habilidad] = {
                'total': total_habilidad,
                'por_nivel': {nivel: len(preguntas) for nivel, preguntas in niveles.items()}
            }
            total_preguntas += total_habilidad

        return {
            'total_preguntas': total_preguntas,
            'total_habilidades': len(self.preguntas_iniciales),
            'estadisticas_por_habilidad': estadisticas
        }

    def agregar_habilidad_personalizada(self, habilidad: str, preguntas_por_nivel: dict) -> bool:
        """Permite agregar una habilidad personalizada con sus preguntas"""
        try:
            if habilidad in self.preguntas_iniciales:
                print(f"⚠️ La habilidad '{habilidad}' ya existe")
                return False

            # Validar estructura
            niveles_validos = ['basico', 'intermedio', 'avanzado']
            for nivel in preguntas_por_nivel.keys():
                if nivel not in niveles_validos:
                    print(f"❌ Nivel inválido: {nivel}. Use: {niveles_validos}")
                    return False

            self.preguntas_iniciales[habilidad] = preguntas_por_nivel
            print(
                f"✅ Habilidad '{habilidad}' agregada con {sum(len(p) for p in preguntas_por_nivel.values())} preguntas")
            return True

        except Exception as e:
            print(f"❌ Error agregando habilidad personalizada: {e}")
            return False

    def exportar_preguntas_json(self, archivo_salida: str = "preguntas_backup.json") -> bool:
        """Exporta todas las preguntas a formato JSON"""
        try:
            import json

            data = {
                "metadata": {
                    "generado": datetime.now().isoformat(),
                    "total_habilidades": len(self.preguntas_iniciales),
                    "total_preguntas": sum(
                        len(p) for niveles in self.preguntas_iniciales.values() for p in niveles.values()),
                    "version": "1.0"
                },
                "preguntas": self.preguntas_iniciales
            }

            with open(archivo_salida, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"✅ Preguntas exportadas a JSON: {archivo_salida}")
            return True

        except Exception as e:
            print(f"❌ Error exportando a JSON: {e}")
            return False

    def importar_preguntas_json(self, archivo_entrada: str) -> bool:
        """Importa preguntas desde un archivo JSON"""
        try:
            import json

            if not os.path.exists(archivo_entrada):
                print(f"❌ Archivo no encontrado: {archivo_entrada}")
                return False

            with open(archivo_entrada, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if 'preguntas' in data:
                self.preguntas_iniciales.update(data['preguntas'])
                print(f"✅ Preguntas importadas desde: {archivo_entrada}")
                return True
            else:
                print("❌ Formato de archivo JSON inválido")
                return False

        except Exception as e:
            print(f"❌ Error importando desde JSON: {e}")
            return False

    def validar_integridad_datos(self) -> dict:
        """Valida la integridad de los datos cargados"""
        try:
            resultados = {
                'errores': [],
                'advertencias': [],
                'estadisticas': {}
            }

            niveles_validos = ['basico', 'intermedio', 'avanzado']

            for habilidad, niveles in self.preguntas_iniciales.items():
                # Validar que la habilidad no esté vacía
                if not habilidad or not habilidad.strip():
                    resultados['errores'].append("Habilidad vacía encontrada")

                # Validar niveles
                for nivel, preguntas in niveles.items():
                    if nivel not in niveles_validos:
                        resultados['errores'].append(f"Nivel inválido en {habilidad}: {nivel}")

                    # Validar preguntas
                    if not preguntas or len(preguntas) == 0:
                        resultados['advertencias'].append(f"{habilidad}-{nivel}: No tiene preguntas")

                    for i, pregunta in enumerate(preguntas):
                        if not pregunta or not pregunta.strip():
                            resultados['errores'].append(f"{habilidad}-{nivel}: Pregunta {i + 1} vacía")
                        elif len(pregunta) < 10:
                            resultados['advertencias'].append(f"{habilidad}-{nivel}: Pregunta {i + 1} muy corta")
                        elif not pregunta.endswith('?'):
                            resultados['advertencias'].append(
                                f"{habilidad}-{nivel}: Pregunta {i + 1} no termina con '?'")

            # Estadísticas generales
            resultados['estadisticas'] = self.obtener_estadisticas_datos()

            return resultados

        except Exception as e:
            return {'errores': [f"Error validando datos: {e}"], 'advertencias': [], 'estadisticas': {}}

    def mostrar_resumen_contenido(self):
        """Muestra un resumen del contenido disponible"""
        print("\n📚 RESUMEN DE CONTENIDO DISPONIBLE")
        print("=" * 50)

        stats = self.obtener_estadisticas_datos()
        print(f"📊 Total: {stats['total_preguntas']} preguntas en {stats['total_habilidades']} habilidades")

        print(f"\n🎯 HABILIDADES DISPONIBLES:")
        print("-" * 30)

        for habilidad, data in stats['estadisticas_por_habilidad'].items():
            print(f"\n{habilidad}: {data['total']} preguntas")
            niveles_info = []
            for nivel, count in data['por_nivel'].items():
                niveles_info.append(f"{nivel}: {count}")
            print(f"  └── {' | '.join(niveles_info)}")


# Función utilitaria para uso independiente
def inicializar_base_datos_completa(db_path: str = "preguntas_entrevista.db", forzar_recarga: bool = False):
    """Función utilitaria para inicializar completamente la base de datos"""
    try:
        print("🚀 Inicializando base de datos completa...")

        # Crear gestor de BD
        db_manager = DatabaseManager(db_path)

        # Crear cargador de datos
        data_loader = DataLoader()

        # Cargar datos iniciales
        if data_loader.cargar_datos_iniciales(db_manager, forzar_recarga):
            print("✅ Base de datos inicializada correctamente")

            # Mostrar estadísticas
            resumen = db_manager.obtener_resumen_completo()
            print(f"📊 Total de preguntas: {resumen['total_preguntas']}")
            print(f"📊 Total de habilidades: {resumen['total_habilidades']}")

            return True
        else:
            print("❌ Error inicializando base de datos")
            return False

    except Exception as e:
        print(f"❌ Error en inicialización completa: {e}")
        return False


if __name__ == "__main__":
    # Permitir ejecutar este archivo directamente para inicializar la BD
    print("🎯 EJECUTANDO DATA LOADER INDEPENDIENTE")
    print("=" * 50)

    # Opciones disponibles
    print("1. Inicializar base de datos con preguntas")
    print("2. Generar archivo SQL")
    print("3. Ver estadísticas de datos")
    print("4. Exportar a JSON")
    print("5. Validar integridad de datos")
    print("6. Mostrar resumen de contenido")
    print("7. Salir")

    opcion = input("\nSelecciona una opción (1-7): ").strip()

    data_loader = DataLoader()

    if opcion == "1":
        inicializar_base_datos_completa(forzar_recarga=True)

    elif opcion == "2":
        if data_loader.generar_archivo_sql():
            print("✅ Archivo SQL generado exitosamente")

    elif opcion == "3":
        stats = data_loader.obtener_estadisticas_datos()
        print("\n📊 ESTADÍSTICAS DE DATOS INICIALES:")
        print("=" * 40)
        print(f"Total de preguntas: {stats['total_preguntas']}")
        print(f"Total de habilidades: {stats['total_habilidades']}")
        print("\nPor habilidad:")
        for hab, data in stats['estadisticas_por_habilidad'].items():
            print(f"  {hab}: {data['total']} preguntas")
            for nivel, count in data['por_nivel'].items():
                print(f"    - {nivel}: {count}")

    elif opcion == "4":
        if data_loader.exportar_preguntas_json():
            print("✅ Archivo JSON generado exitosamente")

    elif opcion == "5":
        resultados = data_loader.validar_integridad_datos()
        print("\n🔍 VALIDACIÓN DE INTEGRIDAD:")
        print("=" * 35)

        if resultados['errores']:
            print(f"❌ Errores encontrados: {len(resultados['errores'])}")
            for error in resultados['errores'][:5]:  # Mostrar máximo 5
                print(f"  • {error}")
        else:
            print("✅ No se encontraron errores")

        if resultados['advertencias']:
            print(f"\n⚠️ Advertencias: {len(resultados['advertencias'])}")
            for advertencia in resultados['advertencias'][:5]:  # Mostrar máximo 5
                print(f"  • {advertencia}")

    elif opcion == "6":
        data_loader.mostrar_resumen_contenido()

    elif opcion == "7":
        print("👋 ¡Adiós!")

    else:
        print("⚠️ Opción no válida")