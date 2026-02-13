# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2026-02-14

### Added
- **Real-time Interaction**:
  - Implemented Server-Sent Events (SSE) for real-time agent progress streaming from backend to frontend.
  - Added visual indicators: "Thinking..." text and pulsing avatar animation for active agents.
  - Added ability to stop/cancel running agent tasks via a "Stop" button in the UI.
- **Frontend Architecture**:
  - **TypeScript Migration**: Fully converted the frontend codebase to TypeScript for better type safety and maintainability.
  - **Modularization**: Refactored the monolithic `ChatArea` component into smaller, focused components:
    - `ChatArea` (Container)
    - `MessageList` (Display logic)
    - `MessageItem` (Individual message rendering)
    - `ChatInput` (User input handling)
  - **Custom Hooks**: logic extracted into `useOrchestrator` hook.
- **Testing & Quality**:
  - **Backend**: Added `pytest` setup w/ `pytest-mock`, plus `flake8`, `black`, and `isort`.
  - **Frontend**: Added `vitest` and `@testing-library/react` for component testing.
  - Created initial unit tests for both backend agents and frontend components.
- **CI/CD & DevEx**:
  - Added GitHub Actions workflows: `.github/workflows/ci.yml` (Backend) and `.github/workflows/frontend-ci.yml` (Frontend).
  - Added `Makefile` in both directories to standardize commands (`make test`, `make lint`, `make install`).

### Changed
- **Documentation**:
  - Major reorganization of project documentation into `docs/` directory (Setup, Guides, API, Architecture).
  - Completely rewrote `README.md` to serve as a better entry point.
- **Backend API**:
  - Updated `ChatView` to support `StreamingHttpResponse`.
  - Enhanced `Orchestrator` class to yield detailed event objects (`step_start`, `plan_created`, `error`, etc.) instead of just final results.

### Fixed
- Fixed backend linting issues and standardized code style.
- Resolved various minor bugs in the chat interface state management.

## [1.2.0] - 2026-01-22

### Added
- **Web UI**: Introduced a modern Streamlit-based web interface (Release v1.2).
- **Parallel Execution**: Enabled parallel task execution capabilities in orchestrator and coordinator.
- **File Access**: Allowed agents to read local files for analysis context.
- **Session Persistence**: Added ability to save and restore agent sessions.
- **Web Search**: Integrated DuckDuckGo search capabilities for the Researcher agent.
- **File Output**: Added capability for agents to write results to files.

### Changed
- **Documentation**: Updated README with Web UI details and added preview images.
- **Styles**: Applied "Gemini 3" style design to the web interface.

## [1.1.0] - 2026-01-21

### Added
- Initial project release.
- Core agent architecture (Researcher, Analyzer, Writer, Coordinator).
- Basic orchestration logic.
- CLI interface for interaction.

### Fixed
- Fixed image paths for GitHub compatibility.
