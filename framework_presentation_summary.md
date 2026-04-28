# Arquitectura y Lineamientos: Multi-Agent Assembly Line Framework

> **Estado del Proyecto:** ✅ Funcional | 🧪 Fase Experimental

Este documento consolida la arquitectura, diseño y lineamientos del framework agéntico integrado nativamente en VS Code GitHub Copilot Chat. Está diseñado siguiendo estrictamente los lineamientos de **GitHub Copilot**, mejores prácticas de **Prompt Engineering**, y estrategias de mitigación de alucinaciones.

---

## 1. Arquitectura Base y Orquestación

El framework opera directamente en la carpeta `.github/` de los repositorios sin interferir con flujos de trabajo existentes (como `workflows/` o `CODEOWNERS`). Utiliza un equipo de 9 agentes especializados, orquestados bajo el paradigma **"Strategy First"**. 

**Modos de Ejecución:**
1. **Subagent Pipeline (Mode 1):** Orquestación mediante el `@dispatcher`. Los agentes operan de forma secuencial o paralela en contextos estrictamente aislados, retornando solo resúmenes para evitar saturación de memoria.
2. **Compact Session (Mode 2):** Trabajo continuo en una sola ventana (ideal para refactors directos).
3. **Parallel Worktrees (Mode 3):** Aislamiento duro en ramas Git (`git worktree`) y persistencia transversal (cross-session) de estado utilizando memoria en disco.

---

## 2. Gestión de Assets, Discovery y Data Curation

Para garantizar la viabilidad del framework y mitigar la "ceguera por saturación de contexto" de los Modelos de Lenguaje (LLMs), se eliminaron los índices masivos del código fuente.

* **Mapas Topográficos (`atlas.tson`):** En lugar de inyectar todo el proyecto, los agentes leen un mapa estructural ligero que les permite orientarse.
* **Búsqueda Bajo Demanda (`discovery.py`):** El agente explora proactivamente los componentes o "skills" que necesita mediante scripts deterministas, garantizando un contexto *Zero-Shot* quirúrgico.
* **Curación de Datos:** Los archivos de contexto se inyectan dinámicamente según el rol activo. `@frontend-coder` no verá las reglas de base de datos, optimizando el consumo de tokens.

---

## 3. Estandarización a Python y Formato Ligero (TSON)

Alineados con el objetivo de facilitar el mantenimiento a todo el equipo, se adoptaron dos estándares arquitectónicos críticos:

* **Pure Python Runtime:** Todo el motor de automatización de contexto y generación de índices (scripts en `.github/hooks/scripts/`) opera **100% en Python**. Se eliminó Node.js (`.mjs`) por completo. Ya que herramientas como macOS y distribuciones Linux traen Python preinstalado, cualquier desarrollador (Frontend, Backend o DevOps) puede correr los flujos localmente.
* **Formato Estándar TSON:** JSON y YAML anidados introducen ruido cognitivo innecesario para la IA. Se migró toda la persistencia transversal y los mapas de estado (ej. `active_state.tson`, `local_dispatcher_state.tson`) al formato TSON (derivado de TOML). Es extremadamente ligero y fácil de consumir por Copilot.

---

## 4. Estructura de Archivos y Metadatos (Prompt Engineering)

El diseño de las instrucciones aprovecha metadatos (Frontmatter) para una activación condicional inteligente:

* **Agentes (`agents/*.agent.md`):** Definen la identidad y filosofía del agente. Utilizan un bloque YAML inicial que expone su `description` (prompt de activación) y las `tools` permitidas para su rol.
* **Instrucciones Permanentes (`instructions/*.instructions.md`):** Reglas siempre activas (ej. guías de estilo). Usan el atributo `applyTo: "**/*.py"` para inyectarse al contexto solo si el desarrollador abre o edita un archivo Python.
* **Habilidades Modulares (`skills/*/SKILL.md`):** Conocimiento y workflows almacenados en disco (ej. `a11y-checklist`). Contienen en su metadata a qué `roles` pertenecen, cargándose dinámicamente en memoria solo si el agente los solicita.

---

### Conclusión para el Equipo

Esta configuración representa el siguiente paso evolutivo en el uso de Copilot. Pasamos de *autocompletado pasivo* a **agentes autónomos asilados**. Con la migración a Python y la estandarización en TSON y `discovery.py`, el framework no solo inyecta el contexto correcto, sino que protege la ventana del LLM de ruido irrelevante, manteniéndolo ligero y altamente enfocado.
