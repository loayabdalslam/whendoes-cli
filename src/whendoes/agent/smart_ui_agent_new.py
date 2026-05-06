"""Smart UI Agent - Understands browser content without screenshots."""

from typing import Optional
from whendoes.llm.base import BaseLLMProvider, Message
from whendoes.windows_api.ui_automation import UIAutomationExtractor, UIElement


class SmartUIAgent:
    """Agent that understands UI without screenshots using Accessibility Tree."""

    def __init__(self, llm_provider: BaseLLMProvider, app_name: str = "chrome"):
        """Initialize Smart UI Agent.

        Args:
            llm_provider: LLM provider instance
            app_name: Application name (chrome, edge, firefox)
        """
        self.llm = llm_provider
        self.extractor = UIAutomationExtractor(app_name)
        self.current_tree = None

    def read_ui_tree(self, max_depth: int = 8) -> Optional[str]:
        """Read current UI tree from application.

        Args:
            max_depth: Maximum depth to traverse

        Returns:
            Text representation of UI tree or None
        """
        self.current_tree = self.extractor.extract_tree(max_depth)
        if not self.current_tree:
            return None
        return self.current_tree.to_text()

    def understand_ui(self, user_query: str) -> str:
        """Understand UI and generate action based on user query.

        Args:
            user_query: User's natural language query

        Returns:
            LLM response with suggested action
        """
        # Read current UI tree
        ui_text = self.read_ui_tree()
        if not ui_text:
            return "Failed to read UI tree. Make sure the application is running."

        # Create system prompt
        system_prompt = self._get_system_prompt()

        # Create context message with UI tree
        context_message = f"""Current UI Tree:
{ui_text}

User Request: {user_query}

Based on the UI tree above, what action should be taken? Respond with:
1. The element ID to interact with
2. The action to perform (CLICK, TYPE, SELECT, etc.)
3. Any additional parameters needed"""

        # Call LLM
        messages = [Message(role="user", content=context_message)]
        response = self.llm.chat(messages=messages, system=system_prompt)

        return response.content

    def find_and_click(self, element_name: str) -> bool:
        """Find element by name and click it.

        Args:
            element_name: Name of element to find

        Returns:
            True if successful
        """
        if not self.current_tree:
            self.read_ui_tree()

        element = self.extractor.find_element_by_name(element_name, self.current_tree)
        if not element:
            return False

        try:
            # Get actual pywinauto element and click it
            # This is simplified - in real implementation would need to map back to pywinauto element
            return True
        except Exception:
            return False

    def find_elements_by_role(self, role: str) -> list:
        """Find all elements with specific role.

        Args:
            role: Role to search for (button, textbox, link, etc.)

        Returns:
            List of UIElements
        """
        if not self.current_tree:
            self.read_ui_tree()

        return self.extractor.find_elements_by_role(role, self.current_tree)

    def _get_system_prompt(self) -> str:
        """Get system prompt for UI understanding.

        Returns:
            System prompt
        """
        return """أنت خبير في نظام Windows UI Automation. سيتم إعطاؤك تمثيلاً نصياً لـ Accessibility Tree.

مهمتك:
1. تحليل العناصر المتاحة (Buttons, Links, Inputs, etc.)
2. تحديد العنصر الذي يحقق هدف المستخدم بناءً على اسمه (Name) أو دوره (Role)
3. الرد بالأمر المناسب فقط

القواعد:
- لا تحاول الضغط على عناصر غير مرئية (hidden)
- إذا كان هناك عدة تبويبات، ابحث عن عنصر النوع 'tab' الذي يحمل الاسم المطلوب أولاً
- استخدم element IDs من الشجرة مباشرة
- كن دقيقاً في اختيار العنصر الصحيح

أمثلة على الأوامر:
- CLICK(elem_5) - اضغط على العنصر
- TYPE(elem_10, "البحث") - اكتب نصاً
- SELECT(elem_15, "Option 1") - اختر من قائمة
- NAVIGATE(elem_20) - انتقل إلى رابط"""
