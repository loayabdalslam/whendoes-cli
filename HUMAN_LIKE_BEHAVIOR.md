# Human-Like Chrome Automation - Complete Guide

## Overview

The Human-Like Behavior system enables the agent to interact with Chrome in a natural, human-like manner with:
- Natural thinking delays
- Streaming observations and actions
- Accessibility tree understanding
- Intelligent task planning and execution
- Real-time feedback

## Architecture

### Components

1. **HumanLikeBehavior** - Simulates human behavior with natural delays
   - `think()` - Thinking with delays
   - `observe()` - Observing UI state
   - `plan()` - Planning actions
   - `execute()` - Executing actions
   - `success()` - Success feedback
   - `error()` - Error handling
   - `wait()` - Natural waiting

2. **ChromeAccessibilityAgent** - Orchestrates Chrome automation
   - Reads accessibility tree
   - Plans tasks using LLM
   - Executes actions with human-like behavior
   - Tracks action history

3. **Integration with Main Agent** - Seamless integration
   - Optional human-like mode
   - Streaming callbacks
   - Natural delays between actions

## How It Works

### Traditional Approach
```
User Query
    ↓
Agent thinks (instant)
    ↓
Agent executes (instant)
    ↓
Result
```

### Human-Like Approach
```
User Query
    ↓
💭 Agent thinks (0.5s delay)
    ↓
👁️  Agent observes UI (0.3s delay)
    ↓
📋 Agent plans (0.2s delay)
    ↓
⚡ Agent executes (0.1s delay per action)
    ↓
✅ Success feedback (0.2s delay)
    ↓
Result with action history
```

## Usage

### Basic Usage

```python
from whendoes.llm import create_provider
from whendoes.agent.human_like_behavior import ChromeAccessibilityAgent

# Create LLM provider
llm = create_provider("anthropic", api_key="your_key")

# Create agent with streaming
def stream_callback(text):
    print(text, end="", flush=True)

agent = ChromeAccessibilityAgent(llm, stream_callback=stream_callback)

# Execute task
result = agent.execute_task("Search for Python programming")
```

### Output Example

```
🎯 Task: Search for Python programming
============================================================

💭 Analyzing task...
👁️  Observing: Reading Chrome accessibility tree

📖 Current UI State:
[elem_1] window: Google Chrome
└── [elem_5] document: Google Search
    ├── [elem_10] textbox: Search
    └── [elem_15] button: Google Search

📋 Plan: 1. Click on search box (elem_10)
2. Type "Python programming"
3. Click search button (elem_15)

⚡ Executing: CLICK - Click on search box
⏳ Waiting (action delay)... Done
✅ Action executed successfully

⚡ Executing: TYPE - Type search query
⏳ Waiting (action delay)... Done
✅ Action executed successfully

⚡ Executing: CLICK - Click search button
⏳ Waiting (action delay)... Done
✅ Action executed successfully

============================================================
✅ Task completed: Search for Python programming
```

### Interactive Mode

```python
# Interactive task execution
while True:
    task = input("Task: ")
    if task.lower() == "exit":
        break
    
    result = agent.execute_task(task)
    print(f"\n✅ {result}\n")
```

## Behavior Customization

### Thinking Duration

```python
behavior = HumanLikeBehavior()
behavior.think(1.0)  # 1 second thinking
behavior.think(0.3)  # 0.3 second thinking
```

### Observation

```python
behavior.observe("Checking page title")
behavior.observe("Looking for search box")
```

### Planning

```python
behavior.plan("Click search box → Type query → Click search")
behavior.plan("Find element → Verify visibility → Execute action")
```

### Execution

```python
behavior.execute("CLICK", "Search button (elem_15)")
behavior.execute("TYPE", "Python programming")
behavior.execute("NAVIGATE", "First search result")
```

### Waiting

```python
behavior.wait(1.0, "page to load")
behavior.wait(0.5, "animation to complete")
behavior.wait(2.0)  # Generic wait
```

## Integration with Main Agent

### Enable Human-Like Mode

```python
from whendoes.agent.agent import Agent

agent = Agent(
    llm_provider=llm,
    tool_registry=tools,
    stream_callback=stream_callback,
    human_like=True,  # Enable human-like behavior
)
```

### CLI Usage

```bash
whendoes
```

The CLI automatically enables human-like mode with streaming output.

### Example Commands

```
You: open chrome and search for python
💭 Analyzing task...
👁️  Observing: Reading Chrome accessibility tree
📋 Plan: Open Chrome → Search for Python
⚡ Executing: launch_app - Open Chrome
✅ Chrome opened successfully
⚡ Executing: find_app_path - Find Chrome path
✅ Chrome path found
Assistant: ✓ Chrome opened and ready for search

You: find the first search result and click it
💭 Analyzing task...
👁️  Observing: Reading Chrome accessibility tree
📋 Plan: Find first result → Click it
⚡ Executing: CLICK - First search result
✅ Action executed successfully
Assistant: ✓ First search result clicked
```

## Action History

Track all executed actions:

