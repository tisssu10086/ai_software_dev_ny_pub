# 第一周 — 提示工程技术

你将通过编写提示词来完成特定任务，练习多种提示工程技术。每个任务的说明都位于相应源文件的顶部。

## 安装
确认你完成了 `set_env.md` 中的环境配置。

## 技术和源文件
- K-shot 提示 (K-shot prompting) — `week1/k_shot_prompting.py`
- 思维链 (Chain-of-thought) — `week1/chain_of_thought.py`
- 工具调用 (Tool calling) — `week1/tool_calling.py`
- 自我一致性提示 (Self-consistency prompting) — `week1/self_consistency_prompting.py`
- RAG (检索增强生成) — `week1/rag.py`
- 反思 (Reflexion) — `week1/reflexion.py`

## 交付成果
- 阅读每个文件中的任务描述。
- 设计并运行提示词（寻找代码中标注 `TODO` 的所有位置）。这应该是你需要更改的唯一内容（即不要修改模型逻辑）。
- 迭代改进结果，直到测试脚本通过。
- 保存每种技术的最终提示词和输出。
- ***仔细检查所有 `TODO` 是否都已解决。***
