# Accessibility Tools - Complete Reference

## Overview

The Accessibility Tools provide comprehensive access to UI elements in applications (Chrome, Edge, Firefox, etc.) through the Windows UI Automation API. These tools enable the agent to:

- Read complete accessibility trees
- Find elements by name or role
- Get detailed element information
- Search for elements
- Analyze page structure
- List interactive elements
- Filter by visibility and enabled state

## Available Tools

### 1. read_accessibility_tree

Read the complete accessibility tree from an application.

**Parameters:**
- `app_name` (string, optional): Application name (default: "chrome")
- `max_depth` (integer, optional): Maximum depth to traverse (default: 8)

**Returns:** Text representation of the accessibility tree

**Example:**
```
You: read the accessibility tree from chrome
Agent: 
[elem_1] window: Google Chrome
└── [elem_5] document: Google Search
    ├── [elem_10] textbox: Search
    ├── [elem_15] button: Google Search
    └── [elem_20] link: Images
```

### 2. find_element_by_name

Find a specific element by name.

**Parameters:**
- `app_name` (string, required): Application name
- `element_name` (string, required): Element name to search for

**Returns:** Element information (id, name, role, control_type, enabled, visible, value)

**Example:**
```
You: find the search button in chrome
Agent: Found: {
  "id": "elem_15",
  "name": "Google Search",
  "role": "button",
  "control_type": "Button",
  "is_enabled": true,
  "is_visible": true
}
```

### 3. find_elements_by_role

Find all elements with a specific role.

**Parameters:**
- `app_name` (string, required): Application name
- `role` (string, required): Element role (button, link, textbox, tab, checkbox, etc.)

**Returns:** List of elements with the specified role

**Example:**
```
You: find all buttons in chrome
Agent: Found 5 buttons:
  - [elem_15] Google Search
  - [elem_25] I'm Feeling Lucky
  - [elem_30] Settings
  - [elem_35] Sign in
  - [elem_40] More
```

### 4. get_element_info

Get detailed information about a specific element.

**Parameters:**
- `app_name` (string, required): Application name
- `element_id` (string, required): Element ID

**Returns:** Detailed element information including children count

**Example:**
```
You: get info about element elem_15
Agent: {
  "id": "elem_15",
  "name": "Google Search",
  "role": "button",
  "control_type": "Button",
  "is_enabled": true,
  "is_visible": true,
  "value": null,
  "children_count": 0
}
```

### 5. list_all_buttons

List all buttons in an application.

**Parameters:**
- `app_name` (string, optional): Application name (default: "chrome")

**Returns:** List of all buttons

**Example:**
```
You: list all buttons in chrome
Agent: Found 5 buttons:
  - [elem_15] Google Search
  - [elem_25] I'm Feeling Lucky
  - [elem_30] Settings
  - [elem_35] Sign in
  - [elem_40] More
```

### 6. list_all_textboxes

List all textboxes in an application.

**Parameters:**
- `app_name` (string, optional): Application name (default: "chrome")

**Returns:** List of all textboxes

**Example:**
```
You: list all textboxes in chrome
Agent: Found 1 textbox:
  - [elem_10] Search
```

### 7. list_all_links

List all links in an application.

**Parameters:**
- `app_name` (string, optional): Application name (default: "chrome")

**Returns:** List of all links

**Example:**
```
You: list all links in chrome
Agent: Found 8 links:
  - [elem_20] Images
  - [elem_45] Maps
  - [elem_50] News
  - [elem_55] Shopping
  - [elem_60] Gmail
  - [elem_65] Drive
  - [elem_70] More
  - [elem_75] Settings
```

### 8. list_all_tabs

List all tabs in an application.

**Parameters:**
- `app_name` (string, optional): Application name (default: "chrome")

**Returns:** List of all tabs

**Example:**
```
You: list all tabs in chrome
Agent: Found 3 tabs:
  - [elem_100] Google Search
  - [elem_105] GitHub
  - [elem_110] Stack Overflow
```

### 9. get_page_title

Get the page title from an application.

