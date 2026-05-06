"""Tool registry for agent."""

from typing import Any, Callable, Optional
from dataclasses import dataclass


@dataclass
class Tool:
    """Tool definition."""

    name: str
    description: str
    func: Callable
    parameters: dict[str, Any]
    requires_approval: bool = False


class ToolRegistry:
    """Registry for available tools."""

    def __init__(self):
        """Initialize tool registry."""
        self.tools: dict[str, Tool] = {}

    def register(
        self,
        name: str,
        description: str,
        func: Callable,
        parameters: dict[str, Any],
        requires_approval: bool = False,
    ) -> None:
        """Register a tool.

        Args:
            name: Tool name
            description: Tool description
            func: Callable function
            parameters: Parameter schema (OpenAI format)
            requires_approval: Whether tool requires user approval
        """
        self.tools[name] = Tool(
            name=name,
            description=description,
            func=func,
            parameters=parameters,
            requires_approval=requires_approval,
        )

    def get_tool(self, name: str) -> Optional[Tool]:
        """Get tool by name.

        Args:
            name: Tool name

        Returns:
            Tool object or None
        """
        return self.tools.get(name)

    def get_all_tools(self) -> list[Tool]:
        """Get all registered tools.

        Returns:
            List of Tool objects
        """
        return list(self.tools.values())

    def get_tools_for_llm(self) -> list[dict[str, Any]]:
        """Get tools in OpenAI format for LLM.

        Returns:
            List of tool definitions
        """
        tools = []
        for tool in self.tools.values():
            tools.append(
                {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters,
                }
            )
        return tools

    def execute_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        """Execute a tool.

        Args:
            name: Tool name
            arguments: Tool arguments

        Returns:
            Tool result

        Raises:
            ValueError: If tool not found
        """
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool not found: {name}")

        try:
            return tool.func(**arguments)
        except Exception as e:
            return f"Error executing {name}: {str(e)}"
