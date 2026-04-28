# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [Unreleased]

## [1.3.0] - 2026-04-22

### Added
- **Asset Management & Discovery**: Nuevo script `discovery.py` para búsquedas deterministas bajo demanda que evita la saturación del contexto del LLM.

### Changed
- **Estandarización TSON**: Migración completa de archivos de estado y configuración (previamente JSON/YAML) al formato `.tson` (derivado de TOML) para optimizar el consumo de tokens.
- **Pure Python Runtime**: Eliminación total de dependencias y scripts de Node.js (`.mjs`). El framework opera 100% en Python, garantizando compatibilidad nativa en macOS y Linux para equipos frontend y backend.

## [1.1.0] - 2026-04-20

### Added
- **Limpieza de archivos deprecados:** `upgrade.sh` ahora elimina archivos legacy del framework (con backup `.deprecated`) listados en `deprecated_files` del manifest
- **Preservación de `project_profile`:** al actualizar el manifest, las configuraciones locales del usuario se mantienen
- Helper reutilizable `parse_json_array` en upgrade.sh para parsear múltiples arrays del manifest

### Changed
- Manifest v2: nuevo campo `deprecated_files` para listar archivos que ya no se usan
- Versión bumpeada a 1.1.0

### Fixed
- Crash de `((VAR++))` con `set -e` cuando contadores empezaban en 0 (cambiado a `VAR=$((VAR + 1))`)

### Deprecated
- Agentes sin sufijo `.agent.md`: `dispatcher.md`, `coder.md`, `appsec.md`, `devops.md`, `qa.md`, `tech-lead.md`, etc.

## [1.0.0] - 2026-04-20

### Added
- **9 agentes especializados:** dispatcher, tech-lead, backend-coder, frontend-coder, htmx-prototyper, ux-lead, appsec, qa, devops
- **3 modos de ejecución:** Subagent Pipeline, Compact Session, Parallel Worktrees
- **6 skills:** architecture-patterns, component-patterns, context-handoff, a11y-checklist, frontend-performance, react-native
- **4 instructions always-on:** design, python, react, typescript
- **Scripts de sincronización dual runtime:** Node.js (`.mjs`) y Python (`uv`)
- **Copilot hook** (`sync-on-stop.tson`): auto-regenera índices `.tson` al detener sesión
- **Workflow CI** (`copilot-context-migration.yml`): regenera índices en push a main
- **Prompt one-shot** (`copilot-init.prompt.md`): genera instrucciones/skills para repos nuevos
- Compatibilidad verificada con Linux y macOS

## [1.2.0] - 2026-04-21

### Added
- **The Atlas Discovery System**: Sustitución de carga masiva de índices por búsqueda bajo demanda (`atlas.tson` + `discovery.py/mjs`). Contexto inicial reducido de ~37% a <5%.
- **Blueprint & Bootstrap**: Nuevo comando `/init` y script `blueprint.py` para inicialización proactiva de proyectos (Frontend, Backend, etc.) en carpetas vacías.
- **Skill Library (Zero-Noise)**: Nueva carpeta `.github/skills/.library/` para alojar skills opcionales sin contaminar el contexto del agente por defecto.
- **Skill de Auditoría**: `system-audit` para validación obligatoria de calidad, seguridad y arquitectura.
- **Protocolo de Resiliencia**: Soporte para "Zero-Runtime" (operación manual vía IA) y stacks no predefinidos (como Rust).
- **Veracity & Evidence Rule**: Mandato de validación vía MCP para toda decisión de arquitectura y patrones de diseño.

### Changed
- **Purga de `/clear`**: Eliminación total de la dependencia de `/clear` a favor del aislamiento nativo por subagentes.
- **Unificación de Runtime**: Consolidación de toda la lógica de generación en Python, eliminando scripts redundantes en Node.js.
- **Clean Root**: El archivo `VERSION` se movió a `.github/framework-version.tson` para evitar ruido en la raíz del proyecto.
- **Sync Robusto**: `sync_agents.sh` ahora maneja validación de integridad de rutas y auto-corrección.

### Fixed
- Conflictos de rebase en archivos auto-generados `.tson`.
- Mapeo de skills en roles específicos para evitar carga de herramientas irrelevantes.

[Unreleased]: https://github.com/vic-mk/copilot-dev/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/vic-mk/copilot-dev/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/vic-mk/copilot-dev/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/vic-mk/copilot-dev/releases/tag/v1.0.0
