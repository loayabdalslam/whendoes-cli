"""Smart agent that learns UI patterns without screenshots."""

from typing import Optional
from whendoes.llm.base import BaseLLMProvider, Message
from whendoes.agent.tool_registry import ToolRegistry
from whendoes.agent.context import AgentContext
from whendoes.ui_automation import (
    get_window_ui_context,
    click_element,
    type_text,
    get_element_value,
    invoke_pattern,
    select_item,
    toggle_element,
    expand_element,
)


class SmartUIAgent:
    """Agent that understands UI patterns without screenshots."""

    def __init__(
        self,
        llm_provider: BaseLLMProvider,
        tool_registry: ToolRegistry,
        max_iterations: int = 10,
        require_approval: bool = True,
        verbose: bool = False,
    ):
        """Initialize smart UI agent.

        Args:
            llm_provider: LLM provider instance
            tool_registry: Tool registry
            max_iterations: Maximum reasoning iterations
            require_approval: Require approval for destructive ops
            verbose: Verbose logging
        """
        self.llm = llm_provider
        self.tools = tool_registry
        self.max_iterations = max_iterations
        self.require_approval = require_approval
        self.verbose = verbose

    def interact_with_window(
        self, window_title: str, user_request: str, system_prompt: Optional[str] = None
    ) -> str:
        """Interact with a window based on user request.

        Args:
            window_title: Target window title
            user_request: What user wants to do
            system_prompt: Custom system prompt

        Returns:
            Result of interaction
        """
        # Step 1: Extract UI context (no screenshots!)
        ui_context = get_window_ui_context(window_title, max_depth=4)

        if "error" in ui_context:
            return f"Error: {ui_context}"

        # Step 2: Build context for LLM
        context = AgentContext(
            user_input=user_request,
            max_iterations=self.max_iterations,
            require_approval=self.require_approval,
            verbose=self.verbose,
        )

        # Add UI context as system knowledge
        context.add_message("system", f"Current UI Context:\n{ui_context}")
        context.add_message("user", user_request)

        # Step 3: Get system prompt with UI understanding
        if not system_prompt:
            system_prompt = self._get_ui_system_prompt()

        # Step 4: Reasoning loop
        while context.should_continue():
            context.increment_iteration()

            if self.verbose:
                print(f"\n[Iteration {context.iterations}]")

            # Get LLM response
            messages = [Message(role=msg["role"], content=msg["content"])
                       for msg in context.messages]

            response = self.llm.chat(
                messages=messages,
                tools=self.tools.get_tools_for_llm(),
                system=system_prompt,
            )

            if self.verbose:
                print(f"LLM Response: {response.content}")

            context.add_message("assistant", response.content)

            # Check if done
            if not response.tool_calls or response.stop_reason == "end_turn":
                return response.content

            # Execute tool calls
            for tool_call in response.tool_calls:
                if self.verbose:
                    print(f"Tool Call: {tool_call.name}({tool_call.arguments})")

                # Check approval
                tool = self.tools.get_tool(tool_call.name)
                if tool and tool.requires_approval and self.require_approval:
                    approval = self._request_approval(tool_call.name, tool_call.arguments)
                    if not approval:
                        context.add_message(
                            "tool",
                            f"Tool {tool_call.name} execution denied by user",
                        )
                        continue

                # Execute tool
                result = self.tools.execute_tool(tool_call.name, tool_call.arguments)
                context.add_tool_call(tool_call.name, tool_call.arguments, result)

                if self.verbose:
                    print(f"Tool Result: {result}")

                context.add_message("tool", f"{tool_call.name}: {str(result)}")

        return "Maximum iterations reached."

    def _get_ui_system_prompt(self) -> str:
        """Get system prompt for UI understanding.

        Returns:
            System prompt
        """
        return """أنت وكيل ذكي متخصص في التحكم بتطبيقات Windows عبر فهم بنية الواجهة الرسومية.

مهمتك:
1. تحليل سياق الواجهة (UI Context) المعطى لك
2. فهم العناصر المتاحة وأنواعها (Button, TextBox, MenuItem, etc)
3. تحديد الإجراء الأمثل بناءً على طلب المستخدم
4. استخدام الأدوات المناسبة لتنفيذ الإجراء

المبادئ الأساسية:
- ابحث عن العناصر بناءً على الاسم (name) أو نوع التحكم (type)
- استخدم الأنماط المدعومة (patterns): Invoke للأزرار، Value للحقول النصية
- تذكر أن كل تطبيقات Windows تستخدم نفس الأنماط القياسية
- لا تحتاج إلى صور - البيانات النصية كافية

عند التفاعل:
1. حدد العنصر المناسب من القائمة
2. اختر الإجراء المناسب (click, type, select, etc)
3. نفذ الإجراء باستخدام معرف العنصر (element_id)

مثال:
- إذا طلب المستخدم "افتح ملف جديد"، ابحث عن عنصر اسمه "File" أو "New"
- إذا طلب "اكتب نصاً"، ابحث عن TextBox وأرسل النص إليه
- إذا طلب "اختر عنصراً من قائمة"، استخدم select_item"""

    def _request_approval(self, tool_name: str, arguments: dict) -> bool:
        """Request user approval.

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


def setup_ui_tools() -> ToolRegistry:
    """Set up UI automation tools.

    Returns:
        Configured ToolRegistry
    """
    registry = ToolRegistry()

    # UI Interaction tools
    registry.register(
        "click_element",
        "Click on a UI element by ID",
        click_element,
        {
            "type": "object",
            "properties": {
                "window_title": {"type": "string", "description": "Window title"},
                "element_id": {"type": "string", "description": "Element ID (e.g., elem_5)"},
            },
            "required": ["window_title", "element_id"],
        },
    )

    registry.register(
        "type_text",
        "Type text into a text field",
        type_text,
        {
            "type": "object",
            "properties": {
                "window_title": {"type": "string", "description": "Window title"},
                "element_id": {"type": "string", "description": "Element ID"},
                "text": {"type": "string", "description": "Text to type"},
            },
            "required": ["window_title", "element_id", "text"],
        },
    )

    registry.register(
        "get_element_value",
        "Get value from a UI element",
        get_element_value,
        {
            "type": "object",
            "properties": {
                "window_title": {"type": "string", "description": "Window title"},
                "element_id": {"type": "string", "description": "Element ID"},
            },
            "required": ["window_title", "element_id"],
        },
    )

    registry.register(
        "invoke_pattern",
        "Invoke pattern on an element (for buttons)",
        invoke_pattern,
        {
            "type": "object",
            "properties": {
                "window_title": {"type": "string", "description": "Window title"},
                "element_id": {"type": "string", "description": "Element ID"},
            },
            "required": ["window_title", "element_id"],
        },
    )

    registry.register(
        "select_item",
        "Select an item from a list or combobox",
        select_item,
        {
            "type": "object",
            "properties": {
                "window_title": {"type": "string", "description": "Window title"},
                "element_id": {"type": "string", "description": "Element ID"},
            },
            "required": ["window_title", "element_id"],
        },
    )

    registry.register(
        "toggle_element",
        "Toggle a checkbox or similar element",
        toggle_element,
        {
            "type": "object",
            "properties": {
                "window_title": {"type": "string", "description": "Window title"},
                "element_id": {"type": "string", "description": "Element ID"},
            },
            "required": ["window_title", "element_id"],
        },
    )

    registry.register(
        "expand_element",
        "Expand a tree item or group",
        expand_element,
        {
            "type": "object",
            "properties": {
                "window_title": {"type": "string", "description": "Window title"},
                "element_id": {"type": "string", "description": "Element ID"},
            },
            "required": ["window_title", "element_id"],
        },
    )

    return registry
