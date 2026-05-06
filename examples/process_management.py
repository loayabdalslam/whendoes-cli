"""Example: Process management."""

from whendoes.llm import create_provider
from whendoes.agent import Agent, ToolRegistry
from whendoes.cli.repl import setup_tools

# Initialize with Groq (faster, free tier available)
llm = create_provider(
    "groq",
    api_key="your-groq-api-key",
    model="mixtral-8x7b-32768",
)

# Set up tools
tools = setup_tools()

# Create agent
agent = Agent(llm, tools, require_approval=True)

# Examples
print("=== Process Management Examples ===\n")

# List processes
response = agent.run("Show me all running processes")
print(f"Response: {response}\n")

# Start an application
response = agent.run("Start Notepad")
print(f"Response: {response}\n")

# Get system info
response = agent.run("What is the current system information?")
print(f"Response: {response}\n")
