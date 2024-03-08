# config.py

openai_config = {
    'api_key': 'YOUR_OPENAI_API_KEY',
    'max_retries': 3,
    'retry_delay': 5,
    'rate_limit_wait_time': 1.5,
    'max_tokens': 2000,
    'prompt_version': 'iris_v5',
}

claude_config = {
    'api_key': 'YOUR_CLAUDE_API_KEY',
    'model_name': 'claude-3-opus-20240229',
    'max_retries': 3,
    'retry_delay': 5,
    'max_tokens': 2048,
    'prompt_version': 'iris_v5',
}

# Add more configurations for other AI engines like Claude here

