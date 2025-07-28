import argparse
from vllm import LLM

from src.agent import WebAssistant


def initialize_vllm(model_name: str, **kwargs):
    """Initialize vLLM model"""
    print(f"Loading model: {model_name}")
    return LLM(
        model=model_name,
        trust_remote_code=True,
        **kwargs
    )


def main():
    """Main interactive loop"""
    parser = argparse.ArgumentParser(description="Web QA Assistant using vLLM")
    parser.add_argument(
        "--model", 
        type=str, 
        default="trillion;",
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
        tensor_parallel_size=args.tensor_parallel_size,
        gpu_memory_utilization=args.gpu_memory_utilization,
    )
    
    # Create assistant
    assistant = WebAssistant(llm)
    
    print(f"Model loaded successfully!")
    print("Type 'quit' to exit\n")
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Prepare messages
        messages = [
            {"role": "system", "content": assistant.get_system_prompt()},
            {"role": "user", "content": user_input}
        ]
        
        # Get response
        print("\nAssistant: ", end="", flush=True)
        response = assistant.run_with_tools(messages)
        print(response)
        print()


if __name__ == "__main__":
    main()