"""Advanced: Building custom learning models for specific applications."""

from whendoes.llm import create_provider
from whendoes.agent.smart_ui_agent import SmartUIAgent, setup_ui_tools
from whendoes.ui_automation import get_window_ui_context
import json


class ApplicationSpecificLearner:
    """Learn patterns specific to an application."""

    def __init__(self, app_name: str, llm_provider):
        """Initialize learner for specific app.

        Args:
            app_name: Application name (e.g., "Excel", "Word")
            llm_provider: LLM provider instance
        """
        self.app_name = app_name
        self.llm = llm_provider
        self.learned_patterns = {}
        self.ui_cache = {}

    def learn_pattern(self, task_description: str, steps: list[str]) -> None:
        """Learn a pattern for this application.

        Args:
            task_description: What the pattern does
            steps: List of steps to perform
        """
        self.learned_patterns[task_description] = {
            "app": self.app_name,
            "steps": steps,
            "learned_at": "now",
        }

    def get_ui_structure(self) -> dict:
        """Get cached UI structure."""
        if self.app_name not in self.ui_cache:
            context = get_window_ui_context(self.app_name, max_depth=4)
            self.ui_cache[self.app_name] = json.loads(context)
        return self.ui_cache[self.app_name]

    def build_custom_system_prompt(self) -> str:
        """Build custom system prompt for this app.

        Returns:
            Custom system prompt
        """
        ui_structure = self.get_ui_structure()

        prompt = f"""أنت متخصص في التحكم بتطبيق {self.app_name}.

معلومات عن التطبيق:
- الاسم: {self.app_name}
- العناصر الرئيسية: {', '.join([e['name'] for e in ui_structure.get('elements', [])[:5]])}

الأنماط المتعلمة:
"""

        for pattern_name, pattern_info in self.learned_patterns.items():
            prompt += f"\n- {pattern_name}: {' → '.join(pattern_info['steps'])}"

        prompt += """

عند التعامل مع طلب جديد:
1. تحقق من الأنماط المتعلمة
2. طبق النمط الأقرب
3. تعلم من النتيجة
4. حسّن الأداء للمرات القادمة
"""

        return prompt


# مثال: تعلم أنماط Excel
print("=" * 60)
print("ADVANCED: Application-Specific Learning")
print("=" * 60)

# إنشاء متعلم مخصص لـ Excel
excel_learner = ApplicationSpecificLearner(
    "Excel",
    create_provider("groq", api_key="your-key"),
)

# تعلم أنماط Excel
excel_learner.learn_pattern(
    "Create new spreadsheet",
    ["File → New", "Select Blank Workbook", "Click Create"],
)

excel_learner.learn_pattern(
    "Add data to cells",
    ["Click cell", "Type data", "Press Enter"],
)

excel_learner.learn_pattern(
    "Create formula",
    ["Click cell", "Type =", "Enter formula", "Press Enter"],
)

excel_learner.learn_pattern(
    "Format cells",
    ["Select cells", "Right-click", "Format Cells", "Choose format"],
)

# طباعة الأنماط المتعلمة
print("\n[Learned Patterns for Excel]")
print("-" * 60)
for pattern_name, pattern_info in excel_learner.learned_patterns.items():
    print(f"\n{pattern_name}:")
    for i, step in enumerate(pattern_info["steps"], 1):
        print(f"  {i}. {step}")

# بناء نموذج مخصص
print("\n\n[Custom System Prompt]")
print("-" * 60)
custom_prompt = excel_learner.build_custom_system_prompt()
print(custom_prompt)

# مثال: تعلم أنماط Word
print("\n\n" + "=" * 60)
print("Learning Patterns for Word")
print("=" * 60)

word_learner = ApplicationSpecificLearner(
    "Word",
    create_provider("groq", api_key="your-key"),
)

word_learner.learn_pattern(
    "Create document with title",
    ["File → New", "Type title", "Press Enter", "Start typing content"],
)

