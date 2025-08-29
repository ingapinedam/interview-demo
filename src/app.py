"""
Servidor Flask para Interfaz Web del Agente Entrevistador
Proporciona API REST y sirve la interfaz HTML
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import json
from datetime import datetime
import io

# Agregar el directorio actual al path para importar nuestros módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from database_manager import DatabaseManager
    from data_loader import DataLoader, inicializar_base_datos_completa

    print("✅ Módulos importados correctamente")
    MODULOS_DISPONIBLES = True
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    MODULOS_DISPONIBLES = False

# Inicializar Flask
import os
app = Flask(__name__,
           template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
           static_folder=os.path.join(os.path.dirname(__file__), 'static'))
CORS(app)  # Permitir CORS para desarrollo

# Variables globales
db_manager = None
data_loader = None


def inicializar_sistema():
    """Inicializa el sistema de base de datos"""
    global db_manager, data_loader

    if not MODULOS_DISPONIBLES:
        return False

    try:
        # Inicializar componentes
        db_manager = DatabaseManager()
        data_loader = DataLoader()

        # Cargar datos si es necesario
        if db_manager.contar_preguntas() == 0:
            print("📝 Cargando preguntas iniciales...")
            data_loader.cargar_datos_iniciales(db_manager)

        return True

    except Exception as e:
        print(f"❌ Error inicializando sistema: {e}")
        return False


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/api/status')
def api_status():
    """Estado del sistema"""
    if not MODULOS_DISPONIBLES:
        return jsonify({
            'status': 'error',
            'message': 'Módulos no disponibles'
        })

    try:
        total_preguntas = db_manager.contar_preguntas()
        habilidades = db_manager.obtener_todas_habilidades()

        return jsonify({
            'status': 'success',
            'data': {
                'total_preguntas': total_preguntas,
                'total_habilidades': len(habilidades),
                'habilidades': habilidades,
                'sistema_listo': total_preguntas > 0
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


@app.route('/api/habilidades')
def api_habilidades():
    """Obtiene todas las habilidades disponibles"""
    try:
        habilidades = db_manager.obtener_todas_habilidades()
        habilidades_con_stats = []

        for habilidad in habilidades:
            stats = db_manager.obtener_estadisticas_habilidad(habilidad)
            habilidades_con_stats.append({
                'nombre': habilidad,
                'total': stats.get('total', 0),
                'por_nivel': stats.get('por_nivel', {}),
                'por_tipo': stats.get('por_tipo', {})
            })

        return jsonify({
            'status': 'success',
            'data': habilidades_con_stats
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


@app.route('/api/generar-preguntas', methods=['POST'])
def api_generar_preguntas():
    """Genera preguntas basadas en la selección del usuario"""
    try:
        data = request.get_json()

        habilidades_seleccionadas = data.get('habilidades', [])
        nivel_filtro = data.get('nivel_filtro')
        cantidad_por_habilidad = data.get('cantidad_por_habilidad', 2)

        if not habilidades_seleccionadas:
            return jsonify({
                'status': 'error',
                'message': 'No se seleccionaron habilidades'
            })

        preguntas_resultado = {}

        for habilidad in habilidades_seleccionadas:
            preguntas = db_manager.obtener_preguntas_por_habilidad(
                habilidad,
                cantidad=cantidad_por_habilidad,
                nivel=nivel_filtro
            )

            if preguntas:
                preguntas_resultado[habilidad] = preguntas
            else:
                # Fallback con preguntas genéricas
                preguntas_resultado[habilidad] = [
                    f"¿Cuál es tu experiencia trabajando con {habilidad}?",
                    f"Describe un proyecto donde hayas aplicado {habilidad} de manera efectiva"
                ]

        # Estadísticas
        total_preguntas = sum(len(p) for p in preguntas_resultado.values())

        return jsonify({
            'status': 'success',
            'data': {
                'preguntas': preguntas_resultado,
                'estadisticas': {
                    'total_habilidades': len(preguntas_resultado),
                    'total_preguntas': total_preguntas,
                    'promedio_por_habilidad': round(total_preguntas / len(preguntas_resultado),
                                                    1) if preguntas_resultado else 0
                }
            }
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


@app.route('/api/exportar', methods=['POST'])
def api_exportar():
    """Exporta preguntas en formato especificado"""
    try:
        data = request.get_json()

        preguntas = data.get('preguntas', {})
        formato = data.get('formato', 'txt')

        if not preguntas:
            return jsonify({
                'status': 'error',
                'message': 'No hay preguntas para exportar'
            })

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if formato == 'json':
            filename = f"entrevista_tecnica_{timestamp}.json"
            content = json.dumps({
                "metadata": {
                    "generado": datetime.now().isoformat(),
                    "total_habilidades": len(preguntas),
                    "total_preguntas": sum(len(p) for p in preguntas.values())
                },
                "preguntas_por_habilidad": preguntas
            }, indent=2, ensure_ascii=False)
            mimetype = 'application/json'

        elif formato == 'csv':
            filename = f"entrevista_tecnica_{timestamp}.csv"
            content = "Habilidad,Numero_Pregunta,Pregunta\n"

            for habilidad, lista_preguntas in preguntas.items():
                for i, pregunta in enumerate(lista_preguntas, 1):
                    pregunta_csv = pregunta.replace('"', '""')
                    content += f'"{habilidad}",{i},"{pregunta_csv}"\n'
            mimetype = 'text/csv'

        else:  # txt por defecto
            filename = f"entrevista_tecnica_{timestamp}.txt"
            content = "🎯 PREGUNTAS DE ENTREVISTA TÉCNICA\n"
            content += "=" * 65 + "\n"
            content += f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            content += f"Habilidades: {len(preguntas)}\n"
            content += f"Total preguntas: {sum(len(p) for p in preguntas.values())}\n\n"

            for habilidad, lista_preguntas in preguntas.items():
                content += f"\n🎯 {habilidad.upper()}:\n"
                content += "-" * (len(habilidad) + 5) + "\n"
                for i, pregunta in enumerate(lista_preguntas, 1):
                    content += f"  {i}. {pregunta}\n"

            content += "\n\n--- Fin del documento ---"
            mimetype = 'text/plain'

        # Crear archivo en memoria
        archivo_memoria = io.BytesIO()
        archivo_memoria.write(content.encode('utf-8'))
        archivo_memoria.seek(0)

        return send_file(
            archivo_memoria,
            as_attachment=True,
            download_name=filename,
            mimetype=mimetype
        )

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


@app.route('/api/estadisticas')
def api_estadisticas():
    """Obtiene estadísticas completas del sistema"""
    try:
        resumen = db_manager.obtener_resumen_completo()
        stats_generales = db_manager.obtener_estadisticas_generales()

        return jsonify({
            'status': 'success',
            'data': {
                'resumen': resumen,
                'generales': stats_generales
            }
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


@app.route('/api/buscar', methods=['POST'])
def api_buscar():
    """Busca preguntas por término"""
    try:
        data = request.get_json()
        termino = data.get('termino', '').strip()

        if not termino:
            return jsonify({
                'status': 'error',
                'message': 'Término de búsqueda vacío'
            })

        resultados = db_manager.buscar_preguntas(termino, limit=20)

        resultados_formateados = []
        for habilidad, pregunta, tipo, nivel in resultados:
            resultados_formateados.append({
                'habilidad': habilidad,
                'pregunta': pregunta,
                'tipo': tipo,
                'nivel': nivel
            })

        return jsonify({
            'status': 'success',
            'data': {
                'termino': termino,
                'total_encontrados': len(resultados_formateados),
                'resultados': resultados_formateados
            }
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


@app.route('/api/agregar-pregunta', methods=['POST'])
def api_agregar_pregunta():
    """Agrega una nueva pregunta a la base de datos"""
    try:
        data = request.get_json()

        habilidad = data.get('habilidad', '').strip()
        pregunta = data.get('pregunta', '').strip()
        tipo = data.get('tipo', 'general').strip()
        nivel = data.get('nivel', 'intermedio').strip()

        if not habilidad or not pregunta:
            return jsonify({
                'status': 'error',
                'message': 'Habilidad y pregunta son requeridos'
            })

        if db_manager.agregar_pregunta(habilidad, pregunta, tipo, nivel):
            return jsonify({
                'status': 'success',
                'message': f'Pregunta agregada para {habilidad}'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Error agregando pregunta'
            })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


@app.route('/api/backup')
def api_backup():
    """Genera un backup de la base de datos"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_bd_{timestamp}.sql"

        if db_manager.exportar_bd_a_sql(filename):
            # Leer el archivo generado y enviarlo
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()

            # Eliminar el archivo temporal
            os.remove(filename)

            archivo_memoria = io.BytesIO()
            archivo_memoria.write(content.encode('utf-8'))
            archivo_memoria.seek(0)

            return send_file(
                archivo_memoria,
                as_attachment=True,
                download_name=filename,
                mimetype='application/sql'
            )
        else:
            return jsonify({
                'status': 'error',
                'message': 'Error generando backup'
            })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


