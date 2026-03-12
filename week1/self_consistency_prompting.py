import os
import re
from collections import Counter
from dotenv import load_dotenv
from llm import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# TODO: Fill this in! Try to get as close to 100% correctness across all runs as possible.
YOUR_SYSTEM_PROMPT = ""

# USER_PROMPT = """
# Solve this problem, then give the final answer on the last line as "Answer: <number>".

# Henry made two stops during his 60-mile bike trip. He first stopped after 20
# miles. His second stop was 15 miles before the end of the trip. How many miles
# did he travel between his first and second stops?
# """

USER_PROMPT = """
解决这个问题，然后在最后一行给出最终答案，格式为 "Answer: <number>"。

球面上取五个点，它们处在同一个半球面的概率是多少？
"""

EXPECTED_OUTPUT = "Answer: 0.6875"


def extract_final_answer(text: str) -> str:
    """从详细的推理轨迹中提取最后的 'Answer: ...' 行。

    - 查找以 'Answer:' 开头的最后一行（不区分大小写）
    - 当存在数字时，规范化为 'Answer: <number>'
    - 如果未检测到数字，则回退到返回匹配的内容
    """
    matches = re.findall(r"(?mi)^\s*answer\s*:\s*(.+)\s*$", text)
    if matches:
        value = matches[-1].strip()
        num_match = re.search(r"-?\d+(?:\.\d+)?", value.replace(",", ""))
        if num_match:
            return f"Answer: {num_match.group(0)}"
        return f"Answer: {value}"
    return text.strip()


def test_your_prompt(system_prompt: str) -> bool:
    """运行提示词 NUM_RUNS_TIMES 次，对提取的 'Answer: ...' 行进行多数投票。

    如果多数答案等于 EXPECTED_OUTPUT，则打印 "SUCCESS"。
    """
    answers: list[str] = []
    for idx in range(NUM_RUNS_TIMES):
        print(f"正在运行第 {idx + 1} 次测试，共 {NUM_RUNS_TIMES} 次")
        response = chat(
            model="test-model",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 1},
        )
        output_text = response.message.content
        # print(output_text)
        final_answer = extract_final_answer(output_text)
        print(f"第 {idx + 1} 次运行的答案: {final_answer}")
        answers.append(final_answer.strip())

    if not answers:
        print("未产生任何答案。")
        return False

    counts = Counter(answers)
    majority_answer, majority_count = counts.most_common(1)[0]
    print(f"多数答案: {majority_answer} ({majority_count}/{len(answers)})")

    if majority_answer.strip() == EXPECTED_OUTPUT.strip():
        print("SUCCESS")
        return True

    # Print distribution for debugging when majority does not match expected
    print(f"预期输出: {EXPECTED_OUTPUT}")
    print("答案分布:")
    for answer, count in counts.most_common():
        print(f"  {answer}: {count}")
    return False


if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)