**Parameters:**
- `app_name` (string, optional): Application name (default: "chrome")

**Returns:** Page title string

**Example:**
```
You: get the page title from chrome
Agent: Google
```

### 10. get_page_content_summary

Get a summary of page content (buttons, links, textboxes).

**Parameters:**
- `app_name` (string, optional): Application name (default: "chrome")
- `max_items` (integer, optional): Maximum items to include (default: 10)

**Returns:** Formatted content summary

**Example:**
```
You: get a summary of the page content
Agent: Page: Google Search

Buttons (5):
  - [elem_15] Google Search
  - [elem_25] I'm Feeling Lucky
  - [elem_30] Settings
  - [elem_35] Sign in
  - [elem_40] More

Links (8):
  - [elem_20] Images
  - [elem_45] Maps
  - [elem_50] News
  - [elem_55] Shopping
  - [elem_60] Gmail
  - [elem_65] Drive
  - [elem_70] More
  - [elem_75] Settings

Textboxes (1):
  - [elem_10] Search
```

### 11. search_element

Search for elements containing a search term.

**Parameters:**
- `app_name` (string, required): Application name
- `search_term` (string, required): Search term

**Returns:** List of matching elements

**Example:**
```
You: search for "sign" in chrome
Agent: Found 2 elements:
  - [elem_35] Sign in
  - [elem_80] Sign out
```

### 12. get_element_path

Get the path to an element in the hierarchy.

**Parameters:**
- `app_name` (string, required): Application name
- `element_id` (string, required): Element ID

**Returns:** Path string showing hierarchy

**Example:**
```
You: get the path to element elem_15
Agent: [elem_1] Google Chrome → [elem_5] Google Search → [elem_15] Google Search
```

### 13. count_elements_by_role

Count elements by role in an application.

**Parameters:**
- `app_name` (string, required): Application name

**Returns:** Dictionary of role counts

**Example:**
```
You: count elements by role in chrome
Agent: {
  "button": 5,
  "link": 8,
  "textbox": 1,
  "document": 1,
  "window": 1
}
```

### 14. get_interactive_elements

Get all interactive elements (buttons, links, textboxes, tabs, checkboxes).

**Parameters:**
- `app_name` (string, optional): Application name (default: "chrome")

**Returns:** Dictionary of interactive elements by type

**Example:**
```
You: get all interactive elements in chrome
Agent: {
  "buttons": [
    {"id": "elem_15", "name": "Google Search"},
    {"id": "elem_25", "name": "I'm Feeling Lucky"},
    ...
  ],
  "links": [
    {"id": "elem_20", "name": "Images"},
    {"id": "elem_45", "name": "Maps"},
    ...
  ],
  "textboxes": [
    {"id": "elem_10", "name": "Search"}
  ],
  "tabs": [...],
  "checkboxes": [...]
}
```

### 15. get_visible_elements

Get all visible elements in an application.

**Parameters:**
- `app_name` (string, optional): Application name (default: "chrome")

**Returns:** List of visible elements

**Example:**
```
You: get all visible elements in chrome
Agent: Found 25 visible elements:
  - [elem_1] window: Google Chrome
  - [elem_5] document: Google Search
  - [elem_10] textbox: Search
  - [elem_15] button: Google Search
  ...
```

### 16. get_enabled_elements

Get all enabled elements in an application.

**Parameters:**
- `app_name` (string, optional): Application name (default: "chrome")

**Returns:** List of enabled elements

**Example:**
```
You: get all enabled elements in chrome
Agent: Found 20 enabled elements:
  - [elem_10] textbox: Search
  - [elem_15] button: Google Search
  - [elem_20] link: Images
  ...
```

## Element Roles

Supported element roles:

- `button` - Clickable buttons
- `link` - Hyperlinks
- `textbox` - Text input fields
- `tab` - Tab items
- `checkbox` - Checkboxes
- `radio` - Radio buttons
- `combobox` - Dropdown menus
- `listbox` - List boxes
- `option` - List items
- `text` - Text elements
- `document` - Document/page content
- `window` - Application window
- `tablist` - Tab container
- `region` - Content region
- `menu` - Menu items
- `menuitem` - Menu item

