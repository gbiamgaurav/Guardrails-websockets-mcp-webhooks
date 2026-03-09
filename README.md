# Guardrails, WebSockets & MCP Webhooks - Learning Material

A collection of three practical projects demonstrating modern Python web technologies, AI integration, and real-time communication patterns.

---

## 📚 Project Overview

This workspace contains three independent learning projects:

| Project | Technology | Purpose |
|---------|-----------|---------|
| **Guardrails** | LangChain + Groq AI | Building AI applications with safety guardrails |
| **MCP_demo** | Model Context Protocol + FastMCP | Creating intelligent MCP servers and clients |
| **WebsocketsDemo** | FastAPI + WebSockets | Real-time bidirectional communication |
| **WebhooksDemo** | FastAPI + HTTP Callbacks | Event-driven webhooks and integrations |

---

## 🗂️ Folder Structure

```
Guardrails-websockets-mcp-webhooks/
├── Guardrails/              # AI with guardrails
│   ├── guardrails.ipynb    # Interactive Jupyter notebook
│   ├── main.py             # Main entry point
│   ├── requirements.txt     # Dependencies
│   ├── pyproject.toml       # Project config
│   └── README.md            # Project-specific docs
│
├── MCP_demo/                # Model Context Protocol demo
│   ├── client.py           # MCP client implementation
│   ├── main.py             # Entry point
│   ├── mathserver.py        # Math tools server
│   ├── weather.py          # Weather tools server
│   ├── requirements.txt     # Dependencies
│   ├── pyproject.toml       # Project config
│   └── README.md            # Project-specific docs
│
├── WebsocketsDemo/          # WebSocket chat application
│   ├── main.py             # FastAPI server
│   ├── requirements.txt     # Dependencies
│   ├── templates/
│   │   ├── index.html      # Chat UI
│   │   └── admin.html      # Admin dashboard
│   └── README.md            # Project-specific docs
├── WebhooksDemo/            # Webhook event system
│   ├── main.py             # Webhook server
│   ├── client.py           # Webhook client example
│   ├── requirements.txt     # Dependencies
│   └── README.md            # Project-specific docs
│
│
└── README.md                # This file
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8+
- pip or uv package manager
- Virtual environment (venv, conda, or uv venv)

### Setup

---

1. **Navigate to the workspace:**
   ```bash
   cd Guardrails-websockets-mcp-webhooks
   ```

2. **Choose a project and follow its specific setup:**

---

## 📖 Project Details

### 1️⃣ **Guardrails** - AI Applications with Safety

**What you'll learn:**
- Building AI applications using LangChain
- Implementing guardrails for safe AI outputs
- Integrating with Groq AI API
- Using Jupyter notebooks for exploratory development

**Key Technologies:**
- `langchain` - LLM orchestration
- `langchain-groq` - Groq API integration
- `langchain_openai` - OpenAI integration (optional)
- `jupyter` - Interactive notebooks

**How to use:**
```bash
cd Guardrails

# Option 1: Run the notebook
jupyter notebook guardrails.ipynb

# Option 2: Run as Python script
python main.py
```

**What it does:**
Creates AI applications with built-in safeguards to ensure outputs meet safety and business requirements.

---

### 2️⃣ **MCP_demo** - Model Context Protocol

**What you'll learn:**
- Model Context Protocol (MCP) architecture
- Building MCP servers with tools
- Creating MCP clients to consume tools
- Integrating with LangChain agents
- Creating specialized tool servers (math, weather, etc.)

**Key Technologies:**
- `mcp` - Core MCP library
- `fastmcp` - FastAPI-based MCP server
- `langchain-mcp-adapters` - LangChain integration
- `langgraph` - Agentic workflows
- `langchain_openai` - LLM integration

**How to use:**
```bash
cd MCP_demo

# Run the client (connects to MCP servers)
python client.py

# Or run main
python main.py

# The project includes:
# - mathserver.py: Math operations server
# - weather.py: Weather information server
```

**What it does:**
Demonstrates how to create protocol-driven tool systems where clients can discover and use tools provided by MCP servers. Useful for building extensible AI applications.

---

### 3️⃣ **WebsocketsDemo** - Real-Time Chat Application

**What you'll learn:**
- Building real-time web applications with WebSockets
- FastAPI framework and async programming
- Client-side WebSocket communication with JavaScript
- Real-time event broadcasting
- User activity tracking and logging

**Key Technologies:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `websockets` - WebSocket protocol
- HTML5 + JavaScript WebSocket API

**How to use:**
```bash
cd WebsocketsDemo

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload

# Open in browser
# http://localhost:8000
```

**F

### � WebSockets vs Webhooks at a Glance

| Feature | WebSockets | Webhooks |
|---------|-----------|----------|
| Connection | Persistent TCP | HTTP POST requests |
| Direction | Bidirectional | One-way (server → client) |
| Real-time | ✅ Instant (<100ms) | ✅ Fast (~500ms) |
| Firewall | ❌ Needs special ports | ✅ Standard HTTP |
| Use Case | Chat, dashboards, games | Events, notifications, integrations |
| Scalability | Many connections needed | More scalable |
| Client Availability | Must be online | Can handle offline |

**When to Use Each:**
- **WebSockets**: Real-time interactive chat, live dashboards, multiplayer games
- **Webhooks**: GitHub→Deploy, Payment→Notify, Form→Workflow, Monitoring→Alert

For a detailed comparison, see [WebhooksDemo/README.md](WebhooksDemo/README.md).

---

## �4️⃣ **WebhooksDemo** - Event-Driven HTTP Callbacks

**What you'll learn:**
- Webhook registration and management
- Event-driven architecture patterns
- HTTP callback systems
- Decoupled service communication
- Comparing webhooks vs WebSockets
- Real-world webhook implementations

**Key Technologies:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `httpx` - Async HTTP client
- HTTP POST callbacks

**How to use:**
```bash
cd WebhooksDemo

