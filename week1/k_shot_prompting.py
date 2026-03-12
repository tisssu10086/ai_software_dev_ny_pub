import os
from dotenv import load_dotenv
from llm import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# TODO: Fill this in!
YOUR_SYSTEM_PROMPT = ''' 
''' 

USER_PROMPT = """
将以下单词的字母顺序反转。

httpstatus
"""


EXPECTED_OUTPUT = "sutatsptth"

def test_your_prompt(system_prompt: str) -> bool:
    """运行提示词最多 NUM_RUNS_TIMES 次，如果任何输出匹配 EXPECTED_OUTPUT 则返回 True。

    找到匹配项时打印 "SUCCESS"。
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"正在运行第 {idx + 1} 次测试，共 {NUM_RUNS_TIMES} 次")
        response = chat(
            model="test-model",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.5},
        )
        output_text = response.message.content.strip()
        print(output_text)
        if output_text.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"预期输出: {EXPECTED_OUTPUT}")
            print(f"实际输出: {output_text}")
    return False

if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)
