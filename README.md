# tri.oo.ai

A powerful web search assistant powered by Tri-7B-Search and vLLM, providing real-time information retrieval capabilities through DuckDuckGo integration.

## Features

- **Real-time Web Search**: Leverages DuckDuckGo for up-to-date information retrieval
- **Advanced Language Model**: Powered by Tri-7B-Search for intelligent response generation
- **High Performance**: Built on vLLM for efficient inference
- **Modular Architecture**: Clean, maintainable codebase with separated concerns
- **Tool Calling**: Structured approach to web search integration

## Requirements

- Python 3.8 or higher
- CUDA-compatible GPU (for vLLM)
- UV package manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tri.oo.ai.git
cd tri.oo.ai
```

2. Install UV (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Create virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

## Usage

Run the interactive assistant:

```bash
python main.py
```

### Command Line Options

- `--model`: Model name or path (default: "trillion;")
- `--tensor-parallel-size`: Number of GPUs for tensor parallelism (default: 1)
- `--gpu-memory-utilization`: GPU memory utilization 0-1 (default: 0.9)

Example with custom settings:
```bash
python main.py --model "path/to/model" --tensor-parallel-size 2 --gpu-memory-utilization 0.8
```

## Project Structure

```
tri.oo.ai/
├── src/
│   ├── __init__.py
│   ├── types.py      # Data models and type definitions
│   ├── parser.py     # Message parsing utilities
│   ├── tools.py      # Tool implementations (web search)
│   └── agent.py      # Main WebAssistant class
├── main.py           # Entry point
├── pyproject.toml    # Project configuration
└── README.md         # This file
```

## Development

### Running Tests

```bash
uv pip install -e ".[dev]"
pytest
```

### Code Formatting

```bash
black .
ruff check .
```

## Configuration

The assistant can be configured through command-line arguments or by modifying the default values in `main.py`.

### Model Configuration

The default model is set to "trillion;" but can be changed to any vLLM-compatible model:

```python
assistant = WebAssistant(llm, available_tools={"search": search_web})
```

### System Prompt

The system prompt can be customized in `src/agent.py`:

```python
SYSTEM_PROMPT = """You are a helpful assistant that searches the web and answers questions based on search results. 
You excel at finding information through strategic searching. Current time is {time}"""
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Powered by [vLLM](https://github.com/vllm-project/vllm) for efficient inference
- Web search functionality via [DuckDuckGo Search](https://github.com/deedy5/duckduckgo_search)
- Inspired by oo.ai's approach to web-enhanced AI assistants
