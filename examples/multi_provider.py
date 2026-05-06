"""Example: Using different LLM providers."""

from whendoes.llm import create_provider
from whendoes.agent import Agent
from whendoes.cli.repl import setup_tools

# Set up tools once
tools = setup_tools()

# Example 1: Using Anthropic (Claude)
print("=== Using Anthropic ===")
llm_anthropic = create_provider(
    "anthropic",
    api_key="your-anthropic-api-key",
    model="claude-3-5-sonnet-20241022",
)
agent = Agent(llm_anthropic, tools)
response = agent.run("List all open windows")
print(f"Response: {response}\n")

# Example 2: Using OpenAI (GPT-4)
print("=== Using OpenAI ===")
llm_openai = create_provider(
    "openai",
    api_key="your-openai-api-key",
    model="gpt-4-turbo",
)
agent = Agent(llm_openai, tools)
response = agent.run("Start Notepad")
print(f"Response: {response}\n")

# Example 3: Using Groq (fast, free)
print("=== Using Groq ===")
llm_groq = create_provider(
    "groq",
    api_key="your-groq-api-key",
    model="mixtral-8x7b-32768",
)
agent = Agent(llm_groq, tools)
response = agent.run("Get system information")
print(f"Response: {response}\n")

# Example 4: Using Ollama (local, offline)
print("=== Using Ollama (Local) ===")
llm_ollama = create_provider(
    "ollama",
    model="llama2",
    base_url="http://localhost:11434",
)
agent = Agent(llm_ollama, tools)
response = agent.run("What processes are running?")
print(f"Response: {response}\n")

# Example 5: Using Google Gemini
print("=== Using Google Gemini ===")
llm_gemini = create_provider(
    "gemini",
    api_key="your-google-api-key",
    model="gemini-1.5-pro",
)
agent = Agent(llm_gemini, tools)
response = agent.run("Close the Chrome window")
print(f"Response: {response}\n")

# Example 6: Using OpenRouter (access to multiple models)
print("=== Using OpenRouter ===")
llm_openrouter = create_provider(
    "openrouter",
    api_key="your-openrouter-api-key",
    model="openrouter/auto",
)
agent = Agent(llm_openrouter, tools)
response = agent.run("Create a file at C:\\temp\\test.txt")
print(f"Response: {response}\n")
