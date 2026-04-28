# Multi-Agent Assembly Line Framework (Hybrid v2)

![version](https://img.shields.io/badge/version-1.1.0-blue)

Framework de agentes especializados para VS Code Copilot Chat. Agrega la carpeta `.github/` a cualquier repositorio y obtén un equipo de 9 agentes con roles, permisos y conocimiento separados.

## Requisitos

- **VS Code** con GitHub Copilot Chat
- **Python 3.10+** (o `uv`) — para los scripts de automatización y contexto

## Instalación

```bash
# 1. Copia la carpeta .github/ a tu repositorio
cp -r copilot-dev/.github tu-proyecto/.github

# 2. Genera los índices de contexto (nativamente en Python)
cd tu-proyecto
bash .github/hooks/scripts/sync_agents.sh

# 3. (Opcional) Inicializa skills e instructions específicos de tu proyecto
# En Copilot Chat:
#   @copilot /copilot-init
```

Si tu repo ya tiene `.github/workflows/`, `ISSUE_TEMPLATE/`, `CODEOWNERS`, etc., **no hay conflicto** — el framework solo agrega sus propios directorios (`agents/`, `skills/`, `instructions/`, `hooks/`, `prompts/`) y el archivo `copilot-instructions.md`.

Los índices se regeneran automáticamente al final de cada sesión de agente gracias al Copilot hook en `.github/hooks/sync-on-stop.tson`.

## Actualización

### Upgrade normal (ya tienes v1.1.0+)

Si tu proyecto ya tiene `upgrade.sh` (instalado desde v1.1.0):

```bash
# Actualizar a una versión específica
bash .github/hooks/scripts/upgrade.sh v1.2.0

# O actualizar a la última versión de main
bash .github/hooks/scripts/upgrade.sh
```

### Primera vez (upgrade desde versión anterior a v1.1.0)

Si tu proyecto tiene una versión vieja del framework que **no incluye** `upgrade.sh`:

```bash
# 1. Copia los 2 archivos nuevos desde tu copia local de copilot-dev:
cp copilot-dev/.github/.copilot-dev.tson  tu-proyecto/.github/
cp copilot-dev/.github/hooks/scripts/upgrade.sh  tu-proyecto/.github/hooks/scripts/

# 2. Ahora corre el upgrade normalmente:
cd tu-proyecto
bash .github/hooks/scripts/upgrade.sh main
```

A partir de ese momento, `upgrade.sh` se auto-actualiza — no necesitas repetir el paso manual.

### Repos privados

Si el repositorio del framework es privado, necesitas autenticarte:

```bash
# Opción 1 (recomendada): gh CLI — se auto-autentica
# Instalar: https://cli.github.com
gh auth login
bash .github/hooks/scripts/upgrade.sh v1.2.0

# Opción 2: token manual
export GITHUB_TOKEN=ghp_xxxxx
bash .github/hooks/scripts/upgrade.sh v1.2.0
```

### ¿Qué toca y qué no toca?

El script **solo actualiza archivos del framework** (listados en `.github/.copilot-dev.tson`):

| ✅ Se actualiza (framework) | ❌ No se toca (tuyo) |
|---|---|
| `agents/*.agent.md` (los 9 del framework) | `workflows/deploy.yml` |
| `skills/*/SKILL.md` (los del framework) | `ISSUE_TEMPLATE/` |
| `hooks/scripts/*` | `CODEOWNERS` |
| `copilot-instructions.md` | `dependabot.yml` |
| `instructions/*.instructions.md` (las 4 del framework) | `PULL_REQUEST_TEMPLATE.md` |

Agentes, skills e instructions **que tú creaste** (no están en el manifest) nunca se eliminan ni se modifican.

### Archivos legacy y migración

Si el upgrade detecta archivos en formato antiguo (ej: `agents/dispatcher.md` → debería ser `agents/dispatcher.agent.md`), el script te avisa pero **no los elimina**:

```
⚠ agents/dispatcher.md (formato legacy detectado)

📋 Para migrarlos de forma segura, abre Copilot Chat y ejecuta:
   @copilot /copilot-upgrade
```

El prompt `/copilot-upgrade` analiza tus archivos legacy, preserva contenido custom que hayas agregado, los migra al formato nuevo, genera un perfil de proyecto (`project_profile`) para filtrar skills irrelevantes, y limpia los archivos obsoletos — todo con tu confirmación.

### Backups

Si el upgrade modifica un archivo que tú habías personalizado, crea un backup automático:

```bash
# Ver diferencias
diff .github/copilot-instructions.md .github/copilot-instructions.md.pre-upgrade

# Restaurar si prefieres tu versión
cp .github/copilot-instructions.md.pre-upgrade .github/copilot-instructions.md

# Limpiar backups cuando estés satisfecho
rm .github/**/*.pre-upgrade
```

Consulta el [CHANGELOG](CHANGELOG.md) para ver qué cambió en cada versión.

## Agentes

| Agente | Rol | Herramientas |
|--------|-----|-------------|
| `@dispatcher` | Orquestador. Analiza tareas y coordina agentes via subagents. | read, search, execute, todo, **agents** |
| `@tech-lead` | Arquitectura y scaffolding. Define ADRs e interfaces. | read, search (solo lectura) |
| `@backend-coder` | Implementación backend: APIs, servicios, lógica de negocio. | read, search, edit, execute |
| `@frontend-coder` | Implementación frontend: UI, componentes, estilos, a11y. | read, search, edit, execute |
| `@htmx-prototyper` | Prototipado server-side: FastAPI + HTMX + Jinja2. | read, search, edit, execute |
| `@ux-lead` | Specs de diseño UI/UX para `@frontend-coder`. | read, search (solo lectura) |
| `@appsec` | Auditoría de seguridad (OWASP, RBAC). Reporta, no modifica. | read, search (solo lectura) |
| `@qa` | Tests y edge cases. Escribe y ejecuta pruebas. | read, search, edit, execute |
| `@devops` | Infra, CI/CD, migraciones, cleanup. | read, search, edit, execute |

## Modos de Ejecución

| Modo | Cuándo usarlo | Mecanismo |
|------|--------------|-----------|
| **Mode 1 — Subagent Pipeline** | Feature completo (multi-paso) | `@dispatcher` invoca subagentes con contexto aislado |
| **Mode 2 — Compact Session** | Tarea puntual en un solo agente | Invocas directo: `@backend-coder arregla el endpoint` |
| **Mode 3 — Parallel Worktrees** | Trabajo en paralelo entre sesiones | Estado persistido en `active_state.tson` |

## Estructura

```
.github/
├── copilot-instructions.md            # Directivas universales (siempre activas)
│
├── agents/                            # 9 AGENTES ESPECIALIZADOS
│   ├── dispatcher.agent.md
│   ├── tech-lead.agent.md
│   ├── backend-coder.agent.md
│   ├── frontend-coder.agent.md
│   ├── htmx-prototyper.agent.md
│   ├── ux-lead.agent.md
│   ├── appsec.agent.md
│   ├── qa.agent.md
│   ├── devops.agent.md
│   └── assets/                        # Índices dinámicos (generados por scripts)
│       ├── *_index.tson               # Mapas de rutas del repo por rol
│       ├── *_skills.tson              # Skills disponibles por rol
│       └── copilot_runtime.tson       # Slash commands y modelos disponibles
│
├── skills/                            # CONOCIMIENTO ON-DEMAND (SKILL.md folders)
│   ├── architecture-patterns/SKILL.md
│   ├── component-patterns/SKILL.md
│   ├── context-handoff/SKILL.md       # + references/ para carga progresiva
│   ├── a11y-checklist/SKILL.md
│   └── frontend-performance/SKILL.md
│
├── instructions/                      # REGLAS ALWAYS-ON (por glob pattern)
│   └── python.instructions.md         # applyTo: "**/*.py" — uv, type hints, etc.
│
├── prompts/                           # TAREAS ONE-SHOT
│   ├── copilot-init.prompt.md         # Genera instrucciones/skills para un repo nuevo
│   └── copilot-upgrade.prompt.md      # Migra archivos legacy y genera project profile
│
├── .copilot-dev.tson                  # Manifest: lista de archivos del framework
│
├── hooks/scripts/                     # AUTOMATIZACIÓN (Pure Python)
│   ├── sync_agents.sh                 # Punto de entrada — orquestador bash
│   ├── upgrade.sh                     # Actualiza solo archivos del framework
│   ├── blueprint.py                   # Scaffold para inicializar el proyecto
│   ├── discovery.py                   # Búsqueda bajo demanda (Asset Management)
│   ├── generate_atlas.py              # Genera índice ultraligero del proyecto
│   ├── generate_repo_index.py         # Genera mapas de código por rol
│   ├── generate_skill_registry.py     # Genera registros de skills por rol
│   └── generate_copilot_runtime.py    # Extrae slash commands de Copilot Chat
│
├── workflows/
│   └── copilot-context-migration.yml  # CI: regenera índices en push a main
│
└── memory/                            # ESTADO CROSS-SESSION (Mode 3)
    ├── local_dispatcher_state.tson    # Radar de dependencias (.gitignore)
    └── active_state.tson              # Estafeta temporal entre agentes
```

## Flujo Típico (Mode 1 — Subagent Pipeline)

```
Usuario: "@dispatcher implementa login con OAuth"
    │
    ├─► @tech-lead (subagent) → Define arquitectura, interfaces, ADR
    │       └─ retorna resumen al dispatcher
    │
    ├─► @backend-coder (subagent) → Implementa endpoints, servicios, modelos
    │       └─ retorna resumen al dispatcher
    │
    ├─► @appsec (subagent) → Audita seguridad, reporta hallazgos
    │       └─ retorna resumen al dispatcher
    │
    ├─► @qa (subagent) → Escribe y ejecuta tests
    │       └─ retorna resumen al dispatcher
    │
    └─► @devops (subagent) → Migraciones, Docker, CI/CD
            └─ retorna resumen al dispatcher
```

Cada subagente corre en su propio contexto aislado. No necesitan `/clear` entre ellos.

## Personalización

### Agregar un agente nuevo

Crea `.github/agents/mi-agente.agent.md` con frontmatter:
```yaml
---
description: "Mi agente custom — qué hace y cuándo invocarlo"
tools: [read, search, edit, execute]
---
```

### Agregar un skill nuevo

Crea `.github/skills/mi-skill/SKILL.md`:
```yaml
---
name: mi-skill
description: "Cuándo y para qué usar este skill"
roles: [backend-coder, qa]  # o [all] para todos
---
# Contenido del skill...
```

### Agregar una instrucción always-on

Crea `.github/instructions/mi-regla.instructions.md`:
```yaml
---
applyTo: "**/*.ts"  # Se activa cuando se tocan archivos .ts
---
# Reglas que aplican siempre para TypeScript...
```

## Gestión de Assets y Contexto (TSON)

El framework utiliza un formato optimizado llamado **TSON** (derivado de TOML) diseñado para ser extremadamente ligero y reducir el consumo de tokens en comparación con JSON o YAML.

Para evitar la saturación de contexto, el framework **no inyecta todo el proyecto**. En su lugar, utiliza un sistema de **Asset Management & Discovery**:
1. Los agentes leen un índice de muy alto nivel (`atlas.tson`).
2. Utilizan `discovery.py` bajo demanda para buscar y cargar exactamente los archivos o skills necesarios.

Los scripts de sincronización mantienen estos índices siempre actualizados:

```bash
# Ejecutar todos los generadores
bash .github/hooks/scripts/sync_agents.sh

# O directamente vía Python
python .github/hooks/scripts/generate_repo_index.py --role backend-coder
```

El workflow de CI (`copilot-context-migration.yml`) regenera los índices automáticamente en cada push a main.

## Diferencias: Instructions vs Skills

| | Instructions | Skills |
|--|-------------|--------|
| **Cuándo se cargan** | Automáticamente cuando se tocan archivos que matchean `applyTo` | Bajo demanda cuando el agente detecta relevancia por `description` |
| **Para qué** | Reglas de código, convenciones, runtime | Workflows, checklists, conocimiento de dominio |
| **Formato** | `.instructions.md` con `applyTo` glob | `SKILL.md` en carpeta con `description` |
| **Ejemplo** | "Siempre usa `uv run` en Python" | "Checklist de accesibilidad WCAG 2.1" |