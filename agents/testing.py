"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'testing'
LABEL = 'Ingeniero de pruebas'
SPEC_FILE = 'testing_report.md'
EXTRACT_CODE = True

INSTRUCTIONS = """Diseña pruebas verificables para la feature usando sus criterios de aceptación y el contexto aprobado disponible (arquitectura, API, backend, persistencia, seguridad y feedback humano).

Entrega testing_report.md con estas secciones:
1. Alcance, supuestos, dependencias y contratos de referencia. No inventes rutas, esquemas, estados, respuestas ni reglas que no aparezcan en los requisitos o el contexto; señala lo que falte.
2. Trazabilidad: relaciona cada criterio de aceptación, sin omitir ninguno, con uno o más casos de prueba y su resultado esperado. Identifica criterios como CA-1, CA-2 y casos como CP-1.
3. Casos positivos, negativos, de borde e integración. Incluye cada categoría; si alguna no aplica, justifica por qué con relación a la feature.
4. Preparación reproducible: requisitos, configuración, dependencias, servicios, estado inicial, datos de prueba y cómo restaurar o aislar el entorno.
5. Para cada caso: criterio asociado, tipo, precondiciones, datos concretos, pasos/acción, comando reproducible, resultado esperado y resultado real. Distingue claramente lo esperado de lo observado.
6. Contratos y correcciones: verifica solicitudes, respuestas y errores de API contra el contrato aprobado; verifica persistencia, restricciones, integridad y migración/reversión cuando estén definidas. Convierte cada corrección propuesta en una prueba de regresión que falle antes y pase después, pero no afirmes que la corrección está aplicada sin evidencia.
7. Limpieza: indica cómo borrar/restaurar datos temporales, detener servicios y retirar recursos creados.
8. Resumen de ejecución, fallos, bloqueos y cobertura pendiente.

Entrega también pruebas automatizadas ejecutables, en bloques de código con nombre de archivo, y comandos para instalarlas/prepararlas y ejecutarlas. Usa la tecnología y convenciones del proyecto; si no están disponibles, explica qué falta y no presentes pseudocódigo como prueba ejecutable. Cada comando debe indicar desde qué directorio se ejecuta y cualquier variable/configuración necesaria.

Honestidad de ejecución: marca cada caso como NO EJECUTADO cuando no exista una salida real obtenida al ejecutarlo. Solo registra EJECUTADO y un resultado real si cuentas con la salida/evidencia de esa ejecución; no simules comandos, resultados, cobertura ni correcciones. Si solo propones una prueba, incluye su resultado esperado y marca su estado NO EJECUTADO. No uses datos reales ni secretos."""
agent = Agent(role='Ingeniero de pruebas', goal="Traducir todos los criterios de aceptación en pruebas reproducibles con resultados esperados y evidencia honesta.",
              backstory="Eres responsable de verificar el comportamiento y los contratos de la feature. Contrastas las pruebas con las especificaciones aprobadas, haces visibles los supuestos y nunca inventas ejecuciones ni resultados.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='testing_report.md con trazabilidad completa de criterios a casos y resultados esperados, cobertura positiva/negativa/de borde/integración, preparación, datos, comandos, limpieza y estados de ejecución honestos; además, pruebas automatizadas ejecutables con comandos reproducibles. Marca NO EJECUTADO si no hay salida real.', agent=agent)
