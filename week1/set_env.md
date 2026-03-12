# AI 软件开发课程 - Week 1 环境配置手册

欢迎开始你的 AI 软件开发之旅！本手册将一步步引导你完成开发环境的搭建。即使你是编程新手，只要跟随指引，也能轻松完成。

## 什么是环境配置？

简单来说，环境配置就是为我们的代码准备一个"家"。我们需要安装必要的工具（如 Python、uv）和依赖包（如 langchain、openai 等），让代码能够顺利运行。

本项目使用 **`uv`** 作为主要的管理工具，它非常快速且易于使用。

***

## 第一步：安装 uv 工具

`uv` 是一个现代化的 Python 项目管理工具，它能帮我们自动安装 Python 和各种依赖包。

### Windows 用户

打开 终端（Terminal），复制并运行以下命令：

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS / Linux 用户

打开终端（Terminal），复制并运行以下命令：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

> **提示**：安装完成后，建议关闭并重新打开终端窗口，输入 `uv --version` 检查是否安装成功。如果显示版本号（如 `uv 0.x.x`），说明安装成功！
>
> **如果提示 "找不到命令" (command not found)**，请手动配置环境路径：
>
>  - **Windows 用户**：
>     ```powershell
>     $env:PATH="$HOME\.local\bin;$env:PATH"
>     ``` 
> - **macOS / Linux 用户**：
>   - **macOS 用户**（默认使用 Zsh）：
>     ```bash
>     echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
>     source ~/.zshrc
>     ```
>   - **Linux 用户**（通常使用 Bash）：
>     ```bash
>     echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
>     source ~/.bashrc
>     ```

***

## 第二步：获取项目代码

如果你已经下载了解压缩包或通过 Git 克隆了代码，请在终端中进入项目文件夹：

```bash
cd ai_software_dev_ny_pub
```

***

## 第三步：一键初始化环境

在项目根目录下，我们只需要运行两条命令即可完成所有准备工作。

1. **创建虚拟环境**（相当于给项目建一个独立房间，互不干扰）：
   ```bash
   uv venv
   ```
   *运行后你会看到提示：Creating virtual environment at: .venv*
2. **安装依赖包**（把代码需要的工具都搬进房间）：
   ```bash
   uv pip install -r requirements.txt
   ```
   *这一步可能需要几十秒，取决于你的网速。看到 "Successfully installed..." 即表示完成。*

***

## 第四步：配置 API 密钥

我们的代码需要调用大模型（LLM）的能力，因此需要配置 API 密钥。

1. 在项目根目录下，找到名为 `.env` 的文件（如果没有，请新建一个）。
2. 使用文本编辑器打开它，填入你的密钥信息：

```env
# 示例配置（请替换为你自己的 Key）
KIMI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
KIMI_BASE_URL=https://api.kimi.com/coding/
```

> **注意**：`.env` 文件包含敏感信息，请勿将其分享给他人或上传到公开网络。

***

## 第五步：验证环境

最后，让我们运行一个测试脚本，确保一切正常工作。

在终端运行：

```bash
uv run python week1/test_llm_connection.py
```

### 预期结果

如果你看到类似以下的输出，恭喜你，环境配置成功！🎉

```text
Testing LLM connection...
Current LLM Provider: Kimi Code (OpenAI Compatible)
...
Response received:
Yes, I am working.

SUCCESS: LLM connection is working!
```

***

## 常见问题 (FAQ)

**Q: 运行** **`uv`** **命令提示找不到命令？**
A: 请确保安装 `uv` 后重启了终端窗口。如果仍然不行，请检查是否将其添加到了系统环境变量中。

**Q: 安装依赖时速度很慢或失败？**
A: 这可能是网络问题。你可以尝试切换网络，或者配置国内镜像源。

**Q: 测试脚本报错 "Authentication failed"？**
A: 请检查 `.env` 文件中的 API Key 是否正确，注意不要有多余的空格。
