"""Example: Basic window control."""

from whendoes.llm import create_provider
from whendoes.agent import Agent, ToolRegistry
from whendoes.cli.repl import setup_tools

# Initialize LLM provider
llm = create_provider(
    "anthropic",
    api_key="your-api-key-here",
    model="claude-3-5-sonnet-20241022",
)

# Set up tools
tools = setup_tools()

# Create agent
agent = Agent(llm, tools, require_approval=True)

# Run a command
response = agent.run("List all open windows")
print(response)

# Another example
response = agent.run("Close the Chrome window")
print(response)
