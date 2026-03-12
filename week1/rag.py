import os
import re
from typing import List, Callable
from dotenv import load_dotenv
from llm import chat

load_dotenv()

NUM_RUNS_TIMES = 5

DATA_FILES: List[str] = [
    os.path.join(os.path.dirname(__file__), "data", "api_docs.txt"),
]


def load_corpus_from_files(paths: List[str]) -> List[str]:
    corpus: List[str] = []
    for p in paths:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    corpus.append(f.read())
            except Exception as exc:
                corpus.append(f"[load_error] {p}: {exc}")
        else:
            corpus.append(f"[missing_file] {p}")
    return corpus


# Load corpus from external files (simple API docs). If missing, fall back to inline snippet
CORPUS: List[str] = load_corpus_from_files(DATA_FILES)

QUESTION = (
    "编写一个 Python 函数 `fetch_user_name(user_id: str, api_key: str) -> str`，该函数调用文档中的 API "
    "通过 id 获取用户，并仅返回用户的名称字符串。"
)


# TODO: Fill this in!
YOUR_SYSTEM_PROMPT = '''  
    '''


# For this simple example
# For this coding task, validate by required snippets rather than exact string
REQUIRED_SNIPPETS = [
    "def fetch_user_name(",
    "requests.get",
    "/users/",
    "X-API-Key",
    "return",
]


def YOUR_CONTEXT_PROVIDER(corpus: List[str]) -> List[str]:
    """TODO: 选择并返回语料库 (CORPUS) 中与此任务相关的文档子集。

    例如，返回 [] 以模拟缺少上下文，或 [corpus[0]] 以包含 API 文档。
    """
    return []


def make_user_prompt(question: str, context_docs: List[str]) -> str:
    if context_docs:
        context_block = "\n".join(f"- {d}" for d in context_docs)
    else:
        context_block = "(no context provided)"
    return (
        f"上下文 (仅使用此信息):\n{context_block}\n\n"
        f"任务: {question}\n\n"
        "要求:\n"
        "- 使用文档中的 Base URL 和端点。\n"
        "- 发送文档中的认证头。\n"
        "- 对非 200 响应抛出异常。\n"
        "- 仅返回用户的名称字符串。\n\n"
        "输出: 一个包含函数和必要导入的 Python 代码块。\n"
    )


def extract_code_block(text: str) -> str:
    """提取最后一个围栏 Python 代码块，或任何围栏代码块，否则返回文本。"""
    # Try ```python ... ``` first
    m = re.findall(r"```python\n([\s\S]*?)```", text, flags=re.IGNORECASE)
    if m:
        return m[-1].strip()
    # Fallback to any fenced code block
    m = re.findall(r"```\n([\s\S]*?)```", text)
    if m:
        return m[-1].strip()
    return text.strip()


def test_your_prompt(system_prompt: str, context_provider: Callable[[List[str]], List[str]]) -> bool:
    """运行最多 NUM_RUNS_TIMES 次，如果任何输出匹配 EXPECTED_OUTPUT 则返回 True。"""
    context_docs = context_provider(CORPUS)
    user_prompt = make_user_prompt(QUESTION, context_docs)

    for idx in range(NUM_RUNS_TIMES):
        print(f"正在运行第 {idx + 1} 次测试，共 {NUM_RUNS_TIMES} 次")
        response = chat(
            model="test-model",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            options={"temperature": 0.0},
        )
        output_text = response.message.content
        code = extract_code_block(output_text)
        missing = [s for s in REQUIRED_SNIPPETS if s not in code]
        if not missing:
            print("SUCCESS")
            return True
        else:
            print("缺少必要的代码片段:")
            for s in missing:
                print(f"  - {s}")
            print("生成的代码:\n" + code)
    return False


if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT, YOUR_CONTEXT_PROVIDER)
