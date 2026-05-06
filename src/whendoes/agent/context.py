"""Agent context and state management."""

from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime


@dataclass
class AgentContext:
    """Agent execution context."""

    user_input: str
    messages: list[dict[str, Any]] = field(default_factory=list)
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    iterations: int = 0
    max_iterations: int = 10
    start_time: datetime = field(default_factory=datetime.now)
    require_approval: bool = True
    verbose: bool = False

    def add_message(
        self, role: str, content: str, tool_call_id: Optional[str] = None
    ) -> None:
        """Add message to context.

        Args:
            role: Message role (user, assistant, tool)
            content: Message content
            tool_call_id: Tool call ID (for tool messages)
        """
        msg = {"role": role, "content": content}
        if tool_call_id:
            msg["tool_call_id"] = tool_call_id
        self.messages.append(msg)

    def add_tool_call(self, tool_name: str, arguments: dict[str, Any], result: Any) -> None:
        """Add tool call to context.

        Args:
            tool_name: Tool name
            arguments: Tool arguments
            result: Tool result
        """
        self.tool_calls.append(
            {
                "tool": tool_name,
                "arguments": arguments,
                "result": result,
            }
        )

    def should_continue(self) -> bool:
        """Check if agent should continue iterating.

        Returns:
            True if should continue
        """
        return self.iterations < self.max_iterations

    def increment_iteration(self) -> None:
        """Increment iteration counter."""
        self.iterations += 1

    def get_elapsed_time(self) -> float:
        """Get elapsed time in seconds.

        Returns:
            Elapsed time
        """
        return (datetime.now() - self.start_time).total_seconds()

