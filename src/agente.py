"""
Agente Entrevistador con Arquitectura Desacoplada
Utiliza DatabaseManager y DataLoader para manejo de datos
"""

print("🎯 Agente Entrevistador - Arquitectura Desacoplada")
print("=" * 60)

import time
import os
from typing import List, Dict

# Importar módulos desacoplados
try:
    from database_manager import DatabaseManager
    from data_loader import DataLoader, inicializar_base_datos_completa

    print("✅ Módulos de datos importados correctamente")
    MODULOS_DISPONIBLES = True
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("💡 Asegúrate de tener los archivos database_manager.py y data_loader.py")
    MODULOS_DISPONIBLES = False


class AgenteEntrevistador:
    def __init__(self, db_path: str = "preguntas_entrevista.db"):
        print("🤖 Inicializando Agente Entrevistador...")

        if not MODULOS_DISPONIBLES:
            print("❌ No se pueden cargar los módulos necesarios")
            return

        self.db_manager = DatabaseManager(db_path)
        self.data_loader = DataLoader()
        self.habilidades_seleccionadas = []
        self.preguntas_generadas = {}

        # Inicializar datos si es necesario
        self.inicializar_datos_si_necesario()

    def inicializar_datos_si_necesario(self):
        """Inicializa la base de datos con datos si está vacía"""
        total_preguntas = self.db_manager.contar_preguntas()

        if total_preguntas == 0:
            print("📝 Base de datos vacía. Cargando preguntas iniciales...")
            if self.data_loader.cargar_datos_iniciales(self.db_manager):
                print("✅ Preguntas iniciales cargadas correctamente")
            else:
                print("❌ Error cargando preguntas iniciales")
        else:
            print(f"📚 Base de datos lista con {total_preguntas} preguntas")

    def mostrar_habilidades_disponibles(self) -> List[str]:
        """Muestra todas las habilidades disponibles en la base de datos"""
        habilidades = self.db_manager.obtener_todas_habilidades()

        if not habilidades:
            print("❌ No hay habilidades disponibles en la base de datos")
            return []

        print("\n📚 HABILIDADES DISPONIBLES EN LA BASE DE DATOS:")
        print("=" * 55)

        # Organizar en columnas para mejor visualización
        for i, habilidad in enumerate(habilidades, 1):
            total_preguntas = self.db_manager.contar_preguntas_por_habilidad(habilidad)
            estadisticas = self.db_manager.obtener_estadisticas_habilidad(habilidad)

            niveles_info = ", ".join(
                [f"{nivel}: {count}" for nivel, count in estadisticas.get('por_nivel', {}).items()])

            print(f"{i:2d}. {habilidad:<12} ({total_preguntas} preguntas)")
            if niveles_info:
                print(f"    └── Niveles: {niveles_info}")

        return habilidades

    def seleccionar_habilidades(self) -> bool:
        """Permite al usuario seleccionar habilidades con opciones avanzadas"""
        habilidades_disponibles = self.mostrar_habilidades_disponibles()

        if not habilidades_disponibles:
            return False

        print("\n📋 SELECCIÓN DE HABILIDADES")
        print("=" * 50)
        print("Opciones de selección:")
        print("• Números: 1,3,5 (habilidades específicas)")
        print("• Nombres: Python,Java,React (por nombre)")
        print("• Rango: 1-5 (del 1 al 5)")
        print("• Nivel: nivel:basico (filtrar por nivel)")
        print("• Todas: 'todas' (seleccionar todas)")
        print("• Aleatorio: aleatorio:5 (5 habilidades al azar)")
        print("-" * 50)

        while True:
            try:
                seleccion = input("\nTu selección: ").strip()

                if seleccion.lower() == 'todas':
                    self.habilidades_seleccionadas = habilidades_disponibles.copy()
                    break

                elif seleccion.startswith('aleatorio:'):
                    try:
                        import random
                        cantidad = int(seleccion.split(':')[1])
                        cantidad = min(cantidad, len(habilidades_disponibles))
                        self.habilidades_seleccionadas = random.sample(habilidades_disponibles, cantidad)
                        break
                    except (ValueError, IndexError):
                        print("❌ Formato inválido. Usa: aleatorio:5")
                        continue

                elif seleccion.startswith('nivel:'):
                    nivel = seleccion.split(':')[1].lower()
                    self.habilidades_seleccionadas = []
                    for hab in habilidades_disponibles:
                        # Verificar si la habilidad tiene preguntas del nivel solicitado
                        stats = self.db_manager.obtener_estadisticas_habilidad(hab)
                        if nivel in stats.get('por_nivel', {}):
                            self.habilidades_seleccionadas.append(hab)

                    if self.habilidades_seleccionadas:
                        break
                    else:
                        print(f"❌ No se encontraron habilidades con nivel '{nivel}'")
                        continue

                elif '-' in seleccion and seleccion.replace('-', '').replace(' ', '').isdigit():
                    # Rango de números
                    try:
                        inicio, fin = map(int, seleccion.split('-'))
                        indices = list(range(inicio, fin + 1))
                        self.habilidades_seleccionadas = []

                        for indice in indices:
                            if 1 <= indice <= len(habilidades_disponibles):
                                self.habilidades_seleccionadas.append(habilidades_disponibles[indice - 1])

                        if self.habilidades_seleccionadas:
                            break
                    except ValueError:
                        print("❌ Formato de rango inválido. Usa: 1-5")
                        continue

                elif ',' in seleccion or seleccion.isdigit():
                    # Números separados por comas
                    try:
                        indices = [int(x.strip()) for x in seleccion.split(',')]
                        self.habilidades_seleccionadas = []

                        for indice in indices:
                            if 1 <= indice <= len(habilidades_disponibles):
                                self.habilidades_seleccionadas.append(habilidades_disponibles[indice - 1])
                            else:
                                print(f"⚠️ Número {indice} fuera de rango")

                        if self.habilidades_seleccionadas:
                            break
                    except ValueError:
                        print("❌ Números inválidos. Usa formato: 1,3,5")
                        continue

                else:
                    # Nombres de habilidades
                    nombres = [x.strip().title() for x in seleccion.split(',')]
                    self.habilidades_seleccionadas = []

                    for nombre in nombres:
                        coincidencias = [h for h in habilidades_disponibles
                                         if nombre.lower() in h.lower()]
                        if coincidencias:
                            self.habilidades_seleccionadas.extend(coincidencias)
                        else:
                            print(f"⚠️ No se encontró la habilidad: {nombre}")

                    # Eliminar duplicados
                    self.habilidades_seleccionadas = list(set(self.habilidades_seleccionadas))

                    if self.habilidades_seleccionadas:
                        break

                print("❌ Selección no válida. Inténtalo de nuevo.")

            except KeyboardInterrupt:
                print("\n❌ Operación cancelada")
                return False
            except Exception as e:
                print(f"❌ Error procesando selección: {e}")
                continue

        print(f"\n✅ Seleccionadas {len(self.habilidades_seleccionadas)} habilidades:")
        for i, hab in enumerate(self.habilidades_seleccionadas, 1):
            print(f"   {i}. {hab}")

        return True

    def obtener_preguntas_desde_bd(self, nivel_filtro: str = None, cantidad_por_habilidad: int = 2) -> bool:
        """Obtiene preguntas de la base de datos para las habilidades seleccionadas"""
        if not self.habilidades_seleccionadas:
            print("❌ No hay habilidades seleccionadas")
            return False

        print(f"\n🔍 OBTENIENDO PREGUNTAS DE LA BASE DE DATOS...")
        if nivel_filtro:
            print(f"📊 Filtro de nivel: {nivel_filtro}")
        print(f"📊 Cantidad por habilidad: {cantidad_por_habilidad}")
        print("=" * 55)

        preguntas_exitosas = 0

        for habilidad in self.habilidades_seleccionadas:
            print(f"🔄 Procesando {habilidad}...")

            preguntas = self.db_manager.obtener_preguntas_por_habilidad(
                habilidad,
                cantidad=cantidad_por_habilidad,
                nivel=nivel_filtro
            )

            if preguntas:
                self.preguntas_generadas[habilidad] = preguntas
                print(f"✅ {len(preguntas)} preguntas obtenidas")
                preguntas_exitosas += len(preguntas)
            else:
                print(f"⚠️ No se encontraron preguntas para {habilidad}")
                # Fallback con preguntas genéricas
                self.preguntas_generadas[habilidad] = [
                    f"¿Cuál es tu experiencia trabajando con {habilidad}?",
                    f"Describe un proyecto donde hayas aplicado {habilidad} de manera efectiva"
                ]
                preguntas_exitosas += 2

            time.sleep(0.3)  # Pausa visual

        print(f"\n✅ Proceso completado: {preguntas_exitosas} preguntas obtenidas")
        return True

    def mostrar_resumen_preguntas(self):
        """Muestra un resumen detallado de las preguntas obtenidas"""
        if not self.preguntas_generadas:
            print("❌ No hay preguntas generadas")
            return

        print("\n📊 RESUMEN DE PREGUNTAS GENERADAS")
        print("=" * 65)

        total_preguntas = 0
        for habilidad, preguntas in self.preguntas_generadas.items():
            print(f"\n🎯 {habilidad.upper()}:")
            print("-" * (len(habilidad) + 5))

            for i, pregunta in enumerate(preguntas, 1):
                # Truncar pregunta si es muy larga para mejor visualización
                pregunta_display = pregunta if len(pregunta) <= 80 else pregunta[:77] + "..."
                print(f"  {i}. {pregunta_display}")
                total_preguntas += 1

        # Estadísticas finales
        print(f"\n📈 ESTADÍSTICAS FINALES:")
        print("-" * 25)
        print(f"• Habilidades evaluadas: {len(self.preguntas_generadas)}")
        print(f"• Total de preguntas: {total_preguntas}")
        if self.preguntas_generadas:
            print(f"• Promedio por habilidad: {total_preguntas / len(self.preguntas_generadas):.1f}")

    def exportar_preguntas(self, formato: str = "txt") -> str:
        """Exporta las preguntas en diferentes formatos"""
        if not self.preguntas_generadas:
            print("❌ No hay preguntas para exportar")
            return None

        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")

            if formato.lower() == "txt":
                filename = f"entrevista_tecnica_{timestamp}.txt"
                self._exportar_txt(filename)
            elif formato.lower() == "json":
                filename = f"entrevista_tecnica_{timestamp}.json"
                self._exportar_json(filename)
            elif formato.lower() == "csv":
                filename = f"entrevista_tecnica_{timestamp}.csv"
                self._exportar_csv(filename)
            else:
                print(f"❌ Formato '{formato}' no soportado. Use: txt, json, csv")
                return None

            print(f"✅ Preguntas exportadas: {filename}")
            return filename

        except Exception as e:
            print(f"❌ Error exportando: {e}")
            return None

    def _exportar_txt(self, filename: str):
        """Exporta en formato texto plano"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("🎯 PREGUNTAS DE ENTREVISTA TÉCNICA\n")
            f.write("=" * 65 + "\n")
            f.write(f"Generado: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Habilidades: {len(self.preguntas_generadas)}\n")
            f.write(f"Total preguntas: {sum(len(p) for p in self.preguntas_generadas.values())}\n\n")

            for habilidad, preguntas in self.preguntas_generadas.items():
                f.write(f"\n🎯 {habilidad.upper()}:\n")
                f.write("-" * (len(habilidad) + 5) + "\n")
                for i, pregunta in enumerate(preguntas, 1):
                    f.write(f"  {i}. {pregunta}\n")

            f.write(f"\n\n--- Fin del documento ---")

    def _exportar_json(self, filename: str):
        """Exporta en formato JSON"""
        import json

        data = {
            "metadata": {
                "generado": time.strftime('%Y-%m-%d %H:%M:%S'),
                "total_habilidades": len(self.preguntas_generadas),
                "total_preguntas": sum(len(p) for p in self.preguntas_generadas.values())
            },
            "preguntas_por_habilidad": self.preguntas_generadas
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _exportar_csv(self, filename: str):
        """Exporta en formato CSV"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Habilidad,Numero_Pregunta,Pregunta\n")

            for habilidad, preguntas in self.preguntas_generadas.items():
                for i, pregunta in enumerate(preguntas, 1):
                    # Escapar comillas en CSV
                    pregunta_csv = pregunta.replace('"', '""')
                    f.write(f'"{habilidad}",{i},"{pregunta_csv}"\n')

    def menu_configuracion_avanzada(self):
        """Menú para configuraciones avanzadas"""
        while True:
            print("\n⚙️ CONFIGURACIÓN AVANZADA:")
            print("1. Filtrar por nivel de dificultad")
            print("2. Cambiar cantidad de preguntas por habilidad")
            print("3. Regenerar preguntas (diferentes aleatorias)")
            print("4. Agregar nueva habilidad manualmente")
            print("5. Ver estadísticas detalladas de BD")
            print("6. Volver al menú principal")

            try:
                opcion = input("\nSelecciona (1-6): ").strip()

                if opcion == "1":
                    print("\nNiveles disponibles: basico, intermedio, avanzado")
                    nivel = input("Nivel a filtrar (o 'ninguno' para quitar filtro): ").strip().lower()
                    nivel_filtro = nivel if nivel not in ['ninguno', 'none', ''] else None

                    if self.obtener_preguntas_desde_bd(nivel_filtro=nivel_filtro):
                        print(f"✅ Preguntas filtradas por nivel: {nivel_filtro or 'todos'}")

                elif opcion == "2":
                    try:
                        cantidad = int(input("Nueva cantidad por habilidad (1-10): "))
                        cantidad = max(1, min(cantidad, 10))  # Limitar entre 1 y 10

                        if self.obtener_preguntas_desde_bd(cantidad_por_habilidad=cantidad):
                            print(f"✅ Cantidad actualizada a {cantidad} preguntas por habilidad")
                    except ValueError:
                        print("❌ Cantidad inválida")

                elif opcion == "3":
                    if self.obtener_preguntas_desde_bd():
                        print("✅ Preguntas regeneradas")

                elif opcion == "4":
                    self._agregar_habilidad_manual()

                elif opcion == "5":
                    self._mostrar_estadisticas_detalladas()

                elif opcion == "6":
                    break

                else:
                    print("⚠️ Opción no válida")

            except KeyboardInterrupt:
                print("\n🔙 Volviendo al menú principal...")
                break

    def _agregar_habilidad_manual(self):
        """Permite agregar una habilidad y preguntas manualmente"""
        print("\n➕ AGREGAR NUEVA HABILIDAD")
        print("-" * 30)

        try:
            habilidad = input("Nombre de la habilidad: ").strip().title()
            if not habilidad:
                print("❌ Nombre inválido")
                return

            preguntas = []
            print("Ingresa preguntas (escribe 'fin' para terminar):")

            i = 1
            while True:
                pregunta = input(f"{i}. ").strip()
                if pregunta.lower() in ['fin', 'terminar']:
                    break

                if pregunta:
                    preguntas.append(pregunta)
                    i += 1

            if preguntas:
                nivel = input("Nivel (basico/intermedio/avanzado) [intermedio]: ").strip().lower() or "intermedio"

                # Agregar a la base de datos
                agregadas = 0
                for pregunta in preguntas:
                    if self.db_manager.agregar_pregunta(habilidad, pregunta, nivel=nivel):
                        agregadas += 1

                print(f"✅ Se agregaron {agregadas} preguntas para {habilidad}")
            else:
                print("❌ No se agregaron preguntas")

        except KeyboardInterrupt:
            print("\n❌ Operación cancelada")

    def _mostrar_estadisticas_detalladas(self):
        """Muestra estadísticas detalladas de la base de datos"""
        resumen = self.db_manager.obtener_resumen_completo()

        print(f"\n📊 ESTADÍSTICAS DETALLADAS DE LA BASE DE DATOS")
        print("=" * 60)
        print(f"📁 Archivo: {resumen['archivo_bd']}")
        print(f"📚 Total de preguntas: {resumen['total_preguntas']}")
        print(f"🎯 Total de habilidades: {resumen['total_habilidades']}")

        if resumen['estadisticas']:
            print(f"\n📈 DESGLOSE POR HABILIDAD:")
            print("-" * 40)

            for habilidad, stats in resumen['estadisticas'].items():
                print(f"\n{habilidad}: {stats['total']} preguntas")

                if stats['por_nivel']:
                    niveles = ", ".join([f"{nivel}: {count}" for nivel, count in stats['por_nivel'].items()])
                    print(f"  └── Niveles: {niveles}")

                if stats['por_tipo']:
                    tipos = ", ".join([f"{tipo}: {count}" for tipo, count in stats['por_tipo'].items()])
                    print(f"  └── Tipos: {tipos}")

    def menu_principal(self):
        """Menú principal de opciones"""
        while True:
            print("\n🎛️ MENÚ PRINCIPAL - AGENTE ENTREVISTADOR")
            print("=" * 50)
            print("1. 📋 Ver resumen de preguntas actuales")
            print("2. 📁 Exportar preguntas (TXT/JSON/CSV)")
            print("3. 🔄 Cambiar selección de habilidades")
            print("4. ⚙️ Configuración avanzada")
            print("5. 📊 Estadísticas de base de datos")
            print("6. 🔧 Herramientas de base de datos")
            print("7. ❌ Salir")

            try:
                opcion = input("\nSelecciona una opción (1-7): ").strip()

                if opcion == "1":
                    self.mostrar_resumen_preguntas()

                elif opcion == "2":
                    print("\nFormatos disponibles:")
                    print("1. TXT (texto plano)")
                    print("2. JSON (estructura de datos)")
                    print("3. CSV (hoja de cálculo)")

                    formato_op = input("Selecciona formato (1-3): ").strip()
                    formatos = {"1": "txt", "2": "json", "3": "csv"}

                    if formato_op in formatos:
                        archivo = self.exportar_preguntas(formatos[formato_op])
                        if archivo:
                            print(f"📁 Archivo creado: {archivo}")
                    else:
                        print("⚠️ Formato no válido")

                elif opcion == "3":
                    if self.seleccionar_habilidades():
                        self.obtener_preguntas_desde_bd()

                elif opcion == "4":
                    self.menu_configuracion_avanzada()

                elif opcion == "5":
                    self._mostrar_estadisticas_detalladas()

                elif opcion == "6":
                    self._menu_herramientas_bd()

                elif opcion == "7":
                    print("👋 ¡Gracias por usar el Agente Entrevistador!")
                    break

                else:
                    print("⚠️ Opción no válida. Selecciona 1-7.")

            except KeyboardInterrupt:
                print("\n\n👋 ¡Sesión terminada!")
                break
            except Exception as e:
                print(f"❌ Error inesperado: {e}")

    def _menu_herramientas_bd(self):
        """Menú de herramientas para manejo de base de datos"""
        while True:
            print("\n🔧 HERRAMIENTAS DE BASE DE DATOS:")
            print("1. Recargar datos iniciales")
            print("2. Exportar BD completa a SQL")
            print("3. Limpiar base de datos")
            print("4. Buscar preguntas por término")
            print("5. Volver al menú principal")

            try:
                opcion = input("\nSelecciona (1-5): ").strip()

                if opcion == "1":
                    confirmacion = input("¿Recargar datos iniciales? Esto puede duplicar datos (s/n): ")
                    if confirmacion.lower() in ['s', 'si', 'sí']:
                        if self.data_loader.cargar_datos_iniciales(self.db_manager, forzar_recarga=True):
                            print("✅ Datos recargados")

                elif opcion == "2":
                    filename = f"backup_bd_{time.strftime('%Y%m%d_%H%M%S')}.sql"
                    if self.db_manager.exportar_bd_a_sql(filename):
                        print(f"✅ BD exportada a: {filename}")

                elif opcion == "3":
                    confirmacion = input("⚠️ ¿LIMPIAR TODA LA BASE DE DATOS? (escribe 'CONFIRMAR'): ")
                    if confirmacion == "CONFIRMAR":
                        if self.db_manager.limpiar_base_datos():
                            print("✅ Base de datos limpiada")
                            # Recargar datos automáticamente
                            self.inicializar_datos_si_necesario()

                elif opcion == "4":
                    termino = input("Término a buscar: ").strip()
                    if termino:
                        resultados = self.db_manager.buscar_preguntas(termino)
                        if resultados:
                            print(f"\n🔍 Encontradas {len(resultados)} preguntas:")
                            for hab, pregunta, tipo, nivel in resultados:
                                print(f"• {hab} ({nivel}): {pregunta[:60]}...")
                        else:
                            print("❌ No se encontraron resultados")

                elif opcion == "5":
                    break

            except KeyboardInterrupt:
                break


