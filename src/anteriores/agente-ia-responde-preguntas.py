print("🚀 Inicializando agente con IA real...")

try:
    from langchain.llms import Ollama
    from langchain.schema import HumanMessage, SystemMessage
    import time

    print("✅ LangChain importado correctamente")
    LANGCHAIN_OK = True
except ImportError as e:
    print(f"❌ Error importando LangChain: {e}")
    LANGCHAIN_OK = False


class AgenteIAReal:
    def __init__(self, modelo="llama2"):
        print("🤖 Inicializando Agente IA Real...")
        self.memoria = []
        self.modelo = modelo

        # Intentar conectar con Ollama
        if LANGCHAIN_OK:
            try:
                print(f"🔄 Conectando con modelo {modelo}...")
                self.llm = Ollama(model=modelo)

                # Hacer una prueba rápida
                test_response = self.llm("Di solo 'OK'")
                print("✅ Conexión con Ollama establecida correctamente")
                self.ia_disponible = True

            except Exception as e:
                print(f"⚠️ Error conectando con Ollama: {e}")
                print("💡 Asegúrate de que:")
                print("   1. 'ollama serve' esté corriendo en otra terminal")
                print(f"   2. El modelo '{modelo}' esté descargado: ollama pull {modelo}")
                self.ia_disponible = False
        else:
            self.ia_disponible = False

    def respuesta_inteligente(self, consulta):
        """Genera una respuesta usando IA o modo simulado"""
        if self.ia_disponible:
            try:
                print("🔄 Procesando con IA...")

                # Prompt mejorado para mejores respuestas
                prompt = f"""Eres un asistente IA útil y amigable. 
                Responde de manera clara, concisa y en español.

                Pregunta: {consulta}

                Respuesta:"""

                respuesta = self.llm(prompt)
                return respuesta.strip()

            except Exception as e:
                return f"❌ Error procesando con IA: {e}"
        else:
            # Modo simulado con respuestas más inteligentes
            respuestas_simuladas = {
                "hola": "¡Hola! Soy tu agente IA. Aunque estoy en modo simulado, puedo ayudarte.",
                "python": "Python es un lenguaje de programación versátil, ideal para IA y desarrollo web.",
                "agente": "Un agente IA es un programa que puede percibir, razonar y actuar de forma autónoma.",
                "ayuda": "Puedo ayudarte con programación, explicaciones técnicas y responder preguntas.",
                "default": f"Modo simulado: He recibido tu consulta '{consulta}'. Para respuestas reales, activa Ollama."
            }

            # Buscar palabras clave en la consulta
            consulta_lower = consulta.lower()
            for palabra_clave, respuesta in respuestas_simuladas.items():
                if palabra_clave in consulta_lower:
                    return respuesta

            return respuestas_simuladas["default"]

    def conversar(self, consulta):
        """Procesa una consulta y la guarda en memoria"""
        print(f"\n❓ Usuario: {consulta}")

        inicio = time.time()
        respuesta = self.respuesta_inteligente(consulta)
        tiempo = time.time() - inicio

        # Guardar en memoria
        self.memoria.append({
            "consulta": consulta,
            "respuesta": respuesta,
            "tiempo": round(tiempo, 2)
        })

        print(f"🤖 Agente ({tiempo:.1f}s): {respuesta}")
        return respuesta

    def mostrar_memoria(self):
        """Muestra el historial de conversación"""
        print("\n" + "=" * 60)
        print("📚 MEMORIA DEL AGENTE")
        print("=" * 60)

        if not self.memoria:
            print("No hay conversaciones guardadas.")
            return

        for i, item in enumerate(self.memoria, 1):
            print(f"\n{i}. 👤 Usuario: {item['consulta']}")
            print(f"   🤖 Agente ({item['tiempo']}s): {item['respuesta']}")

        print(f"\n📊 Total: {len(self.memoria)} interacciones")

    def conversacion_interactiva(self):
        """Modo conversación interactiva con el usuario"""
        print("\n" + "=" * 50)
        print("💬 MODO CONVERSACIÓN INTERACTIVA")
        print("=" * 50)
        print("Escribe 'salir', 'quit' o 'exit' para terminar")
        print("Escribe 'memoria' para ver el historial")
        print("-" * 50)

        while True:
            try:
                consulta = input("\n👤 Tú: ").strip()

                if consulta.lower() in ['salir', 'quit', 'exit', 'bye']:
                    print("👋 ¡Hasta luego!")
                    break

                if consulta.lower() == 'memoria':
                    self.mostrar_memoria()
                    continue

                if not consulta:
                    print("⚠️ Por favor escribe algo...")
                    continue

                self.conversar(consulta)

            except KeyboardInterrupt:
                print("\n👋 ¡Adiós!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    print("\n" + "=" * 60)
    print("🎯 AGENTE IA - SISTEMA INICIADO")
    print("=" * 60)

    # Crear el agente (prueba primero con 'phi' si tienes problemas con 'llama2')
    agente = AgenteIAReal(modelo="llama2")

    if not agente.ia_disponible:
        print("\n⚠️ MODO SIMULADO ACTIVADO")
        print("Para activar IA real:")
        print("1. Ejecuta 'ollama serve' en una terminal")
        print("2. Ejecuta 'ollama pull llama2' en otra terminal")

    # Pruebas automáticas
    print("\n🧪 EJECUTANDO PRUEBAS...")
    print("-" * 40)

    preguntas_prueba = [
        "Hola, ¿cómo estás?",
        "¿Qué es Python?",
        "¿Cómo funciona un agente de IA?",
        "Dame un consejo para programar mejor"
    ]

    for pregunta in preguntas_prueba:
        agente.conversar(pregunta)
        time.sleep(1)  # Pausa entre preguntas

    # Mostrar resumen
    agente.mostrar_memoria()

    # Ofrecer modo interactivo
    print("\n🤔 ¿Quieres continuar en modo interactivo? (s/n)")
    respuesta = input().lower().strip()

    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        agente.conversacion_interactiva()
    else:
        print("👋 ¡Gracias por probar el agente!")


if __name__ == "__main__":
    main()