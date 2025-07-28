from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Function:
    name: str
    arguments: str  # JSON string of arguments
    
    
@dataclass
class ToolCall:
    function: Function
    id: Optional[str] = None
    type: str = "function"


@dataclass
class ParsedMessage:
    content: str
    reasoning: Optional[str] = None
    tool_calls: List[ToolCall] = field(default_factory=list)