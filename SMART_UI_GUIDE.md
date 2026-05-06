# Smart UI Agent - Advanced Browser Automation

## Overview

The Smart UI Agent is an advanced system that understands browser content **without screenshots** by reading the Windows UI Automation Accessibility Tree. This enables true AI understanding of web page structure and content.

## How It Works

### 1. Accessibility Tree Extraction

Instead of sending screenshots to the LLM, we extract the **Accessibility Tree** from the browser:

```
Window: Google Chrome - [Tab: Facebook]
└── Document: Facebook News Feed
    ├── Button: [elem_102] Name: "Like"
    ├── EditBox: [elem_105] Name: "What's on your mind?"
    └── Link: [elem_110] Name: "Profile Account"
```

### 2. Smart Prompt Engineering

The LLM receives a structured prompt that teaches it to:
- Analyze available UI elements
- Identify the correct element for the user's goal
- Return precise element IDs and actions

### 3. Direct Action Execution

Instead of guessing mouse coordinates, we execute actions directly on elements:

```python
CLICK(elem_102)      # Click the "Like" button
TYPE(elem_105, "Hello")  # Type in the text box
SELECT(elem_110, "Profile")  # Select from dropdown
```

## Architecture

### Components

1. **UIAutomationExtractor** - Reads Accessibility Tree from applications
2. **UIElement** - Represents a single UI element with metadata
3. **UIAutomationExecutor** - Executes actions on UI elements
4. **SmartUIAgent** - Orchestrates UI understanding and action

### File Structure

```
src/whendoes/
├── windows_api/
│   └── ui_automation.py          # UI Automation classes
├── agent/
│   └── smart_ui_agent_new.py     # Smart UI Agent
└── cli/
    └── repl.py                   # Integration with CLI

examples/
└── smart_ui_agent_demo.py        # Usage examples
```

## Usage

### Basic Usage

```python
from whendoes.llm import create_provider
from whendoes.agent.smart_ui_agent_new import SmartUIAgent

# Create LLM provider
llm = create_provider("anthropic", api_key="your_key")

# Create Smart UI Agent
agent = SmartUIAgent(llm, app_name="chrome")

# Read UI tree
ui_tree = agent.read_ui_tree()
print(ui_tree)

# Understand UI and get action
response = agent.understand_ui("Find the search box and search for Python")
print(response)
```

### Finding Elements

```python
# Find element by name
element = agent.extractor.find_element_by_name("Search", agent.current_tree)

# Find all buttons
buttons = agent.find_elements_by_role("button")
for btn in buttons:
    print(f"[{btn.id}] {btn.name}")
```

### Executing Actions

```python
# Click element
agent.extractor.find_and_click("Search Button")

# Type text
executor = UIAutomationExecutor("chrome")
executor.type_text("elem_105", "Python programming")

# Get element value
value = executor.get_element_value("elem_105")
```

## System Prompt

The Smart UI Agent uses an intelligent system prompt that guides the LLM:

```
أنت خبير في نظام Windows UI Automation. سيتم إعطاؤك تمثيلاً نصياً لـ Accessibility Tree.

مهمتك:
1. تحليل العناصر المتاحة (Buttons, Links, Inputs, etc.)
2. تحديد العنصر الذي يحقق هدف المستخدم بناءً على اسمه (Name) أو دوره (Role)
3. الرد بالأمر المناسب فقط

القواعد:
- لا تحاول الضغط على عناصر غير مرئية (hidden)
- إذا كان هناك عدة تبويبات، ابحث عن عنصر النوع 'tab' أولاً
- استخدم element IDs من الشجرة مباشرة
- كن دقيقاً في اختيار العنصر الصحيح
```

## Advantages Over Screenshots

