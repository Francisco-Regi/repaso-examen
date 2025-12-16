from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# DATOS LITERALES DEL DOCUMENTO "GUIA DE EXTRAORDINARIO" 
BD_PREGUNTAS = [
    # --- PARES (Pregunta -> Respuesta) ---
    {
        "t": "pair", 
        "q": "1.Este se ejecuta entre la entidad administrativa y el dispositivo administrado permitiendo a la entidad administradora consultar el estado de los dispositivos e indirectamente realizar acciones en dichos a través de los agentes", 
        "a": "Protocolo de Administración"
    },
    {
        "t": "pair", 
        "q": "2.Define los indicadores de prestaciones, realiza el análisis global de la calidad de servicios y toma de decisiones para corregir desviaciones, preparan los procedimientos de operadores y administradores", 
        "a": "Analistas"
    },
    {
        "t": "pair", 
        "q": "3.Herramienta de seguimiento de incidencias que permitan conocer el estado actual de incidencias y elaborar informes de actividad operacional para su posterior análisis", 
        "a": "Control de operadores"
    },
    {
        "t": "pair", 
        "q": "4.Este proceso está relacionado con la modificación de parámetros y provoca acciones por parte de los sistemas qué componen la configuración a gestionar, para ello se apoya de la gestión de configuración, información de configuración y mantenimiento de la seguridad", 
        "a": "Control de la red"
    },
    {
        "t": "pair", 
        "q": "5.Proporciona seguridad tanto a nivel de los computadores como nivel de red, para los recursos sujetos a gestión. De este se deriva la seguridad del orden y la seguridad de red", 
        "a": "Control de seguridad"
    },
    {
        "t": "pair", 
        "q": "6.Se encarga del análisis de informes técnico-económicos, establecimiento de política de telecomunicaciones, asignación de presupuesto y elección de criterios de distribución de costes o facturación", 
        "a": "Planificadores"
    },
    {
        "t": "pair", 
        "q": "7.Está a cargo de la iniciativa no, mantenimiento y cierre de componentes individuales y subsistemas lógicos dentro de la configuración completa de la red.", 
        "a": "Control de configuración"
    },
    {
        "t": "pair", 
        "q": "8.Es una parte del equipamiento de la red, incluye el software, reside en la red administrada. También puede ser un host, un switch, un puente, un Hub, una impresora o un módem", 
        "a": "Disposit admin"
    },
    {
        "t": "pair", 
        "q": "9.Describe la naturaleza y estado de los recursos que son de interés para la gestión de red, cómo: los recursos físicos, los recursos lógicos y los atributos", 
        "a": "Información de configuración"
    },
    {
        "t": "pair", 
        "q": "10.Dentro de sus funciones se encuentra el soporte a usuarios, recogida y evaluación de alarmas, ejecución programada de pruebas preventivas, modificación de configuración, etc.", 
        "a": "Operadores"
    },
    {
        "t": "pair", 
        "q": "11.Lugar donde se almacenan los datos referentes a los objetos administrados.", 
        "a": "Base de información de administración"
    },
    {
        "t": "pair", 
        "q": "12.Aplicación con control humano que se ejecuta en una estación centralizada de administración de red, este es el lugar donde se realiza la actividad de la administración de red, controla la recolección, procesamiento, análisis y/o visualización de la información de administración", 
        "a": "Entidad administradora"
    },
    {
        "t": "pair", 
        "q": "13.En este proceso se define qué equipos tendrán la función de servidores y cuáles la d estaciones clientes de acuerdo a las necesidades de cada departamento; se define las relaciones con otros grupos o dominios de la red en lo referente al uso de recursos, así como de la comunicación", 
        "a": "Organización de la red"
    },
    {
        "t": "pair", 
        "q": "14.Tiene como propósito fijar las metas de los niveles administrativos que tengan relación con el proyecto, seleccionar la metodología apropiada, levantamiento de entrevista, prioridades para la implementación del proyecto, entre otros", 
        "a": "Planificación de la red"
    },
    {
        "t": "pair", 
        "q": "15.Procesos residente que se ejecuta en cada dispositivo administrado y que se comunica con la entidad administradora, realizando acciones locales bajo el control de los comandos", 
        "a": "Agente de administración de red"
    },

    # --- SECCIÓN VERDADERO / FALSO (Afirmaciones completas) ---
    # Según tu doc: "Falso/gestión de prestaciones" significa que la afirmación es FALSA.
    {
        "t": "false", 
        "q": "16. La gestión de configuración prevé el desarrollo de pruebas preventivas de conectividad, integridad de datos, Integridad de protocolos, saturación de datos, etc."
    },
    {
        "t": "true",  
        "q": "17. Dentro de las tareas de la gestión de prestaciones Están: establecimiento de nivel de la calidad de servicio y métricas, monitorización de recursos para la detección de cuellos de botella y desbordamiento de umbrales; establecimiento de planes, medidas y cambios de planificación"
    },
    {
        "t": "true",  
        "q": "18. Algunas de las tareas de gestión de seguridad son: realizar el análisis de amenazas, comprobación de identidad, establecimiento y exigencia de control de acceso, confidencialidad e integridad de los datos"
    },
    {
        "t": "false", 
        "q": "19. La gestión de contabilidad trata de la protección de los recursos de la compañía a fin de proteger información, infraestructura IT, servicios y producción de amenazas de ataques o uso inadecuado"
    },
    {
        "t": "true",  
        "q": "20. La gestión de configuración prevé la gestión SLAs, contratos entre cliente/proveedor o entre proveedores sobre servicios a proporcionar y calidades asociadas"
    },
    # Doc dice "Falso/fallos", así que la respuesta correcta es FALSO
    {
        "t": "false", 
        "q": "21. Entre las tareas que comprende la gestión de prestación están: monitorización de red y estado, responder y reaccionar a las alarmas, establecer medidas de recuperación, asistencia a usuarios"
    },
    {
        "t": "true",  
        "q": "22. Las tareas de la gestión de contabilidad comprende: recopilación de datos de uso, mantenimiento de cuentas y logs, estadísticas de uso, políticas de cuentas y tarifas"
    },
    {
        "t": "true",  
        "q": "23. La gestión de prestaciones tiene como tarea s instalar nuevo SW, retocar viejo SW, conectar dispositivos, cambios en topología y tráfico, control SW, de aspectos que acompañan a la instalación física"
    },
    {
        "t": "true",  
        "q": "24. La gestión de configuración incluye la gestión de inventario, gestión de topología y gestión de servicios de directorio"
    },
    {
        "t": "true",  
        "q": "25. La administración de usuarios se basa en: autentificación, autorización, customización son objetivos de la gestión de contabilidad"
    },

    # --- CONTINUACIÓN PARES (Del 26 al 45) ---
    {
        "t": "pair", 
        "q": "26.Un agente manda la información al nodo administrador puntualmente, ante una situación predeterminada", 
        "a": "Trap"
    },
    {
        "t": "pair", 
        "q": "27.Protocolo de capa de aplicación diseñada para comunicar entre el administrador y el agente", 
        "a": "Protocolo de administración"
    },
    {
        "t": "pair", 
        "q": "28.Consta de muy diversos tipos de equipos de telecomunicaciones analógicas y digitales y equipos soporte asociados como sistemas de transmisión, sistemas de conmutación, multiplexores, terminales de señalización, entre otros", 
        "a": "Redes de telecomunicaciones"
    },
    {
        "t": "pair", 
        "q": "29.La estación administradora envié una solicitud a un agente pidiéndole información o mandándole a actualizar su estado de cierta manera; la información recibida del agente es la respuesta o la confirmación a la acción solicitada", 
        "a": "Sondeo/polling"
    },
    {
        "t": "pair", 
        "q": "30.El puerto-----se utiliza para las transmisiones tipo sondeo", 
        "a": "161"
    },
    {
        "t": "pair", 
        "q": "31.Contemplar el control y coordinación de un subconjunto de elementos de red; mantenimiento de datos estadísticos, registros y otros datos acerca de un conjunto de elementos de red; y se sitúa todo el equipamiento que forma parte de la red: conmutadores, routers, multiplexores, infraestructura SDH, etc.", 
        "a": "Elementos de red"
    },
    {
        "t": "pair", 
        "q": "32.los operadores de telecomunicaciones precisan de una infraestructura de gestión singular, este entorno de gestión debe contemplar el fin último de sus redes; el modelo clásico de gestión orienta sus tareas hacia la red: configuración, mantenimiento y ocasionalmente análisis de rendimiento.", 
        "a": "Gestión de red y servicios"
    },
    {
        "t": "pair", 
        "q": "33.Interconectividad, servicios relacionados con objetos, heterogeneidad, cambios dinámicos y es cala enorme son:", 
        "a": "Características de IoT"
    },
    {
        "t": "pair", 
        "q": "34.Es un protocolo de administración de red utilizado ampliamente por las personas a cargo de los entornos de redes de telecomunicaciones y se desarrollan labores de análisis de mercado, planificación y definición de servicios", 
        "a": "CMIP"
    },
    {
        "t": "pair", 
        "q": "35.Cuida las relaciones con el cliente e interfaz con otras administraciones, la interacción con proveedores de servicios y mantenimiento de datos estadísticos", 
        "a": "Gestión de servicios"
    },
    {
        "t": "pair", 
        "q": "36.Base de datos en relación a l que contiene información del estado de un nodo administrado y es actualizado por un agente SNMP", 
        "a": "MIB"
    },
    {
        "t": "pair", 
        "q": "37.Soporte para proceso de toma de decisiones e inversión y utilización óptima, gestión de presupuesto de telecomunicaciones y desarrollan labores de análisis de mercado, planificación y definición de servicios", 
        "a": "Gestión empresarial"
    },
    {
        "t": "pair", 
        "q": "38.Conectividad basada en la identificación, compatibilidad, configuración automática de servicios y capacidades basadas en la ubicación y seguridad son:", 
        "a": "Requisitos de alto nivel de IoT"
    },
    {
        "t": "pair", 
        "q": "39.Facilita la comunicación entre la estación administradora y el agente de un dispositivo de red, permitiendo que los agentes transmitan datos estadísticos a través de la red al estación de administración", 
        "a": "SNMP"
    },
    {
        "t": "pair", 
        "q": "40.Tiene como responsabilidad gestionar un subconjunto de elementos de red, desarrollando tareas de configuración, gestión de alarmas, registros de actividad; además es capaz de comunicar con el nivel superior mediante el empleo de una interfaz estandarizado, siendo este Q3", 
        "a": "Gestión de elementos"
    },
    {
        "t": "pair", 
        "q": "41.Protocolo para la monitorización remota de redes, es un estándar que define objetivos actuales e históricos de control, permitiendo la captura de información en tiempo real", 
        "a": "RMON"
    },
    {
        "t": "pair", 
        "q": "42.El puerto---------se utiliza para los mensajes de tipo interrupción", 
        "a": "162"
    },
    {
        "t": "pair", 
        "q": "43.Proporciona una estructura de red organizada para conseguir la interconexión de los diversos tipos de sistemas de operaciones y equipos de telecomunicación usando una arquitectura estándar e interfaces normalizadas", 
        "a": "Objetivos de TMN"
    },
    {
        "t": "pair", 
        "q": "44.Es el proceso de los dispositivos que están siendo monitorizados, puentes, routers, hubs, and switches", 
        "a": "Agente de administración"
    },
    {
        "t": "pair", 
        "q": "45.Además de las habituales tareas de mantenimiento, c desarrollan los servicios que serán ofrecidos a la capa superior. Comunica con los niveles superior e inferior mediante Q3", 
        "a": "Gestión de redes"
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/cartas')
def obtener_cartas():
    cartas = []
    # Generación dinámica de cartas según el tipo
    for i, item in enumerate(BD_PREGUNTAS):
        if item['t'] == 'pair':
            # Crea 2 cartas: Pregunta y Respuesta
            cartas.append({"id": f"{i}_q", "match_id": i, "txt": item['q'], "type": "pair"})
            cartas.append({"id": f"{i}_a", "match_id": i, "txt": item['a'], "type": "pair"})
        else:
            # Crea 1 carta solitaria para Verdadero/Falso
            cartas.append({"id": f"{i}_tf", "match_id": i, "txt": item['q'], "type": item['t']})
    
    random.shuffle(cartas)
    return jsonify(cartas)

if __name__ == '__main__':
    app.run(debug=True)