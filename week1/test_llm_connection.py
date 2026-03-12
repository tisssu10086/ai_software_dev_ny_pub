import sys
import os

# Ensure the current directory is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from llm import chat

def test_llm_connection():
    print("正在测试 LLM 连接...")
    
    # 1. Print current provider (Hardcoded to Kimi Code now)
    print(f"当前 LLM 提供商: Kimi Code (OpenAI 兼容)")
    print(f"Base URL: {os.getenv('KIMI_BASE_URL', 'https://api.kimi.com/coding/v1')}")
    print(f"Model: {os.getenv('KIMI_MODEL', 'kimi-for-coding')}")
    
    # 2. Check environment variables (masked)
    print("\n正在检查环境变量:")
    keys_to_check = [
        "LLM_PROVIDER",
        "AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_DEPLOYMENT",
        "KIMI_API_KEY", "MOONSHOT_API_KEY", "KIMI_MODEL",
        "OPENAI_API_KEY", "OPENAI_BASE_URL"
    ]
    
    for key in keys_to_check:
        val = os.getenv(key)
        if val:
            masked = val[:4] + "..." + val[-4:] if len(val) > 8 else "****"
            print(f"  {key}: {masked}")
        else:
            print(f"  {key}: (未设置)")

    # 3. Try a simple chat request
    print("\n正在发送测试请求...")
    try:
        messages = [{"role": "user", "content": "你好，你在工作吗？请回复 '是的，我在工作'。"}]
        response = chat(model="test-model", messages=messages, options={"temperature": 0.7})
        print(f"收到的响应:\n{response.message.content}")
        print("\n成功: LLM 连接正常工作!")
    except Exception as e:
        print(f"\n错误: 连接或获取响应失败。\n{e}")

if __name__ == "__main__":
    test_llm_connection()