@app.route('/api/limpiar-bd', methods=['POST'])
def api_limpiar_bd():
    """Limpia la base de datos y recarga datos iniciales"""
    try:
        if db_manager.limpiar_base_datos():
            # Recargar datos iniciales
            if data_loader.cargar_datos_iniciales(db_manager):
                return jsonify({
                    'status': 'success',
                    'message': 'Base de datos limpiada y recargada'
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'BD limpiada pero error recargando datos'
                })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Error limpiando base de datos'
            })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


@app.route('/api/eliminar-pregunta', methods=['POST'])
def api_eliminar_pregunta():
    """Elimina una pregunta específica"""
    try:
        data = request.get_json()
        pregunta_id = data.get('id')

        if not pregunta_id:
            return jsonify({
                'status': 'error',
                'message': 'ID de pregunta requerido'
            })

        if db_manager.eliminar_pregunta(pregunta_id):
            return jsonify({
                'status': 'success',
                'message': 'Pregunta eliminada correctamente'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Error eliminando pregunta'
            })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


@app.route('/api/obtener-pregunta/<int:pregunta_id>')
def api_obtener_pregunta(pregunta_id):
    """Obtiene una pregunta específica por ID"""
    try:
        pregunta = db_manager.obtener_pregunta_por_id(pregunta_id)

        if pregunta:
            return jsonify({
                'status': 'success',
                'data': pregunta
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Pregunta no encontrada'
            })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