```python
agent = ChromeAccessibilityAgent(llm, stream_callback=stream_callback)
agent.execute_task("Search for Python")

# Get history
history = agent.get_action_history()
for i, action in enumerate(history, 1):
    print(f"{i}. {action['action']}: {action['details']}")

# Output:
# 1. CLICK: Click on search box
# 2. TYPE: Type search query
# 3. CLICK: Click search button
```

## Element Finding

### Find by Name

```python
element = agent.find_element("Search")
if element:
    print(f"Found: {element.name} (ID: {element.id})")
```

### Find by Role

```python
buttons = agent.find_elements_by_role("button")
for btn in buttons:
    print(f"Button: {btn.name} (ID: {btn.id})")
```

## System Prompts

### Task Planning Prompt

```
أنت مساعد ذكي متخصص في التحكم بمتصفح Chrome.

مهمتك: تحليل المهمة والواجهة الحالية وإنشاء خطة تنفيذ واضحة.

الخطة يجب أن تتضمن:
1. العناصر التي ستتفاعل معها
2. ترتيب الخطوات
3. الإجراءات المطلوبة (CLICK, TYPE, NAVIGATE, etc.)

كن دقيقاً وعملياً.
```

### Action Execution Prompt

```
أنت متخصص في تنفيذ المهام على Chrome باستخدام عناصر الواجهة.

مهمتك: تحديد العناصر الدقيقة والإجراءات المطلوبة.

الرد بصيغة:
ACTION: [CLICK|TYPE|SELECT|NAVIGATE]
ELEMENT: [element_id]
VALUE: [value if needed]
REASON: [لماذا هذا الإجراء]
```

## Performance Tips

1. **Adjust Delays** - Customize thinking/waiting durations
2. **Cache Trees** - Don't re-read if content hasn't changed
3. **Batch Actions** - Group related actions together
4. **Use Roles** - Find elements by role for faster searches
5. **Limit Depth** - Use appropriate max_depth for tree extraction

## Supported Actions

- `CLICK` - Click on element
- `TYPE` - Type text into element
- `SELECT` - Select from dropdown
- `NAVIGATE` - Navigate to link
- `SCROLL` - Scroll page
- `WAIT` - Wait for element
- `OBSERVE` - Observe current state

## Error Handling

```python
try:
    result = agent.execute_task("Search for Python")
except Exception as e:
    print(f"Error: {e}")
    # Check action history for debugging
    history = agent.get_action_history()
```

## Debugging

### Enable Verbose Output

```python
agent = ChromeAccessibilityAgent(llm, stream_callback=stream_callback)
# All actions are streamed automatically
```

### Check Action History

```python
history = agent.get_action_history()
print(f"Total actions: {len(history)}")
for action in history:
    print(f"  - {action['action']}: {action['details']}")
```

### Inspect Current UI Tree

```python
tree_text = agent.current_tree.to_text()
print(tree_text)
```

## Advanced Features

### Custom Behavior

```python
from whendoes.agent.human_like_behavior import HumanLikeBehavior

behavior = HumanLikeBehavior(stream_callback)
behavior.think(2.0)  # Long thinking
behavior.observe("Analyzing page structure")
behavior.plan("Complex multi-step task")
behavior.execute("ACTION", "Details")
behavior.success("Task completed!")
```

### Multi-Task Execution

```python
tasks = [
    "Search for Python programming",
    "Click first result",
    "Scroll down to see more",
    "Click on a related link",
]

for task in tasks:
    result = agent.execute_task(task)
    print(f"✅ {result}\n")
```

### Task Chaining

```python
# Execute related tasks in sequence
agent.execute_task("Open Google")
agent.execute_task("Search for Python")
agent.execute_task("Click first result")
agent.execute_task("Read the article")
```

## Limitations

1. **Requires Chrome** - Must have Chrome running
2. **UIA Support** - Requires Windows UI Automation support
3. **Dynamic Content** - Must re-read tree after page changes
4. **Complex Interactions** - Some interactions may need multiple steps

## Troubleshooting

### "Failed to read Chrome accessibility tree"
- Ensure Chrome is running
- Check that Chrome window is visible
- Try reducing max_depth

### Actions not executing
- Verify element IDs are correct
- Check that elements are visible and enabled
- Increase wait duration

### Slow execution
- Reduce thinking/waiting delays
- Use appropriate max_depth
- Cache UI trees when possible

## Future Enhancements

- [ ] Multi-window support
- [ ] Cross-application automation
- [ ] Pattern learning
- [ ] Keyboard navigation
- [ ] Screenshot fallback
- [ ] Performance optimization
- [ ] Custom action types
- [ ] Action recording/playback

## Examples

See `examples/human_like_chrome_automation.py` for complete working examples.

## Integration

The human-like behavior system is fully integrated with:
- Main Agent (with `human_like=True` flag)
- CLI REPL (enabled by default)
- Streaming callbacks
- Tool registry
- LLM providers

This creates a seamless, natural automation experience that feels like a human is controlling the browser!
