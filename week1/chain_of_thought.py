import os
import re
from dotenv import load_dotenv
from llm import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# TODO: Fill this in!
YOUR_SYSTEM_PROMPT = ""


# USER_PROMPT = """
# Solve this problem, then give the final answer on the last line as "Answer: <number>".

# what is 3^{12345} (mod 100)?
# """

# # For this simple example, we expect the final numeric answer only
# EXPECTED_OUTPUT = "Answer: 43"


USER_PROMPT = """
解决这个问题，然后在最后一行给出最终答案，格式为 "Answer: <number>"。

1.10 和 1.9 谁更大?
"""

# For this simple example, we expect the final numeric answer only
EXPECTED_OUTPUT = "Answer: 1.9"


def extract_final_answer(text: str) -> str:
    """从详细的推理轨迹中提取最后的 'Answer: ...' 行。

    - 查找以 'Answer:' 开头的最后一行（不区分大小写）
    - 当存在数字时，规范化为 'Answer: <number>'
    - 如果未检测到数字，则回退到返回匹配的内容
    """
    matches = re.findall(r"(?mi)^\s*answer\s*:\s*(.+)\s*$", text)
    if matches:
        value = matches[-1].strip()
        # Prefer a numeric normalization when possible (supports integers/decimals)
        num_match = re.search(r"-?\d+(?:\.\d+)?", value.replace(",", ""))
        if num_match:
            return f"Answer: {num_match.group(0)}"
        return f"Answer: {value}"
    return text.strip()



def test_your_prompt(system_prompt: str) -> bool:
    """运行最多 NUM_RUNS_TIMES 次，如果任何输出匹配 EXPECTED_OUTPUT 则返回 True。

    找到匹配项且推理有效时打印 "SUCCESS"。
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"正在运行第 {idx + 1} 次测试，共 {NUM_RUNS_TIMES} 次")
        response = chat(
            model="kimi-k2.5", # Ensure we use a capable model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.3},
        )
        output_text = response.message.content
        print(output_text)
        
        # 2. Check final answer
        final_answer = extract_final_answer(output_text)
        if final_answer.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"预期输出: {EXPECTED_OUTPUT}")
            print(f"实际输出: {final_answer}")
    return False


if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)

