import os
import argparse
from openai import OpenAI
from dotenv import load_dotenv
from prompts import system_prompt


def main():
    # Prompt the user for content
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
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
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt}
    ]
    generate_content(client, messages, args)


def generate_content(client: OpenAI, messages: list, args: object) -> None:
    # Create a chat and save the response
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
    )
    if not response.usage:
        raise RuntimeError(
            "Request has no token usage, perhaps failed"
        )

    # Optionally print details of response
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    # Print the response
    print("Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
