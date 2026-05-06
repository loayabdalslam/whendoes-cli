# Whendoes CLI

An agentic CLI application that converts Windows API functions into natural language commands. Control applications, windows, and system operations through conversational AI with support for multiple LLM providers.

## Features

- 🤖 **Multi-LLM Support**: OpenAI, Anthropic, Groq, Google Gemini, OpenRouter, Ollama
- 🪟 **Windows API Integration**: Window management, process control, file operations, app launching
- 💬 **Natural Language Interface**: Chat-based terminal for intuitive control
- 🔒 **Safety First**: Approval prompts for destructive operations
- 🧪 **Fully Tested**: Comprehensive unit and integration tests
- ⚙️ **Flexible Configuration**: Environment variables and config files
- 🔍 **App Discovery**: Automatically finds installed applications
- 📡 **Streaming Output**: Real-time feedback during agent reasoning

## Quick Start

### Installation

```bash
pip install -e .
```

### Setup

```bash
whendoes setup
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

## Documentation

For complete documentation, see [DOCUMENTATION.md](DOCUMENTATION.md) which includes:

- **Quick Start Guide** - Installation and setup instructions
- **Architecture** - Core components and design patterns
- **Configuration** - Environment variables and provider setup
- **Development** - Testing, code quality, and development workflow
- **Adding Tools** - How to add new Windows API functions
- **Adding Providers** - How to add new LLM providers
- **Session Behavior** - REPL loop and chat flow
- **Context Engineering** - Message history and tool correlation
- **Troubleshooting** - Common issues and solutions

## Configuration

Create a `.env` file in your project root:

```env
# LLM Provider (openai, anthropic, groq, gemini, openrouter, ollama)
LLM_PROVIDER=anthropic

# API Keys
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
OPENROUTER_API_KEY=your_key_here

# Model selection
LLM_MODEL=claude-3-5-sonnet-20241022

# Agent settings
AGENT_MAX_ITERATIONS=10
AGENT_REQUIRE_APPROVAL=true
AGENT_VERBOSE=false
```

## Development

Run tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=src/whendoes
```

Format code:

```bash
black src/ tests/
```

Lint:

```bash
ruff check src/ tests/
```

## License

MIT
