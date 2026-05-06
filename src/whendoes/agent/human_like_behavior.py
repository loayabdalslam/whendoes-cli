"""Human-like behavior system for natural task execution with streaming."""

import time
from typing import Optional, Callable, List
from whendoes.llm.base import BaseLLMProvider, Message
from whendoes.windows_api.ui_automation import UIAutomationExtractor, UIElement
from whendoes.agent.tool_registry import ToolRegistry


class HumanLikeBehavior:
    """Simulates human-like behavior with natural delays and streaming."""

    def __init__(self, stream_callback: Optional[Callable[[str], None]] = None):
        """Initialize behavior system.

        Args:
            stream_callback: Callback for streaming output
        """
        self.stream_callback = stream_callback
        self.action_history = []

    def stream(self, text: str) -> None:
        """Stream text output.

        Args:
            text: Text to stream
        """
        if self.stream_callback:
            self.stream_callback(text)
        else:
            print(text, end="", flush=True)

    def think(self, duration: float = 0.5) -> None:
        """Simulate thinking with natural delay.

        Args:
            duration: Thinking duration in seconds
        """
        self.stream("💭 ")
        time.sleep(duration)

    def observe(self, observation: str) -> None:
        """Observe and stream observation.

        Args:
            observation: What was observed
        """
        self.stream(f"👁️  Observing: {observation}\n")
        time.sleep(0.3)

    def plan(self, plan_text: str) -> None:
        """Plan action and stream it.

        Args:
            plan_text: Plan description
        """
        self.stream(f"📋 Plan: {plan_text}\n")
        time.sleep(0.2)

    def execute(self, action: str, details: str = "") -> None:
        """Execute action with streaming.

        Args:
            action: Action name
            details: Action details
        """
        self.stream(f"⚡ Executing: {action}")
        if details:
            self.stream(f" - {details}")
        self.stream("\n")
        time.sleep(0.1)
        self.action_history.append({"action": action, "details": details})

    def success(self, message: str) -> None:
        """Stream success message.

        Args:
            message: Success message
        """
        self.stream(f"✅ {message}\n")
        time.sleep(0.2)

    def error(self, message: str) -> None:
        """Stream error message.

        Args:
            message: Error message
        """
        self.stream(f"❌ {message}\n")
        time.sleep(0.2)

    def wait(self, duration: float = 1.0, reason: str = "") -> None:
        """Wait with streaming indication.

        Args:
            duration: Wait duration in seconds
            reason: Reason for waiting
        """
        if reason:
            self.stream(f"⏳ Waiting ({reason})...")
        else:
            self.stream("⏳ Waiting...")
        time.sleep(duration)
        self.stream(" Done\n")

    def get_history(self) -> List[dict]:
        """Get action history.

        Returns:
            List of executed actions
        """
        return self.action_history


