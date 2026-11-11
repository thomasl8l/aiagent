import os
import argparse
from openai import OpenAI
from dotenv import load_dotenv


def main():
    # Prompt the user for content
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to the LLM")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("API key not found")
    
    # Setup the client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # Create a list of messages
    messages=[
        {"role": "user", "content": args.user_prompt}
    ]
    generate_content(client, messages)


def generate_content(client: OpenAI, messages: list) -> None:
    # Create a chat and save the response
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )
    if not response.usage:
        raise RuntimeError(
            "Request has no token usage, perhaps failed"
        )

    # Print the token usage
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")
    # Print the response
    print("Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
