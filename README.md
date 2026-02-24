# gemini-agents-setup
A test setup for working with gemini agents and sub agents

## Overview

This repository provides a complete Docker-based infrastructure for running Gemini AI agents in a multi-agent architecture. It includes:
- A main Gemini agent coordinator
- Multiple sub-agents for distributed processing
- Redis for inter-agent communication and caching
- Isolated network environment for secure agent communication

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)
- A valid Google Gemini API key

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/iandeherdt/gemini-agents-setup.git
   cd gemini-agents-setup
   ```

2. **Run the health check (optional)**
   ```bash
   ./health-check.sh
   ```
   This will verify that all required files and Docker are properly configured.

3. **Set up environment variables**
   ```bash
   make setup
   # or manually:
   cp .env.example .env
   ```
   
   Edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Build and start the services**
   ```bash
   make up
   # or using docker compose directly:
   docker compose up --build -d
   ```

5. **Access the agents**
   - Main Agent: http://localhost:8000
   - Sub-Agent 1: http://localhost:8001
   - Sub-Agent 2: http://localhost:8002
   - Redis: localhost:6379

6. **View logs**
   ```bash
   make logs
   # or for a specific service:
   make logs-main
   ```

## Architecture

The setup includes the following services:

### Main Agent
The primary coordinator that manages and distributes tasks to sub-agents.

### Sub-Agents
- **Sub-Agent 1**: Processing agent for handling data processing tasks
- **Sub-Agent 2**: Analysis agent for performing analytical operations

### Redis
Used for:
- Inter-agent communication
- Task queue management
- Caching frequently accessed data

## Docker Commands

### Using Makefile (Recommended)

The repository includes a Makefile for convenient management:

```bash
make help        # Show all available commands
make setup       # Create .env file from .env.example
make build       # Build all Docker images
make up          # Start all services in detached mode
make down        # Stop all services
make logs        # Show logs from all services
make logs-main   # Show logs from main agent
make logs-sub1   # Show logs from sub-agent-1
make logs-sub2   # Show logs from sub-agent-2
make restart     # Restart all services
make clean       # Stop services and remove volumes
make ps          # Show running containers
make validate    # Validate docker-compose configuration
make shell-main  # Open shell in main agent container
```

### Using Docker Compose Directly

#### Start all services
```bash
docker compose up -d
```

#### Stop all services
```bash
docker compose down
```

#### View logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f main-agent
docker compose logs -f sub-agent-1
docker compose logs -f sub-agent-2
```

#### Rebuild services
```bash
docker compose up --build
```

#### Scale sub-agents
```bash
docker compose up --scale sub-agent-1=3
```

## Configuration

### Environment Variables

All configuration is done via environment variables in the `.env` file:

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `AGENT_TIMEOUT`: Timeout for agent operations in seconds
- `MAX_RETRIES`: Maximum number of retries for failed operations
- `REDIS_HOST`: Redis hostname (default: redis)
- `REDIS_PORT`: Redis port (default: 6379)

### Volume Mounts

The following directories are mounted as volumes:
- `./data`: Persistent data storage
- `./logs`: Agent logs
- `./agents`: Agent source code (for development)

## Development

### Project Structure
```
gemini-agents-setup/
├── agents/              # Agent source code
│   ├── __init__.py
│   └── main.py
├── data/                # Persistent data
├── logs/                # Log files
├── docker-compose.yml   # Docker Compose configuration
├── Dockerfile           # Docker image definition
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
├── .dockerignore        # Docker ignore patterns
├── .gitignore           # Git ignore patterns
├── Makefile             # Convenient make commands
└── health-check.sh      # Health check script
```

### Adding New Agents

To add a new sub-agent, add a new service in `docker-compose.yml`:

```yaml
sub-agent-3:
  build:
    context: .
    dockerfile: Dockerfile
  container_name: gemini-sub-agent-3
  environment:
    - AGENT_TYPE=sub-agent-3
    - GEMINI_API_KEY=${GEMINI_API_KEY}
    - MAIN_AGENT_URL=http://main-agent:8000
  ports:
    - "8003:8000"
  networks:
    - gemini-network
  depends_on:
    - main-agent
```

## Troubleshooting

### Health Check
Run the health check script to diagnose issues:
```bash
./health-check.sh
```

### Containers won't start
- Check Docker logs: `make logs` or `docker compose logs`
- Verify environment variables are set correctly in `.env`
- Ensure ports 8000-8002 and 6379 are not in use
- Run `make validate` to check configuration

### API key errors
- Verify your Gemini API key is valid
- Ensure the `.env` file is in the project root
- Check that the `GEMINI_API_KEY` variable is set correctly
- Make sure you've edited `.env` and replaced the placeholder value

### Network issues
- Ensure the `gemini-network` is created: `docker network ls`
- Restart Docker: `sudo systemctl restart docker`

### Permission issues
- Ensure health-check.sh is executable: `chmod +x health-check.sh`
- Check directory permissions for `data/` and `logs/`

## License

See LICENSE file for details.
