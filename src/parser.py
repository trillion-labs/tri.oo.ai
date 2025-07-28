import re
import json
from typing import List, Optional

from .types import Function, ToolCall, ParsedMessage


class MessageParser:
    """Parser for extracting structured content from assistant messages"""
    
    @staticmethod
    def extract_tag_content(text: str, tag: str) -> List[str]:
        """Extract content from XML-like tags"""
        pattern = f'<{tag}>(.*?)</{tag}>'
        return re.findall(pattern, text, re.DOTALL)
    
    @staticmethod
    def parse_tool_calls_from_content(content: str) -> List[ToolCall]:
        """Parse tool calls from content string"""
        tool_calls = []
        tool_call_contents = MessageParser.extract_tag_content(content, 'tool_call')
        
        for i, match in enumerate(tool_call_contents):
            try:
                tool_data = json.loads(match.strip())
                function = Function(
                    name=tool_data.get('name', ''),
                    arguments=json.dumps(tool_data.get('arguments', {}))
                )
                tool_call = ToolCall(
                    function=function,
                    id=tool_data.get('id') or f"call_parsed_{i}"
                )
                tool_calls.append(tool_call)
            except json.JSONDecodeError:
                continue
                
        return tool_calls
    
    @staticmethod
    def parse_message(message_content: str) -> ParsedMessage:
        """Parse a message to extract content, reasoning, and tool calls"""
        parsed = ParsedMessage(content=message_content)
        
        # Extract reasoning from <think> tags
        parsed.reasoning = MessageParser._extract_reasoning(message_content)
        
        # Extract tool calls from <tool_call> tags
        parsed.tool_calls = MessageParser.parse_tool_calls_from_content(message_content)
        
        return parsed
    
    @staticmethod
    def _extract_reasoning(content: str) -> Optional[str]:
        """Extract reasoning from <think> tags"""
        think_contents = MessageParser.extract_tag_content(content, 'think')
        return '\n'.join(think_contents).strip() if think_contents else None