word_learner.learn_pattern(
    "Format text",
    ["Select text", "Use toolbar buttons", "Or use Format menu"],
)

word_learner.learn_pattern(
    "Insert table",
    ["Insert menu", "Table", "Choose dimensions", "Click OK"],
)

word_learner.learn_pattern(
    "Save document",
    ["File → Save", "Choose location", "Enter filename", "Click Save"],
)

print("\n[Learned Patterns for Word]")
print("-" * 60)
for pattern_name, pattern_info in word_learner.learned_patterns.items():
    print(f"\n{pattern_name}:")
    for i, step in enumerate(pattern_info["steps"], 1):
        print(f"  {i}. {step}")


# مثال: استخدام المتعلم المخصص مع الوكيل
print("\n\n" + "=" * 60)
print("Using Custom Learner with Agent")
print("=" * 60)

# إنشاء وكيل مع نموذج مخصص
llm = create_provider("groq", api_key="your-key")
tools = setup_ui_tools()
agent = SmartUIAgent(llm, tools)

# استخدام النموذج المخصص
print("\nInteracting with Excel using learned patterns...")
print("-" * 60)

# الموديل الآن يستخدم الأنماط المتعلمة
result = agent.interact_with_window(
    "Excel",
    "أنشئ جدول بيانات جديد وأضف البيانات",
)

print(f"Result: {result}")

# مثال: تحسين الأداء عبر التعلم المتكرر
print("\n\n" + "=" * 60)
print("Continuous Learning and Improvement")
print("=" * 60)

class ContinuousLearner:
    """Learn and improve over multiple interactions."""

    def __init__(self, app_name: str, llm_provider):
        self.app_name = app_name
        self.llm = llm_provider
        self.interaction_history = []
        self.success_rate = 0.0
        self.learned_patterns = {}

    def record_interaction(self, task: str, success: bool, steps_taken: list[str]):
        """Record an interaction for learning.

        Args:
            task: Task description
            success: Whether task succeeded
            steps_taken: Steps that were taken
        """
        self.interaction_history.append(
            {
                "task": task,
                "success": success,
                "steps": steps_taken,
            }
        )

        # Update success rate
        successful = sum(1 for i in self.interaction_history if i["success"])
        self.success_rate = successful / len(self.interaction_history)

        # Learn from successful interactions
        if success:
            self.learned_patterns[task] = steps_taken

    def get_learning_summary(self) -> dict:
        """Get summary of learning progress.

        Returns:
            Dictionary with learning stats
        """
        return {
            "app": self.app_name,
            "total_interactions": len(self.interaction_history),
            "success_rate": f"{self.success_rate * 100:.1f}%",
            "patterns_learned": len(self.learned_patterns),
            "learned_tasks": list(self.learned_patterns.keys()),
        }


# مثال على التعلم المستمر
continuous_learner = ContinuousLearner(
    "Excel",
    create_provider("groq", api_key="your-key"),
)

# محاكاة تفاعلات متعددة
interactions = [
    ("Create spreadsheet", True, ["File → New", "Select Blank", "Create"]),
    ("Add data", True, ["Click cell", "Type data", "Enter"]),
    ("Format cells", True, ["Select", "Format", "Apply"]),
    ("Create formula", False, ["Click cell", "Type formula"]),  # فشل
    ("Create formula", True, ["Click cell", "Type =", "Formula", "Enter"]),  # نجح
]

for task, success, steps in interactions:
    continuous_learner.record_interaction(task, success, steps)

print("\n[Learning Progress]")
print("-" * 60)
summary = continuous_learner.get_learning_summary()
for key, value in summary.items():
    print(f"{key}: {value}")

print("\n[Learned Patterns]")
print("-" * 60)
for task, steps in continuous_learner.learned_patterns.items():
    print(f"\n{task}:")
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step}")

print("\n" + "=" * 60)
print("✓ Continuous learning system ready!")
print("=" * 60)
