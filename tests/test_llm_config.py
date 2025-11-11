"""
Test LLM Provider Configuration System
========================================

Demo switching between different LLM providers.
"""

from finrobot.llm_config import LLMConfigManager

def main():
    print("\n" + "="*70)
    print("LLM Provider Configuration Test")
    print("="*70)

    # Create config manager
    mgr = LLMConfigManager()

    # Show all available providers
    mgr.list_providers()

    # Test getting active config
    print("\n📋 Current Active Configuration:")
    config = mgr.get_active_config()
    print(f"  Provider: {config['provider_name']}")
    print(f"  Model: {config['model']}")
    print(f"  Base URL: {config['base_url']}")
    print(f"  API Key: {config['api_key'][:20]}...")

    # Demo switching providers
    print("\n" + "="*70)
    print("Testing Provider Switching")
    print("="*70)

    print("\n1. Switch to OpenRouter (GPT-5):")
    mgr.set_active_provider("openrouter", "gpt-5")

    print("\n2. Switch to Aliyun (Qwen-Max):")
    mgr.set_active_provider("aliyun", "qwen-max")

    print("\n3. Switch to Aliyun (Qwen-Turbo):")
    mgr.set_active_provider("aliyun", "qwen-turbo")

    # Show final state
    print("\n" + "="*70)
    mgr.list_providers()

    print("\n✅ Configuration system working!")
    print("\nTo use in your code:")
    print("  from finrobot.llm_config import switch_provider, get_llm_config")
    print("  switch_provider('aliyun', 'qwen-max')")
    print("  config = get_llm_config()")


if __name__ == "__main__":
    main()
