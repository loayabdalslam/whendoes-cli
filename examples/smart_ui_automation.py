"""Example: Smart UI automation without screenshots."""

from whendoes.llm import create_provider
from whendoes.agent.smart_ui_agent import SmartUIAgent, setup_ui_tools

# Initialize LLM provider
llm = create_provider(
    "anthropic",
    api_key="your-api-key-here",
    model="claude-3-5-sonnet-20241022",
)

# Set up UI tools
tools = setup_ui_tools()

# Create smart UI agent
agent = SmartUIAgent(llm, tools, require_approval=True, verbose=True)

# Example 1: Interact with Notepad
print("=== Example 1: Notepad Automation ===\n")
result = agent.interact_with_window(
    "Notepad",
    "اكتب 'مرحباً بك في Whendoes' ثم احفظ الملف",
)
print(f"Result: {result}\n")

# Example 2: Interact with any application
print("=== Example 2: Generic Application Control ===\n")
result = agent.interact_with_window(
    "Calculator",
    "احسب 5 + 3 واعرض النتيجة",
)
print(f"Result: {result}\n")

# Example 3: Complex workflow
print("=== Example 3: Complex Workflow ===\n")
result = agent.interact_with_window(
    "Word",
    "افتح ملف جديد، اكتب عنوان 'تقرير'، ثم أضف فقرة تحته",
)
print(f"Result: {result}\n")
