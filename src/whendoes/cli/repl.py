"""Interactive REPL for Whendoes CLI."""

import os
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from whendoes.agent.agent import Agent
from whendoes.agent.tool_registry import ToolRegistry
from whendoes.llm import create_provider
from whendoes.config import get_config
from whendoes.cli.setup import setup_wizard, show_provider_info
import whendoes.windows_api as wapi


console = Console()


def setup_tools() -> ToolRegistry:
    """Set up tool registry with all available tools.

    Returns:
        Configured ToolRegistry
    """
    registry = ToolRegistry()

    # Window management tools
    registry.register(
        "list_windows",
        "List all open windows",
        wapi.list_windows,
        {
            "type": "object",
            "properties": {},
            "required": [],
        },
    )

    registry.register(
        "focus_window",
        "Focus a window by title",
        wapi.focus_window,
        {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Window title (partial match)"}
            },
            "required": ["title"],
        },
    )

    registry.register(
        "close_window",
        "Close a window by title",
        wapi.close_window,
        {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Window title (partial match)"}
            },
            "required": ["title"],
        },
        requires_approval=True,
    )

    registry.register(
        "minimize_window",
        "Minimize a window by title",
        wapi.minimize_window,
        {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Window title (partial match)"}
            },
            "required": ["title"],
        },
    )

    registry.register(
        "maximize_window",
        "Maximize a window by title",
        wapi.maximize_window,
        {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Window title (partial match)"}
            },
            "required": ["title"],
        },
    )

    # Process management tools
    registry.register(
        "list_processes",
        "List all running processes",
        wapi.list_processes,
        {
            "type": "object",
            "properties": {},
            "required": [],
        },
    )

    registry.register(
        "start_process",
        "Start a new process",
        wapi.start_process,
        {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Command to execute"}
            },
            "required": ["command"],
        },
    )

    registry.register(
        "stop_process",
        "Stop a process by PID",
        wapi.stop_process,
        {
            "type": "object",
            "properties": {
                "pid": {"type": "integer", "description": "Process ID"}
            },
            "required": ["pid"],
        },
        requires_approval=True,
    )

    registry.register(
        "kill_process",
        "Kill a process by PID (force)",
        wapi.kill_process,
        {
            "type": "object",
            "properties": {
                "pid": {"type": "integer", "description": "Process ID"}
            },
            "required": ["pid"],
        },
        requires_approval=True,
    )

    # File operations tools
    registry.register(
        "list_files",
        "List files in a directory",
        wapi.list_files,
        {
            "type": "object",
            "properties": {
                "directory": {"type": "string", "description": "Directory path"}
            },
            "required": ["directory"],
        },
    )

    registry.register(
        "create_file",
        "Create a new file",
        wapi.create_file,
        {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path"},
                "content": {"type": "string", "description": "File content"},
            },
            "required": ["path"],
        },
    )

    registry.register(
        "delete_file",
        "Delete a file",
        wapi.delete_file,
        {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path"}
            },
            "required": ["path"],
        },
        requires_approval=True,
    )

    registry.register(
        "copy_file",
        "Copy a file",
        wapi.copy_file,
        {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Source file path"},
                "destination": {"type": "string", "description": "Destination file path"},
            },
            "required": ["source", "destination"],
        },
    )

    registry.register(
        "move_file",
        "Move a file",
        wapi.move_file,
        {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "Source file path"},
                "destination": {"type": "string", "description": "Destination file path"},
            },
            "required": ["source", "destination"],
        },
    )

    registry.register(
        "read_file",
        "Read file content",
        wapi.read_file,
        {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path"}
            },
            "required": ["path"],
        },
    )

    registry.register(
        "write_file",
        "Write to file",
        wapi.write_file,
        {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path"},
                "content": {"type": "string", "description": "Content to write"},
            },
            "required": ["path", "content"],
        },
    )

    # App launching tools
    registry.register(
        "launch_app",
        "Launch an application",
        wapi.launch_app,
        {
            "type": "object",
            "properties": {
                "app_path": {"type": "string", "description": "Path to application"},
                "args": {"type": "array", "items": {"type": "string"}, "description": "Arguments"},
            },
            "required": ["app_path"],
        },
    )

    registry.register(
        "launch_app_by_name",
        "Launch application by name",
        wapi.launch_app_by_name,
        {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "Application name"},
                "args": {"type": "array", "items": {"type": "string"}, "description": "Arguments"},
            },
            "required": ["app_name"],
        },
    )

    registry.register(
        "find_app_path",
        "Find installed application path by name (searches Program Files, Registry, common locations)",
        wapi.find_app_path,
        {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "Application name (e.g., 'Chrome', 'Firefox', 'Notepad')"},
            },
            "required": ["app_name"],
        },
    )

    registry.register(
        "launch_url",
        "Open URL in default browser",
        wapi.launch_url,
        {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL to open"}
            },
            "required": ["url"],
        },
    )

    # System info tools
    registry.register(
        "get_system_info",
        "Get system information",
        lambda: wapi.get_system_info().__dict__,
        {
            "type": "object",
            "properties": {},
            "required": [],
        },
    )

    return registry


