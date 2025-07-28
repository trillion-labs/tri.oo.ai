# tri.oo.ai

**tri.oo.ai** is a local, open-source showcase of what you can build with **[Tri-7B-Search](https://huggingface.co/trillionlabs/Tri-7B-Search-preview)**, an efficient LLM with search capabilities 💚. It brings a familiar chat-based interface — inspired by [oo.ai](https://oo.ai).

## 🔍 What is tri.oo.ai?

tri.oo.ai replicates the functionality of oo.ai with a local-first approach and open tooling. It uses the **Tri-7B-Search** model as the engine behind a smart assistant that can:

* Understand natural queries
* Retrieve relevant data from your knowledge base
* Augment answers with **DuckDuckGo search results**
* Run locally for full control and privacy

This is a **search-enabled LLM service** — combining the reasoning of LLMs with the freshness of web search.


## 💡 Example

> 페이커 재계약 소식


페이커(이상혁)는 **2029년까지 T1과 4년 재계약**을 체결한 사실이 확인되었습니다. 이는 2025년 7월 27일(2025년 기준) 공식 발표된 내용으로, 리그 오브 레전드(LoL) e스포츠 역사상 최초로 **18시즌 연속 활동**을 이어가게 되었습니다. 주요 계약 조건은 다음과 같습니다:
- **계약 기간**: 2025년 7월 27일부터 **2029년 6월 30일까지** (4년간)
- **성과**: 해당 기간 동안 **2022 LCK 스프링 전승 우승**, **2023 아시안게임 금메달**, **2023·2024 LoL 월드 챔피언십 2연패** 등 역대 최고 수준의 성적을 기록했습니다.
- **의미**: 페이커는 2013년 데뷔 이래 **팀의 상징**으로 활약하며 e스포츠 역사에 한 획을 그은 선수로 평가받고 있습니다.

**출처**
1. [조선비즈] [페이커 이상혁, T1과 4년 재계약 발표](https://www.chosun.com/sports/sports_general/2025/07/27/VOQ3LGJWPFBX7DKGXD5ESQBTZQ/)  
2. [연합뉴스] [페이커 이상혁, 2029년까지 뛴다…T1과 4년 재계약](https://www.yna.co.kr/view/AKR20250727045800017)  
3. [게임뷰] [페이커 이상혁, T1과 4년 재계약 발표 '2029년까지 동행'](https://www.gamevu.co.kr/news/articleView.html?idxno=50414)


## Installation

1. Clone the repository:
```bash
git clone https://github.com/trillion-labs/tri.oo.ai.git
cd tri.oo.ai
```

2. Install UV (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Create virtual environment and install dependencies:
```bash
uv sync

# for offline vllm usage
uv sync --group vllm
```

## Usage

### Option 1: Direct vLLM Usage

Run the interactive assistant with direct vLLM integration:

```bash
uv run main.py
```

Command line options:
- `--model`: Model name or path (default: "trillionlabs/Tri-7B-Search-preview")
- `--tensor-parallel-size`: Number of GPUs for tensor parallelism (default: 1)
- `--gpu-memory-utilization`: GPU memory utilization 0-1 (default: 0.9)

Example:
```bash
uv run main.py --tensor-parallel-size 2 --gpu-memory-utilization 0.8
```

### Option 2: OpenAI-Compatible API

For better flexibility and integration, you can use the OpenAI-compatible API:

1. Start the vLLM server:
```bash
./serve.sh
```

This will start a vLLM server at `http://localhost:8000` with the Tri-7B-Search-preview model.

2. In a new terminal, run the API client:
```bash
uv run main_api.py
```

Command line options for the API client:
- `--base-url`: Base URL for the OpenAI-compatible API (default: "http://localhost:8000/v1")
- `--model`: Model name (default: "trillionlabs/Tri-7B-Search-preview")

Example with custom server:
```bash
python main_api.py --base-url "http://your-server:8080/v1"
```

### Which Option to Choose?

- **Direct vLLM (`main.py`)**: Best for single-user local usage with minimal setup
- **API mode (`main_api.py`)**: Best for multi-user scenarios, integration with other tools, or when you want to separate the model server from the client

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Powered by [vLLM](https://github.com/vllm-project/vllm) for efficient inference
- Web search functionality via [DuckDuckGo Search](https://github.com/deedy5/duckduckgo_search)