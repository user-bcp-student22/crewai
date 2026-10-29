"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'frontend'
LABEL = 'Desarrollador frontend'
SPEC_FILE = 'frontend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = """Implementa el recorrido del usuario de la feature según el contrato de API aprobado en el paso de Arquitectura (ruta, método, cuerpo, respuestas y códigos de error).
No inventes endpoints, campos ni códigos de error que no estén en ese contrato. Si falta algo, decláralo como supuesto pendiente en frontend_spec.md.

1. Recorrido, campos, validaciones, acciones y mensajes
- Describe paso a paso el recorrido: pantalla inicial, acción principal, respuesta exitosa y destino.
- Lista cada campo con nombre, tipo de control, etiqueta visible, obligatoriedad, formato y longitud según el contrato.
- Lista las validaciones de cliente (obligatoriedad, formato, longitud). Aclara que son una ayuda para el usuario: el servidor siempre valida y autoriza.
- Define cada acción (botón, enlace, envío) con su petición HTTP, su precondición y su resultado.
- Define los mensajes exactos en español para cada validación y cada error del contrato. No muestres detalles técnicos ni datos sensibles.

2. Estados obligatorios
- Carga: indicador visible y anunciado a lectores de pantalla; los controles se deshabilitan mientras dura la petición.
- Vacío: qué se muestra cuando no hay datos, con texto y una acción sugerida.
- Éxito: confirmación visible y siguiente paso.
- Error: mensaje junto al campo cuando es de validación; mensaje general cuando es de servidor o de red. Conserva los datos ingresados.
- Evita envíos duplicados: deshabilita el botón al enviar, ignora clics repetidos mientras la petición está en curso (por ejemplo con exhaustMap) y reactiva el control solo al terminar.

3. Accesibilidad y teclado
- Cada control tiene un label asociado (for/id) o aria-label. Los errores se enlazan con aria-describedby y aria-invalid="true".
- Mensajes de estado en una región aria-live="polite"; errores generales con role="alert".
- Orden de tabulación lógico; todo lo accionable se usa con teclado; Enter envía el formulario.
- Foco visible: no elimines el contorno. Usa :focus-visible con contraste suficiente.
- Tras éxito o error, mueve el foco al mensaje o al encabezado de la pantalla.
- Contraste de texto mínimo WCAG AA (4.5:1).

4. Código Angular 17 (componentes standalone)
- El andamiaje ya existe: main.ts hace bootstrapApplication(AppComponent) con provideRouter(routes) y provideHttpClient(withInterceptorsFromDi()). Si el recorrido necesita rutas, entrega app.routes.ts que exporte `routes` y app.component.ts que exporte `AppComponent`.
- Usa formularios reactivos con validadores, HttpClient y servicios inyectables. No uses `any`.
- La URL de la API va en una constante, no repetida en cada llamada. El backend escucha en http://localhost:8080 y tiene CORS para http://localhost:4200.
- Plantillas (.html) y estilos (.css) se entregan como archivos separados del componente.
- Nombres de archivo en kebab-case con sufijo de rol: .component.ts, .component.html, .component.css, .service.ts, .guard.ts, .interceptor.ts, models.ts. Sin carpetas en el nombre.

5. Cómo comprobar el recorrido y sus errores
- Tabla de casos con entrada, acción y resultado esperado para cada criterio de aceptación.
- Casos de error: validación de campo, 4xx, 5xx, red sin conexión, doble clic en enviar y estado vacío.
- Comandos reproducibles en texto: cd frontend-angular, npm install, npx ng build, npx ng test --watch=false.
- Lista de comprobación de accesibilidad: solo teclado, lector de pantalla y foco visible.
- No afirmes que una prueba pasó sin salida real. Marca como NO EJECUTADO lo que no se haya ejecutado. La persona que revisa ejecuta las pruebas y conserva la evidencia.

6. Formato de entrega
- Primero frontend_spec.md: markdown con las secciones 1, 2, 3 y 5. No incluyas bloques de código en el documento.
- Después, el código en bloques ```typescript, ```html o ```css. Un bloque por archivo, sin repetir archivos.
- La primera línea de cada bloque es el nombre del archivo como comentario: // nombre.component.ts en TypeScript, <!-- nombre.component.html --> en HTML y /* nombre.component.css */ en CSS.
- No pongas carpetas en esa línea; el sistema asigna la ruta."""

agent = Agent(role='Desarrollador frontend', goal="Entregar frontend_spec.md y el código Angular del recorrido de usuario, alineados con el contrato de API aprobado, con estados, accesibilidad y pruebas verificables.",
              backstory="Eres el desarrollador frontend del equipo y trabajas con Angular 17 y componentes standalone. No inventas contratos, pantallas ni resultados de pruebas. Cuando algo falta, lo declaras como pendiente.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='frontend_spec.md en markdown seguido de bloques ```typescript, ```html o ```css; un bloque por archivo y primera línea con // nombre.component.ts (o <!-- nombre.component.html --> / /* nombre.component.css */).', agent=agent)