def run_repl() -> None:
    """Run interactive REPL."""
    config = get_config()

    # Display welcome message
    console.print(
        Panel(
            "[bold cyan]Whendoes CLI[/bold cyan]\n"
            "Control Windows via natural language\n"
            "Type 'help' for commands, 'exit' to quit",
            expand=False,
        )
    )

    # Check if API key is configured
    if not config.llm.api_key and config.llm.provider != "ollama":
        console.print(
            "[yellow]⚠️  No API key configured for {provider}[/yellow]".format(
                provider=config.llm.provider
            )
        )
        response = Prompt.ask(
            "Would you like to set up an API key now?",
            choices=["y", "n"],
            default="y",
        )
        if response == "y":
            if setup_wizard():
                # Reload config
                from importlib import reload
                import whendoes.config
                reload(whendoes.config)
                config = get_config()
            else:
                console.print("[red]Setup cancelled[/red]")
                return
        else:
            console.print("[yellow]You can run 'whendoes setup' to configure later[/yellow]")
            return

    # Initialize LLM provider
    try:
        llm = create_provider(
            config.llm.provider,
            api_key=config.llm.api_key,
            model=config.llm.model,
            temperature=config.llm.temperature,
            max_tokens=config.llm.max_tokens,
            base_url=config.llm.base_url,
        )
        console.print(
            f"[green]✓ Connected to {config.llm.provider} ({config.llm.model})[/green]\n"
        )
    except Exception as e:
        console.print(f"[red]Error initializing LLM provider: {e}[/red]")
        console.print("[yellow]Please check your API key and try again[/yellow]")
        return

    # Set up tools
    tools = setup_tools()

    # Create streaming callback
    stream_output = []

    def stream_callback(text: str) -> None:
        """Callback for streaming output."""
        stream_output.append(text)
        console.print(text, end="")

    # Create agent
    agent = Agent(
        llm_provider=llm,
        tool_registry=tools,
        max_iterations=config.agent.max_iterations,
        require_approval=config.agent.require_approval,
        verbose=config.agent.verbose,
        stream_callback=stream_callback,
    )

    # REPL loop
    while True:
        try:
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit":
                console.print("[yellow]Goodbye![/yellow]")
                break

            if user_input.lower() == "help":
                console.print(
                    Panel(
                        "[bold]Available Commands:[/bold]\n"
                        "exit - Exit the CLI\n"
                        "help - Show this help message\n"
                        "info - Show provider information\n"
                        "\n[bold]Examples:[/bold]\n"
                        "• List all open windows\n"
                        "• Close the Chrome window\n"
                        "• Start Notepad\n"
                        "• Show system information",
                        expand=False,
                    )
                )
                continue

            if user_input.lower() == "info":
                show_provider_info()
                continue

            # Run agent
            console.print("[cyan]Thinking...[/cyan]")
            try:
                stream_output.clear()
                response = agent.run(user_input)
                console.print(f"\n[bold cyan]Assistant[/bold cyan]: {response}\n")
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]\n")

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
