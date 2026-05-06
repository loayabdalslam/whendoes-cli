"""Test script to verify the fix works."""

from whendoes.llm import create_provider
from whendoes.agent import Agent
from whendoes.cli.repl import setup_tools

# Create LLM provider
print("Creating LLM provider...")
llm = create_provider(
    "anthropic",
    api_key="your-api-key-here",  # Replace with your key
    model="claude-3-5-sonnet-20241022",
)

# Set up tools
print("Setting up tools...")
tools = setup_tools()

# Create agent
print("Creating agent...")
agent = Agent(llm, tools, require_approval=False, verbose=True)

# Test: Create file and write to it
print("\n" + "=" * 60)
print("TEST: Create file and write 'hello world'")
print("=" * 60 + "\n")

try:
    result = agent.run("Create a file at C:\\temp\\test.txt and write 'hello world' to it")
    print(f"\n✓ Success!\nResult: {result}")
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
