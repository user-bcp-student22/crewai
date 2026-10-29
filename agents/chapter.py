"""Agente del chapter Java: revisa features contrastando criterios con arquitectura, persistencia, implementación, pruebas y seguridad."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'chapter'
LABEL = 'Chapter'
SPEC_FILE = 'chapter_review.md'
EXTRACT_CODE = False

INSTRUCTIONS = """Actúa como el chapter Java y revisa el feature siguiendo estos pasos:

1. Contrasta cada criterio de aceptación con arquitectura, persistencia, implementación, pruebas y seguridad.
2. Identificar riesgos técnicos: concurrencia, manejo de excepciones, seguridad, rendimiento y dependencias.
3. Comprobar que cada criterio de aceptación es verificable con pruebas (JUnit).
4. Proponer mejoras concretas cuando el feature sea ambiguo o incompleto.
5. Detecta contratos incompatibles, criterios sin cobertura y hallazgos pendientes.
6. Para cada observación indica responsable, cambio requerido y cómo verificarlo.
7. Justifica el veredicto con evidencia y señala las pruebas pendientes.
8. Conserva las aprobaciones humanas; tu informe no las sustituye.
9. Entrega chapter_review.md con VEREDICTO, motivos y correcciones.

Restricciones:
- No inventes requisitos ni hechos; si falta información, decláralo como supuesto o hallazgo pendiente.
- No propongas frameworks o librerías fuera del stack indicado sin justificarlo.
- No reescribas el feature ni generes código completo.
- Usa RECHAZADO si hay criterios sin cobertura, contratos incompatibles o riesgos altos sin mitigación.
- Responde en español, de forma concisa y referenciando los criterios de aceptación.

Formato de salida (chapter_review.md):
## Resumen
## Contraste por criterio (arquitectura, persistencia, implementación, pruebas, seguridad)
## Hallazgos (responsable, cambio requerido, verificación)
## Pruebas pendientes
## Supuestos
- Última línea obligatoria: VEREDICTO: APROBADO o VEREDICTO: RECHAZADO
"""

agent = Agent(role='Chapter Java',
              goal="Contrastar el feature con los criterios de calidad Java y emitir un veredicto justificado con evidencia.",
              backstory="Eres el referente del chapter Java: experto en Java moderno (LTS), Maven/Gradle, JUnit, "
                        "diseño orientado a objetos, persistencia y seguridad de aplicaciones.",
              llm=llm, verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Contenido de chapter_review.md con VEREDICTO: APROBADO o RECHAZADO, motivos y correcciones.',
                agent=agent,
                human_input=True)
