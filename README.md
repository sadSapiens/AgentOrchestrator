# Agent Orchestrator

An intelligent multi-agent orchestration system powered by Gemini 1.5 Flash. This system coordinates specialized AI agents (Researcher, Analyzer, Writer, Coordinator) to solve complex tasks autonomously.

## 📚 Documentation

Complete documentation is available in the `docs/` directory:

- **Setup**:
  - [Quick Start](docs/setup/quickstart.md): Get up and running in minutes.
  - [Project Structure](docs/project_structure.md): Detailed overview of files and directories.

- **Guides**:
  - [CLI Guide](docs/guides/cli.md): How to use the command-line interface.
  - [Tutorial](docs/guides/tutorial.md): Step-by-step walkthrough of features.

- **Technical Reference**:
  - [Architecture](docs/architecture.md): System design and components.
  - [Diagrams](docs/diagrams.md): Visual representations of workflows.

## 🚀 Quick Start (Docker)

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/agent-orchestrator.git
    cd agent-orchestrator
    ```

2.  **Configure Environment**:
    copy `.env.example` to `.env` and add your `GEMINI_API_KEY`.

3.  **Run with Docker Compose**:
    ```bash
    docker-compose up --build
    ```

4.  **Access the App**:
    - Frontend: http://localhost:3000
    - Backend API: http://localhost:8000

## 🧪 Development

### Backend
```bash
cd backend
make install
make test
make lint
```

### Frontend
```bash
cd frontend
make install
make test
make lint
```

## License

MIT
