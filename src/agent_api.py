import json
from typing import List, Dict, Any
from datetime import datetime
from openai import OpenAI
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.markdown import Markdown

from .types import ToolCall
from .parser import MessageParser
from .tools import search_web


class WebAssistantAPI:
    """Web search assistant using OpenAI-compatible API"""
    
    SYSTEM_PROMPT = """You are a helpful assistant that searches the web and answers questions based on search results. 
You excel at finding information through strategic searching. Current time is {time}"""
    
    def __init__(self, base_url: str = "http://localhost:8000/v1", model: str = "trillionlabs/Tri-7B-Search-preview"):
        self.client = OpenAI(
            base_url=base_url,
            api_key="dummy-key",  # vLLM doesn't require a real key for local serving
        )
        self.model = model
        self.available_tools = {"search": search_web}
        self.console = Console()
    
    def process_tool_calls(self, tool_calls: List[ToolCall]) -> List[Dict[str, Any]]:
        """Execute tool calls and return responses"""
        responses = []
        
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            if function_name in self.available_tools:
                result = self.available_tools[function_name](**arguments)
                responses.append({
                    "role": "tool",
                    "content": json.dumps(result, ensure_ascii=False),
                    "tool_call_id": tool_call.id
                })
        
        return responses
    
    def format_tool_calls_for_messages(self, tool_calls: List[ToolCall], iteration: int = 0) -> List[Dict[str, Any]]:
        """Format tool calls for message history"""
        return [
            {
                "id": tc.id or f"call_{iteration}_{idx}",
                "type": "function",
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments
                }
            } for idx, tc in enumerate(tool_calls)
        ]
    
    def display_search_results(self, results_json: str) -> None:
        """Display search results in a readable format"""
        results = json.loads(results_json)
        
        if not results:
            self.console.print("[yellow]No results found[/yellow]")
            return
        
        self.console.print("\n[bold cyan]Search Results:[/bold cyan]")
        for idx, doc in enumerate(results[:3], 1):
            panel_content = f"[bold]{doc['title']}[/bold]\n\n{doc['snippet'][:200]}..."
            self.console.print(Panel(panel_content, title=f"Result {idx}", border_style="cyan"))
        self.console.print()
    
    def run_with_tools(self, messages: List[Dict[str, Any]], max_iterations: int = 3) -> str:
        """Run assistant with tool calling capabilities"""
        for iteration in range(max_iterations + 1):
            # Get assistant response using OpenAI API
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
                console=self.console
            ) as progress:
                task = progress.add_task("Thinking...", total=None)
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=8192,
                    extra_body={
                        "skip_special_tokens": False
                    }
                )
                progress.update(task, completed=True)
            
            response_text = response.choices[0].message.content
            
            # Parse the response
            parsed = MessageParser.parse_message(response_text)
            
            # If no tool calls, return final answer
            if not parsed.tool_calls:
                return response_text
            
            # Add assistant message to conversation
            messages.append({
                "role": "assistant",
                "content": response_text,
                "tool_calls": self.format_tool_calls_for_messages(parsed.tool_calls, iteration)
            })
            
            # Process tool calls
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
                console=self.console
            ) as progress:
                task = progress.add_task("Searching the web...", total=None)
                tool_responses = self.process_tool_calls(parsed.tool_calls)
                messages.extend(tool_responses)
                progress.update(task, completed=True)
            
            # Display results if it's a search
            if tool_responses and "search" in parsed.tool_calls[0].function.name:
                self.display_search_results(tool_responses[0]["content"])
        
        return response_text
    
    def get_system_prompt(self) -> str:
        """Get formatted system prompt with current time"""
        return self.SYSTEM_PROMPT.format(time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))