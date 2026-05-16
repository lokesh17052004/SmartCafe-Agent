# SmartCafe-Agent

An advanced **Agentic AI-Powered Coffee Commerce Assistant** built using **FastAPI**, **LangChain**, **AWS Bedrock**, **PostgreSQL**, and a complete **MCP Client-Server Architecture** that intelligently handles coffee ordering workflows, inventory management, menu assistance, recommendation systems, and conversational customer interactions.

The platform uses a **single intelligent AI agent** integrated with MCP tools and resources to dynamically interact with external commerce capabilities through a centralized conversational workflow.

---

# Project Name

# AI-Powered Autonomous Commerce Assistant

---

# Table of Contents

- Introduction
- Features
- System Architecture
- Technologies Used
- Workflow Architecture
- MCP Client-Server Workflow
- AI Agent Workflow
- MCP Resources
- MCP Tools
- Request Flow
- Inventory Workflow
- Order Workflow
- Recommendation Workflow
- Memory Persistence
- AWS Bedrock Integration
- Folder Structure
- Installation Guide
- UV Package Manager Setup
- Environment Variables
- PostgreSQL Setup
- Running MCP Server
- Running MCP Client
- API Documentation
- Request & Response Examples
- LangGraph Memory Workflow
- Future Enhancements
- License

---

# Introduction

Bean & Brew AI is an intelligent conversational commerce platform capable of:

- understanding customer requests
- handling coffee ordering workflows
- checking inventory dynamically
- managing order status tracking
- providing contextual coffee recommendations
- answering menu-related questions
- retrieving shop information
- orchestrating conversational AI workflows using MCP architecture

The platform demonstrates modern Agentic AI concepts using:

- LangChain
- FastAPI
- AWS Bedrock
- PostgreSQL
- MCP Client-Server Architecture
- Stateful AI Memory

Unlike traditional multi-agent systems, this project uses a **single intelligent AI agent** enhanced through MCP tools and resources for dynamic workflow execution.

---

# Core Features

## AI Features

- Agentic AI Architecture
- Conversational Commerce Workflow
- Intelligent Coffee Recommendations
- Context-Aware Customer Interaction
- Inventory-Aware Ordering System
- Dynamic MCP Tool Execution
- Stateful AI Conversations
- AI-Based Order Management
- Coffee Preference Analysis
- Shop Information Assistance
- Conversational Workflow Automation

---

## Backend Features

- FastAPI REST APIs
- Async Backend Architecture
- PostgreSQL Integration
- MCP Client-Server Communication
- Modular Service Architecture
- Structured Exception Handling
- AWS Bedrock Integration
- Stateful Workflow Persistence

---

# System Architecture

```text
                           ┌────────────────────┐
                           │      Customer      │
                           └─────────┬──────────┘
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │      FastAPI API       │
                        └──────────┬─────────────┘
                                   │
                                   ▼
                    ┌────────────────────────────┐
                    │     Single AI Agent        │
                    │  (Conversational Agent)    │
                    └──────────┬─────────────────┘
                               │
                               ▼
                 ┌───────────────────────────────┐
                 │       MCP Client Layer        │
                 └──────────┬────────────────────┘
                            ▼
                 ┌───────────────────────────────┐
                 │        MCP Server             │
                 └───────┬───────────┬───────────┘
                         │           │
                         ▼           ▼
            ┌─────────────────┐ ┌─────────────────┐
            │ MCP Resources   │ │ MCP Tools       │
            └─────────────────┘ └─────────────────┘
                         │
                         ▼
               ┌─────────────────────┐
               │ PostgreSQL Database │
               └─────────────────────┘
```

---

# Workflow Architecture

The platform follows a centralized AI conversational workflow.

Unlike multi-agent architectures, the system uses:

- one intelligent conversational AI agent
- MCP tools for external actions
- MCP resources for contextual retrieval
- PostgreSQL for memory persistence

The AI dynamically decides:
- when to access menu resources
- when to invoke ordering tools
- when to check inventory
- when to retrieve shop details

---

# Important Workflow Logic

## Single AI Agent Workflow

Every customer request first enters the main AI conversational agent.

