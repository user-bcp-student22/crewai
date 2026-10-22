"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'testing'
LABEL = 'Ingeniero de pruebas'
SPEC_FILE = 'testing_report.md'
EXTRACT_CODE = True

INSTRUCTIONS = """Relaciona cada criterio de aceptación con uno o más casos de prueba identificables.
Incluye pruebas positivas, negativas, de borde e integración; para cada caso indica
preparación, datos, pasos, resultado esperado y resultado real. Comprueba contratos
de API y persistencia, así como las correcciones propuestas. Incluye comandos
reproducibles y limpieza. No inventes ejecuciones: escribe NO EJECUTADO cuando no
haya salida real. Entrega testing_report.md y los archivos de prueba correspondientes."""
agent = Agent(role='Ingeniero de pruebas', goal="Completar la tarea asignada.",
              backstory="Eres un integrante del equipo.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Un informe de pruebas.', agent=agent)
