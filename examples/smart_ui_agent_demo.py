"""Example: Smart UI Agent - Understanding browser content without screenshots."""

from whendoes.llm import create_provider
from whendoes.agent.smart_ui_agent_new import SmartUIAgent
from whendoes.config import get_config


def main():
    """Demonstrate Smart UI Agent capabilities."""

    # Get configuration
    config = get_config()

    # Create LLM provider
    llm = create_provider(
        config.llm.provider,
        api_key=config.llm.api_key,
        model=config.llm.model,
    )

    # Create Smart UI Agent for Chrome
    agent = SmartUIAgent(llm, app_name="chrome")

    print("=" * 60)
    print("Smart UI Agent - Browser Content Understanding")
    print("=" * 60)
    print()

    # Example 1: Read UI tree
    print("📖 Reading UI Tree from Chrome...")
    print("-" * 60)
    ui_tree = agent.read_ui_tree(max_depth=6)
    if ui_tree:
        print(ui_tree)
    else:
        print("❌ Failed to read UI tree. Make sure Chrome is running.")
        return

    print()
    print("=" * 60)
    print()

    # Example 2: Understand UI and get action
    print("🤖 Understanding User Query...")
    print("-" * 60)

    user_query = "Find the search box and search for 'Python programming'"
    print(f"User Query: {user_query}")
    print()

    response = agent.understand_ui(user_query)
    print("LLM Response:")
    print(response)

    print()
    print("=" * 60)
    print()

    # Example 3: Find elements by role
    print("🔍 Finding All Buttons in UI...")
    print("-" * 60)

    buttons = agent.find_elements_by_role("button")
    print(f"Found {len(buttons)} buttons:")
    for btn in buttons[:5]:  # Show first 5
        print(f"  - [{btn.id}] {btn.name}")

    print()
    print("=" * 60)
    print()

    # Example 4: Interactive mode
    print("💬 Interactive Mode")
    print("-" * 60)
    print("Enter your queries (type 'exit' to quit):")
    print()

    while True:
        query = input("You: ").strip()
        if query.lower() == "exit":
            break

        if not query:
            continue

        print()
        print("🤖 Analyzing UI...")
        response = agent.understand_ui(query)
        print(f"Assistant: {response}")
        print()


if __name__ == "__main__":
    main()
