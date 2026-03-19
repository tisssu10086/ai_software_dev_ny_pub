import os
import re
from typing import Callable, List, Tuple
from dotenv import load_dotenv
from llm import chat

load_dotenv()

NUM_RUNS_TIMES = 1

SYSTEM_PROMPT = """
你是一个编程助手。仅输出一个定义了函数 is_valid_password(password: str) -> bool 的围栏 Python 代码块。不要有其他文字或注释。
保持实现尽可能精简。
"""

# TODO: Fill this in!
YOUR_REFLEXION_PROMPT = '''
'''


# Ground-truth test suite used to evaluate generated code
SPECIALS = set("!@#$%^&*()-_")
TEST_CASES: List[Tuple[str, bool]] = [
    ("Password1!", True),       # 有效
    ("password1!", False),      # 缺少大写
    ("Password!", False),       # 缺少数字
    ("Password1", False),       # 缺少特殊字符
    # 边缘情况
    ("Pas1!", False),           # 太短 (只有 5 个字符)
    ("Pass 1!Aa", False),      # 包含空格
    ("PASSWORD1!", False),      # 缺少小写
    ("Password1!Password1!", True),  # 长密码，仍然有效
]


def extract_code_block(text: str) -> str:
    m = re.findall(r"```python\n([\s\S]*?)```", text, flags=re.IGNORECASE)
    if m:
        return m[-1].strip()
    m = re.findall(r"```\n([\s\S]*?)```", text)
    if m:
        return m[-1].strip()
    return text.strip()


def load_function_from_code(code_str: str) -> Callable[[str], bool]:
    namespace: dict = {}
    exec(code_str, namespace)  # noqa: S102 (executing controlled code from model for exercise)
    func = namespace.get("is_valid_password")
    if not callable(func):
        raise ValueError("No callable is_valid_password found in generated code")
    return func


def evaluate_function(func: Callable[[str], bool]) -> Tuple[bool, List[str]]:
    failures: List[str] = []
    for pw, expected in TEST_CASES:
        try:
            result = bool(func(pw))
        except Exception as exc:
            failures.append(f"输入: {pw} → 抛出异常: {exc}")
            continue

        if result != expected:
            # Compute diagnostic based on ground-truth rules
            reasons = []
            if len(pw) < 8:
                reasons.append("长度 < 8")
            if not any(c.islower() for c in pw):
                reasons.append("缺少小写字母")
            if not any(c.isupper() for c in pw):
                reasons.append("缺少大写字母")
            if not any(c.isdigit() for c in pw):
                reasons.append("缺少数字")
            if not any(c in SPECIALS for c in pw):
                reasons.append("缺少特殊字符")
            if any(c.isspace() for c in pw):
                reasons.append("包含空格")

            failures.append(
                f"输入: {pw} → 预期 {expected}, 得到 {result}. 失败检查: {', '.join(reasons) or '未知'}"
            )

    return (len(failures) == 0, failures)


def generate_initial_function(system_prompt: str) -> str:
    response = chat(
        model="test-model",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "现在提供实现。"},
        ],
        options={"temperature": 0.2},
    )
    return extract_code_block(response.message.content)


def your_build_reflexion_context(prev_code: str, failures: List[str]) -> str:
    """TODO: 使用 prev_code 和 failures 构建反思步骤的用户消息。

    返回一个将作为用户内容与反思系统提示词一起发送的字符串。
    """



def apply_reflexion(
    reflexion_prompt: str,
    build_context: Callable[[str, List[str]], str],
    prev_code: str,
    failures: List[str],
) -> str:
    reflection_context = build_context(prev_code, failures)
    print(f"反思上下文: {reflection_context}, {reflexion_prompt}")
    response = chat(
        model="test-model",
        messages=[
            {"role": "system", "content": reflexion_prompt},
            {"role": "user", "content": reflection_context},
        ],
        options={"temperature": 0.2},
    )
    return extract_code_block(response.message.content)


def run_reflexion_flow(
    system_prompt: str,
    reflexion_prompt: str,
    build_context: Callable[[str, List[str]], str],
) -> bool:
    # 1) Generate initial function
    initial_code = generate_initial_function(system_prompt)
    print("初始代码:\n" + initial_code)
    func = load_function_from_code(initial_code)
    passed, failures = evaluate_function(func)
    if passed:
        print("成功 (初始实现通过所有测试)")
        return True
    else:
        print(f"失败 (初始实现未通过部分测试): {failures}")

    # 2) Single reflexion iteration
    improved_code = apply_reflexion(reflexion_prompt, build_context, initial_code, failures)
    print("\n改进后的代码:\n" + improved_code)
    improved_func = load_function_from_code(improved_code)
    passed2, failures2 = evaluate_function(improved_func)
    if passed2:
        print("成功")
        return True

    print("反思后仍然失败的测试:")
    for f in failures2:
        print("- " + f)
    return False


if __name__ == "__main__":
    run_reflexion_flow(SYSTEM_PROMPT, YOUR_REFLEXION_PROMPT, your_build_reflexion_context)
