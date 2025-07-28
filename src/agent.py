import json
from typing import List, Dict, Any
from datetime import datetime

from vllm import LLM, SamplingParams

from .types import ToolCall
from .parser import MessageParser
from .tools import search_web


class WebAssistant:
    """Web search assistant using vLLM"""
    
    SYSTEM_PROMPT = """You are a helpful assistant that searches the web and answers questions based on search results. 
You excel at finding information through strategic searching. Current time is {time}"""
    
    def __init__(self, llm: LLM, available_tools: Dict[str, Any] = None):
        self.llm = llm
        self.available_tools = available_tools or {"search": search_web}
        self.sampling_params = SamplingParams(
            temperature=0.7,
            max_tokens=2048,
            skip_special_tokens=False,
        )
    
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
            print("No results found")
            return
        
        print("\n" + "="*80)
        for idx, doc in enumerate(results[:3], 1):
            print(f"\n{idx}. {doc['title']}")
            print(f"   {doc['snippet'][:200]}...")
        print("="*80 + "\n")
    
    def run_with_tools(self, messages: List[Dict[str, Any]], max_iterations: int = 3) -> str:
        """Run assistant with tool calling capabilities"""
        for iteration in range(max_iterations + 1):
            # Get assistant response
            outputs = self.llm.chat(messages=[messages], sampling_params=self.sampling_params)
            response_text = outputs[0].outputs[0].text
            
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
            tool_responses = self.process_tool_calls(parsed.tool_calls)
            messages.extend(tool_responses)
            
            # Display results if it's a search
            if tool_responses and "search" in parsed.tool_calls[0].function.name:
                self.display_search_results(tool_responses[0]["content"])
        
        return response_text
    
    def get_system_prompt(self) -> str:
        """Get formatted system prompt with current time"""
        return self.SYSTEM_PROMPT.format(time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))