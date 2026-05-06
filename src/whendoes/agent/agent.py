"""Main agent implementation."""

from typing import Any, Optional, Callable
from whendoes.llm.base import BaseLLMProvider, Message
from whendoes.agent.tool_registry import ToolRegistry
from whendoes.agent.context import AgentContext
from whendoes.agent.human_like_behavior import HumanLikeBehavior


class Agent:
    """Agentic reasoning loop."""

    def __init__(
        self,
        llm_provider: BaseLLMProvider,
        tool_registry: ToolRegistry,
        max_iterations: int = 10,
        require_approval: bool = True,
        verbose: bool = False,
        stream_callback: Optional[Callable[[str], None]] = None,
        human_like: bool = False,
    ):
        """Initialize agent.

        Args:
            llm_provider: LLM provider instance
            tool_registry: Tool registry
            max_iterations: Maximum reasoning iterations
            require_approval: Require approval for destructive ops
            verbose: Verbose logging
            stream_callback: Callback for streaming output
            human_like: Enable human-like behavior with delays
        """
        self.llm = llm_provider
        self.tools = tool_registry
        self.max_iterations = max_iterations
        self.require_approval = require_approval
        self.verbose = verbose
        self.stream_callback = stream_callback
        self.human_like = human_like
        self.behavior = HumanLikeBehavior(stream_callback) if human_like else None

    def run(self, user_input: str, system_prompt: Optional[str] = None) -> str:
        """Run agent reasoning loop.

        Args:
            user_input: User query
            system_prompt: System prompt for LLM

        Returns:
            Final response
        """
        context = AgentContext(
            user_input=user_input,
            max_iterations=self.max_iterations,
            require_approval=self.require_approval,
            verbose=self.verbose,
        )

        # Add initial user message
        context.add_message("user", user_input)

        # Default system prompt
        if not system_prompt:
            system_prompt = self._get_default_system_prompt()

        # Reasoning loop
        while context.should_continue():
            context.increment_iteration()

            if self.verbose:
                print(f"\n[Iteration {context.iterations}]")

            # Get LLM response - convert context messages to Message objects
            messages = []
            for msg in context.messages:
                messages.append(
                    Message(
                        role=msg["role"],
                        content=msg["content"],
                        tool_call_id=msg.get("tool_call_id"),
                    )
                )

            response = self.llm.chat(
                messages=messages,
                tools=self.tools.get_tools_for_llm(),
                system=system_prompt,
            )

            if self.verbose:
                print(f"LLM Response: {response.content}")

            # Stream thinking if callback provided
            if self.stream_callback and response.content:
                if self.human_like and self.behavior:
                    self.behavior.think(0.5)
                    self.behavior.stream(f"{response.content}\n")
                else:
                    self.stream_callback(f"💭 {response.content}\n")

            # Add assistant response
            context.add_message("assistant", response.content)

            # Check if we're done
            if not response.tool_calls or response.stop_reason == "end_turn":
                return response.content

            # Execute tool calls
            for tool_call in response.tool_calls:
                if self.verbose:
                    print(f"Tool Call: {tool_call.name}({tool_call.arguments})")

                # Stream tool call if callback provided
                if self.stream_callback:
                    if self.human_like and self.behavior:
                        self.behavior.execute(tool_call.name, str(tool_call.arguments))
                    else:
                        self.stream_callback(f"🔧 Calling: {tool_call.name}({tool_call.arguments})\n")

                # Check if approval needed
                tool = self.tools.get_tool(tool_call.name)
                if tool and tool.requires_approval and self.require_approval:
                    approval = self._request_approval(tool_call.name, tool_call.arguments)
                    if not approval:
                        context.add_message(
                            "tool",
                            f"Tool {tool_call.name} execution denied by user",
                            tool_call_id=tool_call.id,
                        )
                        continue

                # Execute tool
                result = self.tools.execute_tool(tool_call.name, tool_call.arguments)
                context.add_tool_call(tool_call.name, tool_call.arguments, result)

                if self.verbose:
                    print(f"Tool Result: {result}")

                # Stream result if callback provided
                if self.stream_callback:
                    if self.human_like and self.behavior:
                        self.behavior.success(f"{str(result)[:100]}")
                    else:
                        self.stream_callback(f"✓ Result: {str(result)[:100]}...\n")

                # Add tool result to messages with tool_call_id
                context.add_message(
                    "tool",
                    f"{tool_call.name}: {str(result)}",
                    tool_call_id=tool_call.id,
                )

        # Max iterations reached
        return "Maximum iterations reached. Unable to complete request."

    def _get_default_system_prompt(self) -> str:
        """Get default system prompt.

        Returns:
            System prompt
        """
        return """You are a helpful Windows automation assistant. You have access to tools
to control windows, processes, files, and system operations.

When the user asks you to do something:
1. Think about what tools you need to use
2. Use the appropriate tools to accomplish the task
3. Report back with the results

Be concise and helpful. If something fails, explain why and suggest alternatives."""

    def _request_approval(self, tool_name: str, arguments: dict[str, Any]) -> bool:
        """Request user approval for tool execution.

        Args:
            tool_name: Tool name
            arguments: Tool arguments

        Returns:
            True if approved
        """
        print(f"\n⚠️  Approval Required")
        print(f"Tool: {tool_name}")
        print(f"Arguments: {arguments}")
        response = input("Proceed? (y/n): ").strip().lower()
        return response == "y"
