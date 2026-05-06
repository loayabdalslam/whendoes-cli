"""Example: File operations."""

from whendoes.llm import create_provider
from whendoes.agent import Agent, ToolRegistry
from whendoes.cli.repl import setup_tools

# Initialize with OpenAI
llm = create_provider(
    "openai",
    api_key="your-openai-api-key",
    model="gpt-4-turbo",
)

# Set up tools
tools = setup_tools()

# Create agent
agent = Agent(llm, tools, require_approval=True)

# Examples
print("=== File Operations Examples ===\n")

# Create a file
response = agent.run("Create a file at C:\\temp\\test.txt with content 'Hello World'")
print(f"Response: {response}\n")

# List files
response = agent.run("List all files in C:\\temp")
print(f"Response: {response}\n")

# Read file
response = agent.run("Read the content of C:\\temp\\test.txt")
print(f"Response: {response}\n")

# Copy file
response = agent.run("Copy C:\\temp\\test.txt to C:\\temp\\test_backup.txt")
print(f"Response: {response}\n")
