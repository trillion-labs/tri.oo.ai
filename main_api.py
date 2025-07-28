#!/usr/bin/env python3
"""
Main entry point for Web QA Assistant using OpenAI-compatible API
"""

import argparse
import sys
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint
from src.agent_api import WebAssistantAPI


def create_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Web QA Assistant using OpenAI-compatible API",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--base-url", 
        type=str, 
        default="http://localhost:8000/v1",
        help="Base URL for the OpenAI-compatible API"
    )
    parser.add_argument(
        "--model", 
        type=str, 
        default="trillionlabs/Tri-7B-Search-preview",
        help="Model name"
    )
    return parser


def run_interactive_session(assistant: WebAssistantAPI):
    """Run interactive chat session"""
    console = Console()
    console.print(Panel("[bold green]Web QA Assistant[/bold green]\n[dim]Type 'quit' to exit[/dim]", border_style="green"))
    console.print()
    
    while True:
        try:
            # Get user input with rich prompt
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            if not user_input:
                continue
            
            # Prepare messages
            messages = [
                {"role": "system", "content": assistant.get_system_prompt()},
                {"role": "user", "content": user_input}
            ]
            
            # Get response
            console.print("\n[bold green]Assistant:[/bold green] ", end="")
            response = assistant.run_with_tools(messages)
            console.print(response)
            console.print()
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {e}")
            console.print("[dim]Make sure the vLLM server is running with: ./serve.sh[/dim]")


def main():
    """Main function"""
    console = Console()
    
    # Parse arguments
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        # Create assistant
        console.print("[dim]Connecting to API...[/dim]")
        assistant = WebAssistantAPI(base_url=args.base_url, model=args.model)
        
        console.print(f"[green]✓[/green] Connected to API at [cyan]{args.base_url}[/cyan]")
        console.print(f"[green]✓[/green] Using model: [cyan]{args.model}[/cyan]")
        console.print()
        
        # Run interactive session
        run_interactive_session(assistant)
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}", style="red")
        sys.exit(1)


if __name__ == "__main__":
    main()