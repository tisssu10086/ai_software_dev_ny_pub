# Week 2 – Coding Agent & 全栈项目

本周包含两个部分：
1. 从零手写一个最小 coding agent（`coding_agent_from_scratch.py`）
2. 在 FastAPI + SQLite 应用上扩展功能，并观察 AI coding agent 的工具调用行为

---

## 环境配置

### 1. 安装 kimi-cli

```bash
uv tool install --python 3.13 kimi-cli
kimi --version
```

### 2. 在 IDE 中配置 kimi 路径

找到可执行文件路径：
```bash
uv tool dir
# 输出类似：/Users/<用户名>/.local/share/uv/tools
```

在 IDE（如 Cursor）设置中搜索 `kimi`，将 **Kimi: Executable Path** 设置为：
```
/Users/<用户名>/.local/share/uv/tools/kimi-cli/bin/kimi
```

### 3. 配置环境变量

在项目根目录的 `.env` 文件中填写：
```
KIMI_API_KEY=your_api_key_here
```

### 4. 激活虚拟环境

```bash
source .venv/bin/activate
```

---

## 启动应用

从项目根目录运行：
```bash
uv run uvicorn week2.app.main:app --reload
```

访问 http://127.0.0.1:8000

---

## 项目结构

```
week2/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── db.py                # SQLite 数据库操作
│   ├── routers/
│   │   ├── notes.py         # 笔记相关路由
│   │   └── action_items.py  # 行动项相关路由
│   └── services/
│       └── extract.py       # 行动项提取逻辑（启发式规则）
├── frontend/
│   └── index.html           # 前端页面
├── data/
│   └── app.db               # SQLite 数据库文件
├── tests/
│   └── test_extract.py      # 单元测试
├── coding_agent_from_scratch.py  # 练习1：手写 coding agent
├── llm.py                   # LLM 调用封装（Kimi / Anthropic 兼容）
└── psudo_code.md            # coding agent 流程图参考
```

---

## API 端点

### 笔记

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `/notes` | 创建笔记，body: `{"content": "..."}` |
| `GET` | `/notes/{note_id}` | 获取单条笔记 |

### 行动项

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `/action-items/extract` | 从文本提取行动项，body: `{"text": "...", "save_note": true}` |
| `GET` | `/action-items` | 获取所有行动项，可选参数 `?note_id=1` 按笔记过滤 |
| `POST` | `/action-items/{id}/done` | 标记行动项完成，body: `{"done": true}` |

---

## 运行测试

```bash
uv run pytest week2/tests/ -v
```

---

## 练习说明

详见 `assignment.md`，完成情况记录在 `writeup.md`。
