import argparse
from vllm import LLM
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.agent import WebAssistant


def initialize_vllm(model_name: str, console: Console, **kwargs):
    """Initialize vLLM model"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(f"Loading model: {model_name}", total=None)
        llm = LLM(
            model=model_name,
            trust_remote_code=True,
            enforce_eager=True,
            **kwargs
        )
        progress.update(task, completed=True)
    return llm


def main():
    """Main interactive loop"""
    console = Console()
    parser = argparse.ArgumentParser(description="Web QA Assistant using vLLM")
    parser.add_argument(
        "--model", 
        type=str, 
        default="trillionlabs/Tri-7B-Search-preview",
        help="Model name or path"
    )
    parser.add_argument(
        "--tensor-parallel-size", 
        type=int, 
        default=1,
        help="Number of GPUs for tensor parallelism"
    )
    parser.add_argument(
        "--gpu-memory-utilization", 
        type=float, 
        default=0.9,
        help="GPU memory utilization (0-1)"
    )
    args = parser.parse_args()
    
    # Initialize vLLM
    llm = initialize_vllm(
        args.model,
        console,
        tensor_parallel_size=args.tensor_parallel_size,
        gpu_memory_utilization=args.gpu_memory_utilization,
    )
    
    # Create assistant
    assistant = WebAssistant(llm)
    
    console.print("[green]✓[/green] Model loaded successfully!")
    console.print(Panel("[bold green]Web QA Assistant[/bold green]\n[dim]Type 'quit' to exit[/dim]", border_style="green"))
    console.print()
    
    while True:
        # Get user input
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


if __name__ == "__main__":
    main()