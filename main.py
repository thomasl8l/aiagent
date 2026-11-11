import os
import argparse
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")


def main():
    print("Hello from aiagent!")
    if not api_key:
        raise RuntimeError("API key not found")
    
    # Setup the client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # Prompt the user for content
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    # Create a list of messages
    messages=[
        {"role": "user", "content": args.user_prompt}
    ]

    # Create a chat and save the response
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    # Print the token usage
    if not response.usage:
        raise RuntimeError(
            "Request has no token usage, perhaps failed"
        )
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")
    # Print the response
    print("Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
