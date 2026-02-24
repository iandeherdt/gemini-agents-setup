.PHONY: help build up down logs clean restart shell

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

build: ## Build all Docker images
	docker compose build

up: ## Start all services
	docker compose up -d

down: ## Stop all services
	docker compose down

logs: ## Show logs from all services
	docker compose logs -f

logs-main: ## Show logs from main agent
	docker compose logs -f main-agent

logs-sub1: ## Show logs from sub-agent-1
	docker compose logs -f sub-agent-1

logs-sub2: ## Show logs from sub-agent-2
	docker compose logs -f sub-agent-2

clean: ## Stop services and remove volumes
	docker compose down -v

restart: down up ## Restart all services

shell-main: ## Open shell in main agent container
	docker compose exec main-agent /bin/bash

shell-sub1: ## Open shell in sub-agent-1 container
	docker compose exec sub-agent-1 /bin/bash

ps: ## Show running containers
	docker compose ps

validate: ## Validate docker-compose configuration
	docker compose config

setup: ## Setup environment file from example
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env file. Please edit it and add your GEMINI_API_KEY"; \
	else \
		echo ".env file already exists"; \
	fi