The AI agent:
- analyzes customer intent
- determines required MCP resources
- invokes MCP tools dynamically
- generates contextual responses
- maintains conversational memory

---

# MCP Client-Server Workflow

The project implements a complete MCP architecture.

---

# MCP Workflow

```text
Customer Request
        ↓
FastAPI API
        ↓
AI Conversational Agent
        ↓
MCP Client
        ↓
MCP Server
        ↓
Resource / Tool Execution
        ↓
AI Response Generation
        ↓
Final Response
```

---

# AI Agent Workflow

The project contains a single intelligent AI agent enhanced using MCP integrations.

---

# AI Agent Responsibilities

The AI Agent:
- handles customer conversations
- detects user requirements
- retrieves contextual resources
- invokes MCP tools dynamically
- manages ordering workflows
- provides recommendations
- maintains memory continuity

---

# Intent Detection Workflow

The AI agent dynamically detects:

- menu queries
- coffee recommendations
- caffeine preference requests
- inventory checks
- order placement
- order tracking
- shop information requests
- out-of-context conversations

---

# MCP Resources

The MCP Server exposes contextual resources.

---

# 1. Menu Resource

## Resource URI

```text
menu://items
```

## Purpose

Provides:
- menu items
- descriptions
- prices
- tax information
- stock availability

---

# 2. Shop Information Resource

## Resource URI

```text
resource://shop-info
```

## Purpose

Provides:
- shop details
- address
- contact information
- social media links
- working hours
- facilities
- payment modes

---

# MCP Tools

The MCP Server exposes multiple commerce tools.

---

# 1. Inventory Checking Tool

## Purpose

Checks stock availability for coffee items.

## Example

### Input

```text
Do you have cold brew available?
```

### Tool Execution

```python
check_inventory(item_name="Cold Brew")
```

---

# 2. Order Status Tool

## Purpose

Tracks customer orders using order codes.

## Example

### Input

```text
Check my order status ORD-A1B2C3D4
```

### Tool Execution

```python
check_order_status(order_code="ORD-A1B2C3D4")
```

---

# 3. Add Order Tool

## Purpose

Places customer orders dynamically.

## Example

### Input

```text
I want 2 cappuccinos and 1 espresso
```

### Tool Execution

```python
add_order(customer_id="123", items=[...])
```

---

# Request Flow

# Coffee Recommendation Workflow

```text
Customer Request
        ↓
FastAPI API
        ↓
AI Conversational Agent
        ↓
Intent Detection
        ↓
MCP Resource Retrieval
        ↓
Recommendation Generation
        ↓
Final Response
```

---

# Inventory Workflow

```text
Customer Request
        ↓
AI Agent
        ↓
MCP Tool Invocation
        ↓
Inventory Database Check
        ↓
Stock Response
```

---

# Order Placement Workflow

```text
Customer Request
        ↓
AI Agent
        ↓
MCP Add Order Tool
        ↓
Database Order Creation
        ↓
Order Confirmation
```

---

# Out-of-Context Handling

If the customer asks unrelated questions:

Example:

```text
"Who won yesterday's football match?"
```

The AI agent:
- identifies unrelated context
- avoids MCP workflow execution
- directly responds conversationally

This prevents unnecessary tool invocation.

---

# AWS Bedrock Integration

The project integrates AWS Bedrock using:

- boto3
- ChatBedrock
- Bedrock Runtime APIs

---

# AWS Features Used

- Foundation Models
- Conversational AI Processing
- Dynamic Response Generation
- AI Workflow Execution
- LLM Inference

---

# Technologies Used

## Programming Language

- Python

---

## Backend Framework

- FastAPI

---

## AI Frameworks

- LangChain

---

## Cloud & AI Services

- AWS Bedrock
- boto3

---

## Database

- PostgreSQL

---

## AI Concepts

- Agentic AI
- Conversational Commerce
- MCP Client-Server Architecture
- Stateful AI Systems
- Contextual Retrieval
- AI Workflow Automation
- Memory Persistence

---

# Folder Structure

