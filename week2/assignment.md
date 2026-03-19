

***建议在开始之前先阅读完整个文档。***

提示：预览此 Markdown 文件的方法：
- Mac 用户：按 `Command (⌘) + Shift + V`
- Windows/Linux 用户：按 `Ctrl + Shift + V`

# 环境配置
1. 安装kimi coding cli

```bash
uv tool install --python 3.13 kimi-cli
```

verify the version
```bash
kimi --version
```

2. 在 IDE 中配置 kimi coding cli

首先找到 kimi 可执行文件的路径：
```bash
uv tool dir
# 输出类似：/Users/<你的用户名>/.local/share/uv/tools
```

kimi 的完整路径为：
```
/Users/<你的用户名>/.local/share/uv/tools/kimi-cli/bin/kimi
```

打开设置（`Cmd + ,`），搜索 `kimi`，在 **Kimi: Executable Path** 字段中填入上述完整路径，例如：
```
/Users/<你的用户名>/.local/share/uv/tools/kimi-cli/bin/kimi
```

配置完成后重启 IDE，即可在 agent 模式下使用 kimi。


3. 激活 uv 环境：
```bash
source .venv/bin/activate
```

# 练习1 – coding agent 最小实现

完成    `week2/coding_agent_from_scratch.py` 中的TODO, 组装coding agent的最小原型，可以参考 `week2/psudo_code.md` 中的流程图。


# 练习2 - 全栈项目开发

我们将在一个简单的 FastAPI + SQLite 应用基础上进行扩展，该应用可将自由格式的笔记转换为枚举的行动项列表。



## 快速开始

### 当前应用
启动当前示例应用的步骤：

1. 从项目根目录启动服务器：
```bash
uv run uvicorn week2.app.main:app --reload
```
2. 打开浏览器，访问 http://127.0.0.1:8000/。
3. 熟悉应用的当前状态，确保可以成功输入笔记并生成提取的行动项清单。
4. 启动kimi cli, 启动命令为：
```bash
kimi --verbose	--debug
```
这样能详细输出kimi code cli 的运行中间过程， 并且把log输出到 `~/.kimi/logs/kimi.log`

在完成作业的过程中，使用 `writeup.md` 记录你的进度，包括使用的提示词以及 kimi code cli 的trace.


### TODO 1：构建新功能

分析 `week2/app/services/extract.py` 中现有的 `extract_action_items()` 函数，该函数目前使用预定义的启发式规则提取行动项。

你的任务是实现一个基于 **LLM** 的替代方案 `extract_action_items_llm()`，通过大语言模型执行行动项提取。

1. 将基于 LLM 的提取功能集成为新端点。更新前端，添加"Extract LLM"按钮，点击后通过新端点触发提取流程。

2. 暴露一个最终端点用于获取所有笔记。更新前端，添加"List Notes"按钮，点击后获取并显示所有笔记。


### TODO 2：添加单元测试

在 `week2/tests/test_extract.py` 中为 `extract_action_items_llm()` 编写单元测试，覆盖多种输入情况（例如：项目符号列表、关键词前缀行、空输入）。


### TODO 3：从代码库生成 README

***学习目标：***
*学生学习 AI 如何内省代码库并自动生成文档，展示 coding 解析代码上下文并将其转化为人类可读形式的能力。*


使用 coding agent 分析当前代码库，生成结构良好的 `README.md` 文件。README 至少应包含：
- 项目简介
- 项目配置与运行方法
- API 端点及功能说明
- 运行测试套件的说明

按照说明填写 `week2/writeup.md`，确保所有修改都在代码库中有记录。


