# Whendoes CLI - Complete Documentation

## Overview

Whendoes CLI is an agentic application that converts Windows API functions into natural language commands. Users can control applications, windows, and system operations through conversational AI with support for multiple LLM providers (Anthropic, OpenAI, Groq, Google Gemini, OpenRouter, Ollama).

---

## Quick Start

### Installation

```bash
pip install -e .
```

### Setup

```bash
whendoes setup
```

Or manually create `.env`:

```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_key_here
LLM_MODEL=claude-3-5-sonnet-20241022
```

### Run

```bash
whendoes
```

### Example Commands

```
You: List all open windows
You: Close the Chrome window
You: Start Notepad
You: Create a file at C:\temp\test.txt with content "Hello World"
You: Get system information
```

---

## Architecture

### Core Components

1. **LLM Provider Abstraction** (`src/whendoes/llm/`)
   - Base class: `BaseLLMProvider`
   - Implementations: Anthropic, OpenAI, Groq, Google Gemini, OpenRouter, Ollama
   - Factory pattern for provider creation
   - Unified interface for all providers

2. **Windows API Wrappers** (`src/whendoes/windows_api/`)
   - Window management (list, focus, close, minimize, maximize)
   - Process management (list, start, stop, kill)
   - File operations (create, delete, copy, move, read, write)
   - Application launching with auto-discovery
   - System information retrieval

3. **Agent System** (`src/whendoes/agent/`)
   - `Agent`: Main reasoning loop using ReAct pattern
   - `ToolRegistry`: Tool registration and management
   - `AgentContext`: Execution state and history
   - Streaming support for real-time output

4. **CLI Interface** (`src/whendoes/cli/`)
   - Interactive REPL for user interaction
   - Tool setup and configuration
   - Rich terminal formatting with emojis
   - Special commands (help, info, exit)

5. **Configuration** (`src/whendoes/config/`)
   - Pydantic-based configuration management
   - Environment variable support
   - Per-provider settings

### File Structure

```
whendoes-cli/
├── src/whendoes/
│   ├── __init__.py
│   ├── config/              # Configuration management
│   ├── llm/                 # LLM providers
│   ├── windows_api/         # Windows API wrappers
│   ├── agent/               # Agent system
│   └── cli/                 # CLI interface
├── tests/                   # Unit tests
├── examples/                # Usage examples
├── pyproject.toml           # Project metadata
├── requirements.txt         # Dependencies
└── README.md                # User documentation
```

---

## Key Design Decisions

### Provider Abstraction
All LLM providers implement a common interface (`BaseLLMProvider`) with:
- `chat()`: Send messages and receive responses
- `validate_config()`: Verify provider configuration

This allows seamless switching between providers without changing agent code.

### Tool Registry Pattern
Windows API functions are registered as tools with:
- Name and description
- Parameter schema (OpenAI format)
- Approval requirement flag for destructive operations

### ReAct Pattern
Agent uses Reasoning + Acting loop:
1. Receive user input
2. Call LLM with available tools
3. Execute tool calls
4. Add results to context
5. Repeat until done or max iterations

### Safety First
- Destructive operations (delete, kill, uninstall) require user approval
- Approval prompts show tool name and arguments
- Audit trail of all operations

### Streaming Output
- Agent streams thinking (💭), tool calls (🔧), and results (✓) in real-time
- Provides user feedback during long operations
- Makes agent reasoning transparent and debuggable

### App Discovery
- `find_app_path()` automatically searches for installed applications
- Searches: Program Files, Program Files (x86), Registry, common locations
- Special handlers for Chrome, Firefox, Edge, Notepad, VSCode, Python
- Enables agent to launch apps without user providing full paths

---

## Configuration

### Environment Variables

```env
# Provider selection
LLM_PROVIDER=anthropic

# API Keys
ANTHROPIC_API_KEY=...
OPENAI_API_KEY=...
GROQ_API_KEY=...
GOOGLE_API_KEY=...
OPENROUTER_API_KEY=...

# Model selection
LLM_MODEL=claude-3-5-sonnet-20241022

# Agent settings
AGENT_MAX_ITERATIONS=10
AGENT_REQUIRE_APPROVAL=true
AGENT_VERBOSE=false

# CLI settings
CLI_DEBUG=false

# Ollama (local)
OLLAMA_BASE_URL=http://localhost:11434
```

### LLM Providers

| Provider | Setup | Cost | Speed | Capability |
|----------|-------|------|-------|------------|
| Anthropic | API key from console.anthropic.com | Free tier | Medium | Excellent |
| OpenAI | API key from platform.openai.com | Pay-per-use | Medium | Excellent |
| Groq | API key from console.groq.com | Free tier | Fast | Good |
| Google Gemini | API key from makersuite.google.com | Free tier | Medium | Good |
| OpenRouter | API key from openrouter.io | Pay-per-use | Medium | Excellent |
| Ollama | Local installation | Free | Slow | Fair |

---

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/whendoes

# Run specific test file
pytest tests/test_agent.py

# Run specific test
pytest tests/test_agent.py::TestAgent::test_agent_run_simple
```

### Running the CLI

```bash
# Install in development mode
pip install -e .

# Run interactive CLI
whendoes

# Or directly
python -m whendoes.cli.main
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint
ruff check src/ tests/

