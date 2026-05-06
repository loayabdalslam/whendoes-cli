"""Example: Human-like Chrome Automation with Streaming."""

from whendoes.llm import create_provider
from whendoes.agent.human_like_behavior import ChromeAccessibilityAgent
from whendoes.config import get_config


def stream_callback(text: str) -> None:
    """Callback for streaming output."""
    print(text, end="", flush=True)


def main():
    """Demonstrate human-like Chrome automation."""

    # Get configuration
    config = get_config()

    # Create LLM provider
    llm = create_provider(
        config.llm.provider,
        api_key=config.llm.api_key,
        model=config.llm.model,
    )

    # Create Chrome Accessibility Agent with streaming
    agent = ChromeAccessibilityAgent(llm, stream_callback=stream_callback)

    print("\n" + "=" * 60)
    print("🤖 Chrome Accessibility Agent - Human-like Behavior")
    print("=" * 60)

    # Example tasks
    tasks = [
        "Search for 'Python programming' on Google",
        "Find the first search result and click it",
        "Scroll down to see more content",
    ]

    for task in tasks:
        print()
        result = agent.execute_task(task)
        print(f"\n📊 Result: {result}\n")

    # Show action history
    print("\n" + "=" * 60)
    print("📋 Action History")
    print("=" * 60)
    history = agent.get_action_history()
    for i, action in enumerate(history, 1):
        print(f"{i}. {action['action']}: {action['details']}")

    # Interactive mode
    print("\n" + "=" * 60)
    print("💬 Interactive Mode")
    print("=" * 60)
    print("Enter tasks (type 'exit' to quit):\n")

    while True:
        task = input("Task: ").strip()
        if task.lower() == "exit":
            break

        if not task:
            continue

        result = agent.execute_task(task)
        print(f"\n✅ {result}\n")


if __name__ == "__main__":
    main()