| Aspect | Screenshots | Accessibility Tree |
|--------|------------|-------------------|
| **Size** | 100+ KB per image | 1-5 KB text |
| **Speed** | Slow (image processing) | Fast (text processing) |
| **Accuracy** | Guesses coordinates | Direct element IDs |
| **Hidden Content** | Can't see alt-text | Sees all metadata |
| **Reliability** | Breaks with UI changes | Robust to styling |
| **Cost** | Higher token usage | Lower token usage |

## Supported Applications

- **Chrome** - Full support via UIA
- **Edge** - Full support via UIA
- **Firefox** - Full support via UIA
- **Any UIA-compatible app** - Window management, dialogs, etc.

## Element Roles

The system recognizes these element roles:

- `button` - Clickable buttons
- `textbox` - Text input fields
- `combobox` - Dropdown menus
- `listbox` - List boxes
- `checkbox` - Checkboxes
- `radio` - Radio buttons
- `link` - Hyperlinks
- `tab` - Tab items
- `menu` - Menu items
- `document` - Document/page content

## Example: Search on Google

```python
agent = SmartUIAgent(llm, app_name="chrome")

# Read current UI
ui_tree = agent.read_ui_tree()
# Output:
# Window: Google Chrome
# └── Document: Google Search
#     ├── EditBox: [elem_5] Name: "Search"
#     └── Button: [elem_10] Name: "Google Search"

# Ask LLM to search
response = agent.understand_ui("Search for 'Python programming'")
# Output: CLICK(elem_5) then TYPE(elem_5, "Python programming") then CLICK(elem_10)

# Execute actions
executor = UIAutomationExecutor("chrome")
executor.click_element("elem_5")
executor.type_text("elem_5", "Python programming")
executor.click_element("elem_10")
```

## Advanced Features

### Tree Depth Control

```python
# Shallow tree (faster, less detail)
ui_tree = agent.read_ui_tree(max_depth=4)

# Deep tree (slower, more detail)
ui_tree = agent.read_ui_tree(max_depth=10)
```

### Element Filtering

```python
# Find all interactive elements
buttons = agent.find_elements_by_role("button")
inputs = agent.find_elements_by_role("textbox")
links = agent.find_elements_by_role("link")
```

### Custom Prompts

```python
# Override system prompt for specific tasks
custom_prompt = "You are a form-filling expert..."
response = agent.llm.chat(
    messages=[Message(role="user", content=ui_tree)],
    system=custom_prompt
)
```

## Limitations

1. **Requires UIA Support** - Application must expose UI via Windows UI Automation
2. **No Visual Context** - Can't see colors, fonts, or visual layout
3. **Dynamic Content** - Must re-read tree after page changes
4. **Complex Interactions** - Some interactions may require multiple steps

## Troubleshooting

### "Failed to connect to chrome"
- Make sure Chrome is running
- Check that the window title contains "Chrome"

### "Failed to read UI tree"
- Ensure the application is responsive
- Try reducing max_depth
- Check that UIA is enabled in the application

### Element not found
- Verify element name is correct
- Try searching by role instead of name
- Increase max_depth to find nested elements

## Performance Tips

1. **Use appropriate max_depth** - Balance between detail and speed
2. **Cache UI trees** - Don't re-read if content hasn't changed
3. **Filter by role** - Use find_elements_by_role for faster searches
4. **Batch operations** - Group multiple actions together

## Future Enhancements

- [ ] Multi-window support
- [ ] Cross-application automation
- [ ] Pattern learning and generalization
- [ ] Keyboard navigation support
- [ ] Accessibility tree caching
- [ ] Performance optimization
- [ ] Custom element matchers
- [ ] Action recording and playback

## Integration with Main Agent

The Smart UI Agent can be integrated with the main Whendoes Agent:

```python
# In agent system prompt
"When interacting with web browsers, use the Smart UI Agent to:
1. Read the Accessibility Tree
2. Understand the page structure
3. Execute precise actions on elements"
```

This enables the main agent to handle both system-level operations and browser automation seamlessly.