# Type checking
mypy src/
```

---

## Adding New Tools

To add a new Windows API function as a tool:

1. Implement the function in the appropriate module (`window_manager.py`, `process_manager.py`, etc.)
2. Register it in `src/whendoes/cli/repl.py` in the `setup_tools()` function:

```python
registry.register(
    "tool_name",
    "Tool description",
    function_reference,
    {
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "..."},
        },
        "required": ["param1"],
    },
    requires_approval=False,  # Set to True for destructive ops
)
```

---

## Adding New LLM Providers

To add a new LLM provider:

1. Create a new file in `src/whendoes/llm/` (e.g., `new_provider.py`)
2. Implement the `BaseLLMProvider` interface
3. Add to the factory in `src/whendoes/llm/__init__.py`

Example:

```python
class NewProvider(BaseLLMProvider):
    def chat(self, messages, tools=None, system=None):
        # Implementation
        pass
    
    def validate_config(self):
        # Implementation
        pass
```

---

## Session Chat Behavior

### REPL Loop Flow
1. Display welcome panel with instructions
2. Check API key configuration (prompt setup if missing)
3. Initialize LLM provider and tool registry
4. Create agent with streaming callback
5. Enter infinite loop:
   - Prompt user for input
   - Handle special commands (exit, help, info)
   - Run agent with streaming output
   - Display assistant response
   - Continue to next iteration

### Special Commands
- `exit` — Gracefully exit the CLI
- `help` — Show available commands and examples
- `info` — Display provider information

### Error Handling
- Catches KeyboardInterrupt (Ctrl+C) gracefully
- Displays error messages in red
- Continues REPL loop after errors
- Doesn't crash on tool execution failures

---

## Main Context Behavior

### Initialization Flow
1. Load configuration from environment variables and .env file
2. Validate LLM provider is configured
3. Prompt for setup if API key missing
4. Create LLM provider instance with config
5. Set up tool registry with all available tools
6. Create agent with provider, tools, and config settings
7. Start REPL session

### Tool Registry Context
- All Windows API tools registered at startup
- Tools include: window management, process control, file operations, app launching, system info
- Each tool has schema, description, and approval requirements
- Tools available to agent throughout session

### Agent Context
- Created once per session
- Reused for all user queries
- Maintains conversation history across turns
- Streaming callback connected to REPL output

---

## Agentic Context Engineering

### Message History Management
- Stores role, content, and tool_call_id for each message
- Maintains conversation thread for LLM context
- Enables multi-turn reasoning with tool results

### Tool Call ID Correlation
- Each tool call gets unique ID from LLM
- Tool result message includes same ID
- Allows LLM to correlate results with original calls
- Critical for multi-tool workflows

### Iteration Control
- Tracks current iteration count
- Enforces max_iterations limit
- Prevents infinite loops
- Allows graceful degradation

### Tool Call Tracking
- Records tool name, arguments, and result
- Enables audit trail of operations
- Supports debugging and analysis
- Useful for learning patterns

### Message Format
```python
{
    "role": "user|assistant|tool",
    "content": "message text",
    "tool_call_id": "call_123"  # Only for tool messages
}
```

---

## Testing Strategy

### Unit Tests
- LLM providers: Mock API responses, test parsing
- Windows API: Mock system calls, test error handling
- Agent: Test reasoning loop and tool selection
- Configuration: Test config loading and validation

### Integration Tests
- End-to-end workflows (query → reasoning → execution → result)
- Multi-step tasks requiring multiple tool calls
- Error handling and recovery

### Manual Testing
- Interactive CLI testing with real providers
- Real Windows operations
- Error scenarios and edge cases

---

## Common Issues

### LLM Provider Not Responding
- Check API key is set correctly
- Verify network connectivity
- Check provider status page

### Tool Execution Fails
- Check Windows API wrapper error handling
- Verify parameters are correct
- Check system permissions

### Agent Loops Infinitely
- Check `max_iterations` setting
- Verify tool registry has correct tools
- Check LLM is returning proper stop reasons

### "Connection error" or "API key not found"
```bash
# Run setup again
whendoes setup

# Or manually create .env with your API key
```

### "Module not found" errors
```bash
# Reinstall dependencies
pip install -e .
```

### Ollama not connecting
```bash
# Make sure Ollama is running
ollama serve

# In another terminal, pull a model
ollama pull llama2

# Then run whendoes
whendoes
```

### Permission denied errors
- Some operations (like closing windows) require user approval
- When prompted, type `y` to approve or `n` to deny

---

## Features

- 🤖 **Multi-LLM Support**: OpenAI, Anthropic, Groq, Google Gemini, OpenRouter, Ollama
- 🪟 **Windows API Integration**: Window management, process control, file operations, app launching
- 💬 **Natural Language Interface**: Chat-based terminal for intuitive control
- 🔒 **Safety First**: Approval prompts for destructive operations
- 🧪 **Fully Tested**: Comprehensive unit and integration tests
- ⚙️ **Flexible Configuration**: Environment variables and config files
- 🔍 **App Discovery**: Automatically finds installed applications
- 📡 **Streaming Output**: Real-time feedback during agent reasoning

---

## Future Enhancements

- [ ] Keyboard/mouse automation tools
- [ ] Registry manipulation
- [ ] Network operations
- [ ] Scheduled task management
- [ ] Persistent conversation history
- [ ] Multi-user support
- [ ] Web UI interface
- [ ] Plugin system for custom tools
- [ ] Performance optimization
- [ ] Comprehensive logging

---

## Contributing

When making changes:
1. Write tests for new functionality
2. Run full test suite before committing
3. Follow code style (black, ruff)
4. Update documentation
5. Keep commits focused and descriptive

---

## License

MIT
