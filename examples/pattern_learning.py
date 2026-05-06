"""Advanced example: Pattern learning and generalization."""

from whendoes.llm import create_provider
from whendoes.agent.smart_ui_agent import SmartUIAgent, setup_ui_tools
from whendoes.ui_automation import get_window_ui_context
import json

# Initialize LLM
llm = create_provider(
    "groq",
    api_key="your-groq-api-key",
    model="mixtral-8x7b-32768",
)

tools = setup_ui_tools()
agent = SmartUIAgent(llm, tools, verbose=True)

print("=" * 60)
print("ADVANCED: Pattern Learning Without Screenshots")
print("=" * 60)

# Step 1: Show how the agent sees the UI (no images!)
print("\n[Step 1] Extracting UI Context (No Screenshots)\n")
print("What the agent sees when looking at Notepad:")
print("-" * 60)

ui_context = get_window_ui_context("Notepad", max_depth=3)
context_data = json.loads(ui_context)

print(json.dumps(context_data, indent=2, ensure_ascii=False))

print("\n" + "-" * 60)
print("Notice: Pure text description, no images needed!")
print("The agent understands:")
print("  • Element types (Button, TextBox, Menu, etc)")
print("  • Element names and IDs")
print("  • Supported patterns (Invoke, Value, etc)")
print("  • Spatial relationships")

# Step 2: Demonstrate pattern generalization
print("\n\n[Step 2] Pattern Generalization\n")
print("The agent learns these universal patterns:")
print("-" * 60)

patterns = {
    "Opening Files": {
        "Pattern": "Find 'File' menu → Click → Find 'Open' → Click",
        "Works in": ["Notepad", "Word", "Excel", "VS Code", "Any app"],
    },
    "Saving Files": {
        "Pattern": "Find 'File' menu → Click → Find 'Save' → Click",
        "Works in": ["Notepad", "Word", "Excel", "VS Code", "Any app"],
    },
    "Text Input": {
        "Pattern": "Find TextBox element → Click → Type text",
        "Works in": ["Notepad", "Word", "Search boxes", "Forms"],
    },
    "Selecting Items": {
        "Pattern": "Find List/ComboBox → Click item → Select",
        "Works in": ["Dropdowns", "Lists", "Menus"],
    },
}

for pattern_name, details in patterns.items():
    print(f"\n{pattern_name}:")
    print(f"  Pattern: {details['Pattern']}")
    print(f"  Works in: {', '.join(details['Works in'])}")

# Step 3: Show how agent adapts to new applications
print("\n\n[Step 3] Adaptation to New Applications\n")
print("When the agent encounters a new app:")
print("-" * 60)

adaptation_steps = [
    "1. Extract UI context (get element names, types, patterns)",
    "2. Match against known patterns (File menu, TextBox, etc)",
    "3. Apply learned logic to new context",
    "4. Execute actions using standard patterns",
    "5. Learn from results for future interactions",
]

for step in adaptation_steps:
    print(f"  {step}")

# Step 4: Practical example
print("\n\n[Step 4] Practical Example: Multi-App Workflow\n")
print("Request: 'Create a document with title and save it'")
print("-" * 60)

workflow = [
    {
        "App": "Notepad",
        "Agent Reasoning": "Need to create new file → Find File menu → Click New",
        "Action": "click_element('Notepad', 'elem_3')",
    },
    {
        "App": "Notepad",
        "Agent Reasoning": "Need to type title → Find TextBox → Type",
        "Action": "type_text('Notepad', 'elem_5', 'My Document')",
    },
    {
        "App": "Notepad",
        "Agent Reasoning": "Need to save → Find File menu → Click Save",
        "Action": "click_element('Notepad', 'elem_2')",
    },
]

for i, step in enumerate(workflow, 1):
    print(f"\nStep {i}: {step['App']}")
    print(f"  Reasoning: {step['Agent Reasoning']}")
    print(f"  Action: {step['Action']}")

# Step 5: Key advantages
print("\n\n[Step 5] Key Advantages of This Approach\n")
print("-" * 60)

advantages = [
    "✓ No screenshots needed (faster, less bandwidth)",
    "✓ Works with any Windows application",
    "✓ Understands UI structure, not just pixels",
    "✓ Generalizes patterns across apps",
    "✓ Accessible (works with screen readers)",
    "✓ Deterministic (same UI = same result)",
    "✓ Can work offline with local LLM",
]

for advantage in advantages:
    print(f"  {advantage}")

print("\n" + "=" * 60)
print("This is how the agent learns without training!")
print("=" * 60)