# Terminal 1: Run webhook server
python main.py

# Terminal 2: Run webhook client
python client.py

# Terminal 3: Test the system
curl -X POST http://localhost:8000/test-event
```WebhooksDemo** - Learn event-driven architecture
3. Move to **Guardrails** - Learn AI integration basics
4. Advance to **MCP_demo** - Understand tool-driven architecture

**Intermediate/Advanced:**
- Combine concepts: Build a real-time chat with AI (Guardrails + WebsocketsDemo)
- Extend MCP tools: Add custom servers to MCP_demo
- Integrate webhooks: Send WebSocket events via webhooksooks
- Perfect for integrations, notifications, and decoupled systems

**Key Differences from WebSockets:**
- **Webhooks:** One-way (server → client), HTTP-based, firewall-friendly
- **WebSockets:** Bidirectional, persistent connection, real-time
- See [WebhooksDemo/README.md](WebhooksDemo/README.md) for detailed comparison

---eatures:**
- 🔄 Real-time bidirectional communication
- 👥 Online users list
- ✍️ Typing indicators
- 💬 Private messaging
- 📱 Mobile-friendly responsive UI
- 📊 Activity logging and user statistics

---
Webhooks + WebSockets**
   - WebSocket chat broadcasts events
   - Webhooks notify external services
   - Example: Chat message → trigger webhook → external logging

4. **Activity Analytics**
   - WebSocket activity → WebhooksDemo webhooks → analytics service
   - Use Guardrails to generate insights
   - Expose data via MCP tools

5. **Event-Driven System**
   - WebhooksDemo receives integrations (GitHub, payment systems)
   - WebSockets broadcast events in real-time
   - Guardrails processes events safelyFaster)

```bash
# Go to any project folder
cd Guardrails  # or MCP_demo or WebsocketsDemo

# Initialize and setup
uv init
uv venv
uv add -r requirements.txt
```

### Using `venv` (Standard)

```bash
# Go to any project folder
cd Guardrails


### Webhooks
- **HTTP Callbacks**: Server sends POST requests to registered endpoints
- **Event-driven**: Server triggers HTTP calls on events
- **Decoupled**: Services don't need direct connection
- **Scalable**: No persistent connections needed
# Create virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Using `conda`

```bash
cd Guardrails

conda create --name guardrails python=3.10
conda activate guardrails
conda install --file requirements.txt
```

---

## 📝 Learning Path

**Beginners:**
1. Start with **WebsocketsDemo** - Understand real-time web communication
2. Progress to **Guardrails** - Learn AI integration basics
3. Advance to **MCP_demo** - Understand tool-driven architecture

**Intermediate/Advanced:**
- Combine concepts: Build a real-time chat with AI (Guardrails + WebsocketsDemo)
- Extend MCP tools: Add custom servers to MCP_demo
- Deploy: Use deployment strategies for production

---

## 🔗 Integration Ideas

**Project Combinations:**

1. **AI Chat with MCP Tools**
   - Use WebsocketsDemo's UI
   - Integrate Guardrails for safe responses
   - Connect MCP_demo tools for extended functionality

2. **Tool Discovery Dashboard**
   - Create a web interface for MCP servers
   - Real-time tool availability via WebSockets
   - AI-powered tool recommendations

3. **Activity Analytics**
   - Extend WebsocketsDemo's logging
   - Use Guardrails to generate insights
   - Expose data via MCP tools

---

## 🔑 Key Concepts to Understand

### Guardrails
- **Guardrails**: Rules that ensure AI outputs are safe, accurate, and appropriate
- **LLM Chains**: Sequential operations with language models
- **Prompting**: Crafting effective instructions for AI models

### MCP (Model Context Protocol)
- **Server**: Provides tools and resources
- **Client**: Discovers and uses tools
- **Tools**: Discrete operations (math, weather, database queries, etc.)
- **Transport**: How client-server communicate (stdio, HTTP, WebSocket, etc.)

### WebSockets
- **Full-duplex**: Both client and server can send data anytime
- **Event-driven**: Push notifications without polling
- **Real-time**: Immediate delivery (milliseconds)
- **Stateful**: Connection persists until closed

---

## 📚 Useful Resources

### Guardrails
- [LangChain Documentation](https://python.langchain.com/)
- [Groq API Docs](https://console.groq.com/)

### MCP
- [MCP Specification](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

### WebSockets
- [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)
- [MDN WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

---

## ⚙️ Configuration

Each project may require API keys or environment variables:

```bash
# Create a .env file in the project root
# Example:
GROQ_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

Check individual project READMEs for specific configuration needs.

---

## 🤝 Contributing & Extending

Each project is self-contained but can be extended:

- **Add new guardrails** to the Guardrails project
- **Create new MCP servers** (calendar, database, APIs, etc.)
- **Enhance the chat UI** with new features

---

## 📝 Notes for Learners

- Each project has minimal main code intentionally - **you're expected to build on them**
- Check the `requirements.txt` in each folder before running
- Read individual project READMEs for detailed documentation
- Start small and experiment - modify code, break things, fix them!

---

**Happy Learning! 🎓**