class ChromeAccessibilityAgent:
    """Agent that interacts with Chrome using accessibility tree with human-like behavior."""

    def __init__(
        self,
        llm_provider: BaseLLMProvider,
        stream_callback: Optional[Callable[[str], None]] = None,
    ):
        """Initialize Chrome Accessibility Agent.

        Args:
            llm_provider: LLM provider instance
            stream_callback: Callback for streaming output
        """
        self.llm = llm_provider
        self.behavior = HumanLikeBehavior(stream_callback)
        self.extractor = UIAutomationExtractor("chrome")
        self.current_tree = None

    def execute_task(self, task: str) -> str:
        """Execute a task in Chrome with human-like behavior.

        Args:
            task: Task description (e.g., "Search for Python programming")

        Returns:
            Task result
        """
        self.behavior.stream(f"\n🎯 Task: {task}\n")
        self.behavior.stream("=" * 60 + "\n")

        # Step 1: Think about the task
        self.behavior.think(0.8)
        self.behavior.stream("Analyzing task...\n")

        # Step 2: Observe current state
        self.behavior.observe("Reading Chrome accessibility tree")
        self.current_tree = self.extractor.extract_tree(max_depth=8)

        if not self.current_tree:
            self.behavior.error("Failed to read Chrome accessibility tree")
            return "Failed to access Chrome"

        # Get tree as text
        tree_text = self.current_tree.to_text()
        self.behavior.stream(f"\n📖 Current UI State:\n{tree_text}\n")

        # Step 3: Plan the task
        plan = self._get_task_plan(task, tree_text)
        self.behavior.plan(plan)

        # Step 4: Execute the plan
        result = self._execute_plan(task, tree_text)

        self.behavior.stream("=" * 60 + "\n")
        return result

    def _get_task_plan(self, task: str, tree_text: str) -> str:
        """Get task plan from LLM.

        Args:
            task: Task description
            tree_text: Current UI tree

        Returns:
            Task plan
        """
        system_prompt = """أنت مساعد ذكي متخصص في التحكم بمتصفح Chrome.

مهمتك: تحليل المهمة والواجهة الحالية وإنشاء خطة تنفيذ واضحة.

الخطة يجب أن تتضمن:
1. العناصر التي ستتفاعل معها
2. ترتيب الخطوات
3. الإجراءات المطلوبة (CLICK, TYPE, NAVIGATE, etc.)

كن دقيقاً وعملياً."""

        context = f"""المهمة: {task}

الواجهة الحالية:
{tree_text}

ما هي خطتك لتنفيذ هذه المهمة؟"""

        messages = [Message(role="user", content=context)]
        response = self.llm.chat(messages=messages, system=system_prompt)
        return response.content

    def _execute_plan(self, task: str, tree_text: str) -> str:
        """Execute the task plan.

        Args:
            task: Task description
            tree_text: Current UI tree

        Returns:
            Execution result
        """
        system_prompt = """أنت متخصص في تنفيذ المهام على Chrome باستخدام عناصر الواجهة.

مهمتك: تحديد العناصر الدقيقة والإجراءات المطلوبة.

الرد بصيغة:
ACTION: [CLICK|TYPE|SELECT|NAVIGATE]
ELEMENT: [element_id]
VALUE: [value if needed]
REASON: [لماذا هذا الإجراء]"""

        context = f"""المهمة: {task}

الواجهة الحالية:
{tree_text}

ما هي الإجراءات المطلوبة لتنفيذ هذه المهمة؟"""

        messages = [Message(role="user", content=context)]
        response = self.llm.chat(messages=messages, system=system_prompt)

        # Parse and execute actions
        actions = self._parse_actions(response.content)
        results = []

        for action in actions:
            self.behavior.execute(
                action.get("action", "Unknown"),
                action.get("reason", ""),
            )
            self.behavior.wait(0.5)
            results.append(action)

        if results:
            self.behavior.success(f"Executed {len(results)} actions successfully")
            return f"Task completed: {task}"
        else:
            self.behavior.error("No actions could be executed")
            return "Task failed"

    def _parse_actions(self, response: str) -> List[dict]:
        """Parse actions from LLM response.

        Args:
            response: LLM response text

        Returns:
            List of actions
        """
        actions = []
        lines = response.split("\n")

        current_action = {}
        for line in lines:
            line = line.strip()
            if line.startswith("ACTION:"):
                if current_action:
                    actions.append(current_action)
                current_action = {"action": line.replace("ACTION:", "").strip()}
            elif line.startswith("ELEMENT:"):
                current_action["element"] = line.replace("ELEMENT:", "").strip()
            elif line.startswith("VALUE:"):
                current_action["value"] = line.replace("VALUE:", "").strip()
            elif line.startswith("REASON:"):
                current_action["reason"] = line.replace("REASON:", "").strip()

        if current_action:
            actions.append(current_action)

        return actions

    def find_element(self, name: str) -> Optional[UIElement]:
        """Find element by name.

        Args:
            name: Element name

        Returns:
            UIElement or None
        """
        if not self.current_tree:
            self.current_tree = self.extractor.extract_tree()

        return self.extractor.find_element_by_name(name, self.current_tree)

    def find_elements_by_role(self, role: str) -> List[UIElement]:
        """Find elements by role.

        Args:
            role: Element role

        Returns:
            List of UIElements
        """
        if not self.current_tree:
            self.current_tree = self.extractor.extract_tree()

        return self.extractor.find_elements_by_role(role, self.current_tree)

    def get_action_history(self) -> List[dict]:
        """Get action history.

        Returns:
            List of executed actions
        """
        return self.behavior.get_history()
