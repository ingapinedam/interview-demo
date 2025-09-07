print("🎯 Agente IA para Entrevistas Técnicas")
print("=" * 50)

try:
    from langchain.llms import Ollama
    from langchain.schema import HumanMessage, SystemMessage
    import time
    import json

    print("✅ LangChain importado correctamente")
    LANGCHAIN_OK = True
except ImportError as e:
    print(f"❌ Error importando LangChain: {e}")
    LANGCHAIN_OK = False


class AgenteEntrevistador:
    def __init__(self, modelo="llama2"):
        print("🤖 Inicializando Agente Entrevistador...")
        self.modelo = modelo
        self.habilidades = []
        self.preguntas_generadas = {}
        self.memoria_entrevistas = []

        # Conectar con Ollama
        if LANGCHAIN_OK:
            try:
                print(f"🔄 Conectando con modelo {modelo}...")
                self.llm = Ollama(model=modelo)

                # Prueba de conexión
                test_response = self.llm("Responde solo: OK")
                print("✅ Conexión con Ollama establecida")
                self.ia_disponible = True

            except Exception as e:
                print(f"⚠️ Error conectando con Ollama: {e}")
                print("💡 Ejecuta 'ollama serve' en otra terminal")
                self.ia_disponible = False
        else:
            self.ia_disponible = False

    def capturar_habilidades(self):
        """Captura las habilidades técnicas del candidato"""
        print("\n📋 CONFIGURACIÓN DE HABILIDADES TÉCNICAS")
        print("=" * 50)
        print("Ingresa las habilidades que quieres evaluar en la entrevista.")
        print("Ejemplos: Python, JavaScript, React, SQL, Docker, etc.")
        print("Escribe 'fin' cuando termines de agregar habilidades.")
        print("-" * 50)

        habilidades_temp = []
        contador = 1

        while True:
            try:
                habilidad = input(f"\n{contador}. Habilidad: ").strip()

                if habilidad.lower() in ['fin', 'terminar', 'listo']:
                    break

                if not habilidad:
                    print("⚠️ Por favor ingresa una habilidad válida")
                    continue

                # Evitar duplicados
                if habilidad.lower() not in [h.lower() for h in habilidades_temp]:
                    habilidades_temp.append(habilidad.title())
                    print(f"✅ '{habilidad.title()}' agregada")
                    contador += 1
                else:
                    print("⚠️ Esa habilidad ya fue agregada")

            except KeyboardInterrupt:
                print("\n❌ Operación cancelada")
                return False

        if not habilidades_temp:
            print("❌ No se agregaron habilidades")
            return False

        self.habilidades = habilidades_temp

        print(f"\n✅ {len(self.habilidades)} habilidades configuradas:")
        for i, hab in enumerate(self.habilidades, 1):
            print(f"   {i}. {hab}")

        return True

    def generar_preguntas_habilidad(self, habilidad):
        """Genera 2 preguntas para una habilidad específica"""
        if not self.ia_disponible:
            # Modo simulado con preguntas básicas
            preguntas_simuladas = [
                f"¿Cuál es tu experiencia trabajando con {habilidad}?",
                f"¿Puedes explicar un proyecto donde hayas usado {habilidad}?"
            ]
            return preguntas_simuladas

        try:
            print(f"🔄 Generando preguntas para {habilidad}...")

            prompt = f"""Eres un experto reclutador técnico. Genera exactamente 2 preguntas de entrevista para evaluar la habilidad técnica: {habilidad}

Requisitos:
- Preguntas claras y específicas
- Una pregunta conceptual/teórica
- Una pregunta práctica/experiencia
- Nivel intermedio de dificultad
- En español
- Sin numeración

Formato de respuesta:
PREGUNTA 1: [pregunta conceptual]
PREGUNTA 2: [pregunta práctica]

Habilidad a evaluar: {habilidad}"""

            respuesta = self.llm(prompt)

            # Procesar la respuesta para extraer las preguntas
            preguntas = self.extraer_preguntas(respuesta)

            if len(preguntas) >= 2:
                return preguntas[:2]  # Solo las primeras 2
            else:
                # Fallback si no se pudieron extraer
                return [
                    f"¿Cuáles son los conceptos fundamentales de {habilidad}?",
                    f"Describe un proyecto donde hayas aplicado {habilidad}"
                ]

        except Exception as e:
            print(f"❌ Error generando preguntas: {e}")
            return [
                f"¿Cuál es tu nivel de experiencia con {habilidad}?",
                f"¿Puedes dar un ejemplo de uso de {habilidad}?"
            ]

    def extraer_preguntas(self, respuesta_ia):
        """Extrae preguntas de la respuesta de la IA"""
        preguntas = []
        lineas = respuesta_ia.split('\n')

        for linea in lineas:
            linea = linea.strip()
            # Buscar líneas que contengan preguntas
            if ('PREGUNTA' in linea.upper() and ':' in linea) or linea.endswith('?'):
                # Limpiar la pregunta
                if ':' in linea:
                    pregunta = linea.split(':', 1)[1].strip()
                else:
                    pregunta = linea

                if pregunta and pregunta.endswith('?'):
                    preguntas.append(pregunta)

        return preguntas

    def generar_todas_las_preguntas(self):
        """Genera preguntas para todas las habilidades"""
        print("\n🧠 GENERANDO PREGUNTAS DE ENTREVISTA...")
        print("=" * 50)

        for habilidad in self.habilidades:
            preguntas = self.generar_preguntas_habilidad(habilidad)
            self.preguntas_generadas[habilidad] = preguntas

            print(f"\n📌 {habilidad}:")
            for i, pregunta in enumerate(preguntas, 1):
                print(f"   {i}. {pregunta}")

            time.sleep(1)  # Pausa entre generaciones

        print(f"\n✅ Se generaron {len(self.preguntas_generadas)} conjuntos de preguntas")

    def mostrar_resumen_preguntas(self):
        """Muestra un resumen completo de todas las preguntas"""
        print("\n📊 RESUMEN COMPLETO DE PREGUNTAS")
        print("=" * 60)

        total_preguntas = 0
        for habilidad, preguntas in self.preguntas_generadas.items():
            print(f"\n🎯 {habilidad.upper()}:")
            print("-" * (len(habilidad) + 5))
            for i, pregunta in enumerate(preguntas, 1):
                print(f"  {i}. {pregunta}")
                total_preguntas += 1

        print(f"\n📈 ESTADÍSTICAS:")
        print(f"   • Total de habilidades: {len(self.habilidades)}")
        print(f"   • Total de preguntas: {total_preguntas}")
        print(f"   • Promedio por habilidad: {total_preguntas / len(self.habilidades):.1f}")

    def exportar_preguntas(self):
        """Exporta las preguntas a un archivo de texto"""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"entrevista_tecnica_{timestamp}.txt"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write("🎯 PREGUNTAS DE ENTREVISTA TÉCNICA\n")
                f.write("=" * 50 + "\n")
                f.write(f"Generado: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Habilidades evaluadas: {len(self.habilidades)}\n\n")

                for habilidad, preguntas in self.preguntas_generadas.items():
                    f.write(f"\n📌 {habilidad.upper()}:\n")
                    f.write("-" * (len(habilidad) + 5) + "\n")
                    for i, pregunta in enumerate(preguntas, 1):
                        f.write(f"  {i}. {pregunta}\n")

                f.write(f"\n\nTotal de preguntas: {sum(len(p) for p in self.preguntas_generadas.values())}")

            print(f"✅ Preguntas exportadas a: {filename}")
            return filename

        except Exception as e:
            print(f"❌ Error exportando: {e}")
            return None

    def menu_opciones(self):
        """Muestra menú de opciones después de generar preguntas"""
        while True:
            print("\n🎛️ OPCIONES DISPONIBLES:")
            print("1. Ver resumen completo")
            print("2. Exportar preguntas a archivo")
            print("3. Agregar más habilidades")
            print("4. Regenerar preguntas")
            print("5. Salir")

            try:
                opcion = input("\nSelecciona una opción (1-5): ").strip()

                if opcion == "1":
                    self.mostrar_resumen_preguntas()

                elif opcion == "2":
                    archivo = self.exportar_preguntas()
                    if archivo:
                        print(f"📁 Archivo guardado como: {archivo}")

                elif opcion == "3":
                    print("\n➕ Agregando nuevas habilidades...")
                    if self.capturar_habilidades():
                        self.generar_todas_las_preguntas()

                elif opcion == "4":
                    print("\n🔄 Regenerando todas las preguntas...")
                    self.preguntas_generadas = {}
                    self.generar_todas_las_preguntas()

                elif opcion == "5":
                    print("👋 ¡Gracias por usar el Agente Entrevistador!")
                    break

                else:
                    print("⚠️ Opción no válida. Selecciona 1-5.")

            except KeyboardInterrupt:
                print("\n👋 ¡Adiós!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    print("\n🎯 BIENVENIDO AL AGENTE ENTREVISTADOR")
    print("=" * 60)
    print("Este agente te ayudará a generar preguntas técnicas")
    print("personalizadas para entrevistas de trabajo.")
    print("=" * 60)

    # Crear el agente
    agente = AgenteEntrevistador(modelo="llama2")

    if not agente.ia_disponible:
        print("\n⚠️ MODO SIMULADO ACTIVADO")
        print("Para mejores preguntas, activa Ollama:")
        print("1. Ejecuta 'ollama serve' en una terminal")
        print("2. Ejecuta 'ollama pull llama2' en otra terminal")

        continuar = input("\n¿Continuar en modo simulado? (s/n): ")
        if continuar.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
            print("👋 ¡Hasta luego!")
            return

    # Proceso principal
    try:
        # Paso 1: Capturar habilidades
        if not agente.capturar_habilidades():
            print("❌ No se pudieron capturar las habilidades")
            return

        # Paso 2: Generar preguntas
        agente.generar_todas_las_preguntas()

        # Paso 3: Mostrar resumen inicial
        agente.mostrar_resumen_preguntas()

        # Paso 4: Menú de opciones
        agente.menu_opciones()

    except KeyboardInterrupt:
        print("\n\n👋 ¡Sesión terminada!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()