```text
BeanAndBrew-AI/
│
├── MCP_Client/
│   │
│   ├── main.py
│   ├── settings.py
│   ├── pyproject.toml
│   ├── uv.lock
│   │
│   └── src/
│       │
│       ├── agent/
│       │   ├── agent.py
│       │   ├── prompts.py
│       │   └── __init__.py
│       │
│       ├── models/
│       │   ├── model.py
│       │   └── __init__.py
│       │
│       ├── repository/
│       │   ├── database.py
│       │   ├── error_repository.py
│       │   └── schema.py
│       │
│       ├── router/
│       │   └── router.py
│       │
│       ├── service/
│       │   ├── coffee_service.py
│       │   └── __init__.py
│       │
│       └── utils/
│           └── exceptions/
│               ├── custom_app_exception.py
│               └── error_codes.py
│
├── MCP_Server/
│   │
│   ├── main.py
│   ├── settings.py
│   ├── pyproject.toml
│   ├── uv.lock
│   │
│   └── src/
│       │
│       ├── migrations/
│       │   └── migration.py
│       │
│       ├── prompts/
│       │   ├── prompts.py
│       │   └── __init__.py
│       │
│       ├── repository/
│       │   ├── coffee_repository.py
│       │   ├── database.py
│       │   ├── error_repository.py
│       │   └── schema.py
│       │
│       ├── resources/
│       │   ├── resources.py
│       │   └── __init__.py
│       │
│       ├── router/
│       │   └── mcp_router.py
│       │
│       ├── tools/
│       │   ├── mcp_tools.py
│       │   └── __init__.py
│       │
│       └── utils/
│           └── exceptions/
│               ├── custom_app_exception.py
│               └── error_codes.py
│
├── README.md
└── Dockerfile
```

---

# Installation Guide

# Method 1 — Using UV (Recommended)

UV is a modern ultra-fast Python package manager.

---

# Step 1 — Install UV

## Windows

```bash
pip install uv
```

---

## Linux / Mac

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

# Step 2 — Clone Repository

```bash
git clone https://github.com/your-username/beanandbrew-ai.git
```

---

# Step 3 — Navigate to Project

```bash
cd SmartCafe-Agent
cd AI-Powered_Autonomous_Commerce_Assistant
```

---

# Step 4 — Create Virtual Environment

```bash
uv venv
```

---

# Step 5 — Activate Environment

## Windows

```bash
.venv\Scripts\activate
```

---

## Linux / Mac

```bash
source .venv/bin/activate
```

---

# Step 6 — Install Dependencies

## MCP Client

```bash
cd MCP_Client
uv sync
```

---

## MCP Server

```bash
cd ../MCP_Server
uv sync
```

---

# Environment Variables

## MCP Client `.env`

```env
AWS_REGION=us-east-1
MODEL_ID=anthropic.claude-3-5-sonnet
PROVIDER=anthropic

DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=password
DB_NAME=beanandbrew

MCP_SERVER_URL=http://localhost:8001/mcp
```

---

## MCP Server `.env`

```env
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=password
DB_NAME=beanandbrew
```

---

# Database Setup

## Create PostgreSQL Database

```sql
CREATE DATABASE beanandbrew;
```

---

# Running MCP Server

```bash
cd MCP_Server
un run  main.py
```

---

# Running MCP Client

```bash
cd MCP_Client
uv runmain.py
```

---

# API Documentation

## Swagger UI

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoint

# Chat Endpoint

## Endpoint

```http
POST /chat
```

---

# Request Body

```json
{
  "message": "Suggest me a strong cold coffee",
  "thread_id": "12345"
}
```

---

# Example Response

```json
{
  "recommendation": "Cold Brew Espresso",
  "reason": "High caffeine with bold flavor profile."
}
```

---

# Memory Persistence

The project uses:

- AsyncPostgresSaver
- PostgreSQL checkpointing
- thread-based persistence

This enables:
- contextual conversation continuity
- stateful AI memory
- workflow persistence

---

# Key Concepts Implemented

- Agentic AI
- MCP Client-Server Architecture
- Conversational Commerce AI
- AI Tool Invocation
- Contextual Retrieval
- Stateful AI Systems
- AI Workflow Automation
- FastAPI Backend Development
- PostgreSQL Memory Persistence

---

# Author

## Lokesh Sankar

Backend Developer | Agentic AI Developer | FastAPI Developer