@app.route('/api/actualizar-pregunta', methods=['POST'])
def api_actualizar_pregunta():
    """Actualiza una pregunta existente"""
    try:
        data = request.get_json()

        pregunta_id = data.get('id')
        nueva_pregunta = data.get('pregunta')
        nuevo_nivel = data.get('nivel')
        nuevo_tipo = data.get('tipo')

        if not pregunta_id:
            return jsonify({
                'status': 'error',
                'message': 'ID de pregunta requerido'
            })

        if db_manager.actualizar_pregunta(pregunta_id, nueva_pregunta, nuevo_nivel, nuevo_tipo):
            return jsonify({
                'status': 'success',
                'message': 'Pregunta actualizada correctamente'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Error actualizando pregunta'
            })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


@app.route('/api/importar-datos', methods=['POST'])
def api_importar_datos():
    """Importa datos desde un archivo JSON"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No se proporcionó archivo'
            })

        file = request.files['file']

        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'Nombre de archivo vacío'
            })

        # Leer contenido del archivo
        content = file.read().decode('utf-8')
        data = json.loads(content)

        # Validar estructura
        if 'preguntas' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Formato de archivo inválido'
            })

        # Importar preguntas
        total_importadas = 0
        for habilidad, niveles in data['preguntas'].items():
            for nivel, preguntas in niveles.items():
                for pregunta in preguntas:
                    if db_manager.agregar_pregunta(habilidad, pregunta, 'general', nivel):
                        total_importadas += 1

        return jsonify({
            'status': 'success',
            'message': f'Importadas {total_importadas} preguntas correctamente'
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })


@app.route('/api/health')
def api_health():
    """Endpoint de salud para verificar que la API está funcionando"""
    return jsonify({
        'status': 'success',
        'message': 'API funcionando correctamente',
        'timestamp': datetime.now().isoformat(),
        'modulos_disponibles': MODULOS_DISPONIBLES
    })


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint no encontrado'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Error interno del servidor'
    }), 500


@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Solicitud inválida'
    }), 400


if __name__ == '__main__':
    print("🚀 Inicializando Servidor Web del Agente Entrevistador...")
    print("=" * 60)

    if inicializar_sistema():
        print("✅ Sistema inicializado correctamente")
        total_preguntas = db_manager.contar_preguntas()
        total_habilidades = len(db_manager.obtener_todas_habilidades())

        print(f"📊 Estado actual:")
        print(f"   • {total_preguntas} preguntas en base de datos")
        print(f"   • {total_habilidades} habilidades disponibles")
        print("=" * 60)
        print("🌐 Servidor disponible en: http://localhost:5000")
        print("📱 Interfaz web moderna y responsive")
        print("🔧 API REST completa disponible")
        print("📋 Presiona Ctrl+C para detener el servidor")
        print("=" * 60)

        # Configuración del servidor
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=True,
            use_reloader=True,
            threaded=True
        )
    else:
        print("❌ Error inicializando sistema")
        print("💡 Soluciones posibles:")
        print("   1. Verifica que database_manager.py esté presente")
        print("   2. Verifica que data_loader.py esté presente")
        print("   3. Asegúrate de que el entorno virtual esté activado")
        print("   4. Ejecuta: pip install -r requirements.txt")