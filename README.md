# Copier FastAPI Service Template

Generate a ready-to-customize FastAPI service with [Copier](https://copier.readthedocs.io/), modern Python tooling, a `src/` package layout, structured JSON logs, tests, and optional Docker support.

This repository is a **project generator**, not a FastAPI application to run directly. Answer a short set of questions and Copier creates a standalone service tailored to your choices.

## Why this template?

- **A useful starting point, not a black box:** a small health endpoint, application factory, lifespan, settings, and service dependency container give you a clear place to add application code.
- **Modern Python workflow:** Python 3.13+, [uv](https://docs.astral.sh/uv/), [Ruff](https://docs.astral.sh/ruff/), [ty](https://github.com/astral-sh/ty), pytest, and [just](https://just.systems/).
- **Production-minded defaults:** debug mode is off by default, JSON logging includes request IDs, and the optional Docker image runs as a non-root user.
- **Choose your architecture:** include or omit the database, domain, repositories, generative-AI, and Docker scaffolding.
- **Ready to extend:** generated tests, configuration examples, development commands, security checks, and contributor guidance are included.

## Contents

- [Requirements](#requirements)
- [Create a project](#create-a-project)
- [First steps in the generated service](#first-steps-in-the-generated-service)
- [Template options](#template-options)
- [Run with Docker](#run-with-docker)
- [Development commands](#development-commands)
- [Generated project layout](#generated-project-layout)
- [Updating a project](#updating-a-project)
- [Design notes](#design-notes)
- [Contributing](#contributing)
- [License](#license)

## Requirements

To generate a project:

- Python 3.13 or newer
- Git
- Copier 9 or newer

For the generated service, install [uv](https://docs.astral.sh/uv/) and [just](https://just.systems/). Docker Engine with the Compose plugin is needed only if you choose Docker support.

Run the template with Copier and its Jinja extensions using `uvx`:

```bash
uvx --with copier-template-extensions copier --version
```

## Create a project

Run Copier from the template's Git repository:

```bash
uvx --with copier-template-extensions copier copy --trust gh:anocerino-ai/copier-fastapi-service-template.git my-service
```

Copier asks for a project name, description, author details, license, and optional components. The generated directory is independent of the template repository.

The `--trust` flag is required because this template defines post-generation tasks. Before authorizing them, inspect the template source: its tasks initialize Git, set the generated repository's local author name and email, and remove `LICENSE` when you choose no license. Only use `--trust` for a template whose source you trust.

Use a readable project name such as `FastAPI Service`. The template derives the conventional distribution slug (`fastapi-service`) and Python package name (`fastapi_service`) automatically; neither value needs to be entered separately.

To generate from a local checkout instead:

```bash
git clone https://github.com/anocerino-ai/copier-fastapi-service-template.git
cd copier-fastapi-service-template
uvx --with copier-template-extensions copier copy --trust . ../my-service
```

To use defaults non-interactively:

```bash
uvx --with copier-template-extensions copier copy --trust --defaults gh:anocerino-ai/copier-fastapi-service-template.git my-service
```

Review the answers before using `--defaults` in automation. The generated project is initialized as a Git repository with the selected author name and email as its local Git identity.

## First steps in the generated service

```bash
cd my-service
cp .env.example .env
just install
just test
just run-dev
```

The API is then available at:

- OpenAPI UI: <http://localhost:8000/docs>
- Health check: <http://localhost:8000/api/v1/health>

`just install` runs `uv sync --all-groups`, resolving dependencies and creating `uv.lock` as well as the local virtual environment. Review and commit that lockfile to make subsequent installs reproducible.

## Template options

| Option | Default | What it controls |
| --- | --- | --- |
| Project name and description | `FastAPI Service` / `A Python service` | Package, distribution metadata, API title, and generated documentation. |
| Author name and email | Template defaults | Package metadata and the generated repository's local Git identity. |
| License | MIT | Select MIT, Apache-2.0, BSD-3-Clause, Custom, or no license. |
| Docker | Included | Generates a Dockerfile, Compose file, and `.dockerignore`. |
| Docker network | Included with Docker | Creates a project-specific bridge network or connects to an existing external network. |
| Database package | Included | Adds a placeholder `db/` package; database drivers and migrations are not configured automatically. |
| Domain package | Included | Adds a placeholder `domain/` package for domain logic. |
| Repositories package | Included | Adds a placeholder `repositories/` package for persistence adapters. |
| Generative AI packages | Omitted | Adds a modular `gen_ai/` package structure when enabled. |
| MCP subpackage | Enabled with Generative AI | Adds the optional `gen_ai/mcp/` package. |

Optional architecture directories are starting points, not prebuilt integrations. Select only the components that fit your service, then add the corresponding dependencies and implementation.

## Run with Docker

The generated Docker build uses `uv sync --frozen` and expects `uv.lock` in the project root. Create it before building:

```bash
cd my-service
cp .env.example .env
just install
docker compose --env-file .env -f docker/compose.yaml up --build
```

The Compose file loads environment values from `.env`, publishes the configured application port, and optionally connects the service to the selected network. To stop the service:

```bash
docker compose --env-file .env -f docker/compose.yaml down
```

The generated image uses a non-root runtime user and includes a health check. Review the Dockerfile, environment variables, CORS policy, and deployment settings against your own operational and security requirements before deploying.

## Development commands

Run `just` to list all recipes. Common commands include:

| Command | Purpose |
| --- | --- |
| `just install` | Resolve and install all dependency groups. |
| `just run-dev` | Start Uvicorn with hot reload. |
| `just lint` / `just format` | Check or format code with Ruff. |
| `just typecheck` | Run the `ty` type checker. |
| `just test` / `just test-cov` | Run tests, optionally with coverage output. |
| `just lock-check` | Check that the lockfile is current. |
| `just audit` | Audit installed dependencies. |
| `just sast` | Run Semgrep static analysis. |
| `just license-check` | Generate a third-party license report. |
| `just security` | Run the security and dependency checks. |
| `just ci` | Run the local quality, test, and security gate. |
| `just commit` | Start the guided Conventional Commit prompt. |

## Generated project layout

The exact tree depends on the selected options. The base service looks like this:

```text
my-service/
├── .env.example
├── .pytools/                 # Ruff, ty, pytest, and coverage settings
├── pyproject.toml
├── justfile
├── src/
│   └── my_service/
│       ├── api/v1/           # Versioned HTTP routes
│       ├── core/             # Settings, errors, logging, request IDs
│       ├── schemas/          # Request and response models
│       ├── services/         # Application services
│       ├── container.py      # Application-scoped service dependencies
│       ├── lifespan.py       # Startup and shutdown hooks
│       └── main.py           # FastAPI application factory
├── tests/
└── docker/                   # Optional Dockerfile and Compose setup
```

## Updating a project

The generated repository keeps Copier's answers in `.copier-answers.yml`. After making a backup and committing your changes, update from the same template source:

```bash
uvx --with copier-template-extensions copier update --trust
```

Review the diff carefully and resolve conflicts as you would for any upstream change. Template updates do not replace application-specific review or testing.

## Design notes

- **Configuration:** settings are loaded from environment variables and the optional `.env` file. `.env.example` is a safe starting point; keep secrets out of version control.
- **Request IDs:** a request-provided `X-Request-ID` is propagated, or a new ID is generated and returned in the response.
- **Logging:** logs are emitted as JSON to standard output, which works well with container log collectors.
- **Architecture:** the template establishes a modest separation between routes, schemas, services, and core utilities. It does not force a specific database, ORM, or domain model.
- **Security posture:** the defaults are intended as a baseline, not a security certification. Configure trusted CORS origins, secrets, dependency updates, logging, and deployment controls for your environment.
- **License choice:** `Custom` currently generates a proprietary/all-rights-reserved placeholder, not legal advice or a complete custom license. Replace it with terms reviewed for your use before distributing the generated project.

## Contributing

Issues and pull requests are welcome. Please describe the problem, the expected behavior, and any affected template options. When changing generated behavior, test a newly rendered project as well as the source template.

For a quick local smoke test, generate into a new temporary directory with Copier and inspect the rendered files before opening a pull request.

## License

The template repository is licensed under the terms in [LICENSE](LICENSE). The license selected during generation is separate and applies to the generated project.