def main():
    """Función principal del programa"""
    print("\n🎯 AGENTE ENTREVISTADOR - ARQUITECTURA PROFESIONAL")
    print("=" * 65)
    print("Sistema de generación de preguntas técnicas con base de datos SQLite")
    print("Arquitectura desacoplada con módulos especializados")
    print("=" * 65)

    if not MODULOS_DISPONIBLES:
        print("\n❌ ERROR: Módulos requeridos no disponibles")
        print("📋 Archivos necesarios:")
        print("   • database_manager.py")
        print("   • data_loader.py")
        print("   • agente.py (este archivo)")
        return

    try:
        # Verificar si la BD necesita inicialización
        if not os.path.exists("../preguntas_entrevista.db"):
            print("\n🆕 Primera ejecución detectada")
            print("🔄 Inicializando base de datos con preguntas predefinidas...")
            inicializar_base_datos_completa()

        # Crear el agente
        agente = AgenteEntrevistador()

        # Mostrar estadísticas iniciales
        total_preguntas = agente.db_manager.contar_preguntas()
        total_habilidades = len(agente.db_manager.obtener_todas_habilidades())

        print(f"\n📊 ESTADO ACTUAL:")
        print(f"   📚 {total_preguntas} preguntas en base de datos")
        print(f"   🎯 {total_habilidades} habilidades disponibles")

        # Proceso principal
        print(f"\n🚀 INICIANDO PROCESO DE GENERACIÓN...")

        # Seleccionar habilidades
        if not agente.seleccionar_habilidades():
            print("❌ No se seleccionaron habilidades. Saliendo...")
            return

        # Obtener preguntas de la BD
        if not agente.obtener_preguntas_desde_bd():
            print("❌ Error obteniendo preguntas. Saliendo...")
            return

        # Mostrar resumen inicial
        agente.mostrar_resumen_preguntas()

        # Menú principal
        agente.menu_principal()

    except KeyboardInterrupt:
        print("\n\n👋 ¡Sesión terminada por el usuario!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("💡 Verifica que todos los archivos estén presentes y sean válidos")


if __name__ == "__main__":
    main()