## Usage Examples

### Example 1: Analyze Page Structure

```
You: analyze the structure of the current page
Agent: 
1. read_accessibility_tree() → Get full tree
2. count_elements_by_role() → Count by type
3. get_page_content_summary() → Get summary

Result: Page has 5 buttons, 8 links, 1 textbox
```

### Example 2: Find and Interact with Element

```
You: find the search button and tell me its ID
Agent:
1. find_element_by_name("Search") → Find element
2. get_element_info(element_id) → Get details

Result: Found button elem_15 "Google Search"
```

### Example 3: List All Interactive Elements

```
You: show me all interactive elements
Agent:
1. get_interactive_elements() → Get all interactive

Result: 5 buttons, 8 links, 1 textbox, 3 tabs, 2 checkboxes
```

### Example 4: Search for Specific Element

```
You: find all elements containing "sign"
Agent:
1. search_element("sign") → Search

Result: Found 2 elements:
  - elem_35: Sign in
  - elem_80: Sign out
```

### Example 5: Get Element Hierarchy

```
You: show me the path to the search button
Agent:
1. find_element_by_name("Search") → Find element
2. get_element_path(element_id) → Get path

Result: Chrome → Google Search → Search Button
```

## Integration with Agent

The accessibility tools are automatically registered with the agent and can be used in natural language:

```
You: read the page and find all buttons
Agent: [Uses read_accessibility_tree and list_all_buttons]

You: search for "login" in the current page
Agent: [Uses search_element]

You: get a summary of interactive elements
Agent: [Uses get_interactive_elements]
```

## Performance Tips

1. **Use specific searches** - `find_element_by_name()` is faster than `read_accessibility_tree()`
2. **Limit depth** - Use `max_depth` parameter to reduce tree size
3. **Filter by role** - Use `find_elements_by_role()` for specific element types
4. **Cache results** - Store element IDs for repeated use
5. **Use summaries** - `get_page_content_summary()` is faster than full tree

## Error Handling

All tools return error information if something goes wrong:

```
{
  "error": "Failed to connect to chrome"
}
```

Common errors:
- Application not running
- Application not found
- Element not found
- Permission denied
- UI Automation not available

## Supported Applications

- Chrome
- Microsoft Edge
- Firefox
- Any UIA-compatible application

## Advanced Usage

### Combining Tools

```
You: find all buttons and tell me which ones are enabled
Agent:
1. list_all_buttons() → Get all buttons
2. Filter by is_enabled=true

Result: 4 out of 5 buttons are enabled
```

### Element Analysis

```
You: analyze the page structure and suggest what I can interact with
Agent:
1. get_interactive_elements() → Get all interactive
2. get_visible_elements() → Get visible
3. get_enabled_elements() → Get enabled

Result: You can interact with 5 buttons, 8 links, 1 textbox
```

### Hierarchical Navigation

```
You: show me the hierarchy of the search button
Agent:
1. find_element_by_name("Search") → Find element
2. get_element_path(element_id) → Get path
3. get_element_info(element_id) → Get details

Result: Full hierarchy and details
```

## Limitations

1. **Requires UIA Support** - Application must expose UI via Windows UI Automation
2. **Read-Only** - These tools read information, they don't execute actions
3. **Dynamic Content** - Must re-read after page changes
4. **Performance** - Large trees may take time to extract

## Future Enhancements

- [ ] Element filtering by attributes
- [ ] XPath-like queries
- [ ] Element change detection
- [ ] Performance optimization
- [ ] Caching layer
- [ ] Batch operations
- [ ] Custom matchers

## See Also

- [HUMAN_LIKE_BEHAVIOR.md](HUMAN_LIKE_BEHAVIOR.md) - Human-like automation
- [SMART_UI_GUIDE.md](SMART_UI_GUIDE.md) - Smart UI Agent
- [DOCUMENTATION.md](DOCUMENTATION.md) - Complete documentation
