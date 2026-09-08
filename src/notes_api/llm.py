import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()          # reads ANTHROPIC_API_KEY from the environment

MODEL = "claude-haiku-4-5-20251001"   # cheapest + fastest; right choice while learning

def ask(question: str) -> str:

    message = client.messages.create(
        model=MODEL, max_tokens=1024,
        messages=[{"role": "user", "content": question}],
    )
    print(message.content)  # a LIST of content blocks, not a string
    print(message.content[0].text)
    print(message.stop_reason)  # "end_turn" | "max_tokens" | "stop_sequence" | "tool_use"
    print(message.usage)
    if message.stop_reason == "max_tokens":
        raise ValueError("The provided query exceed max token.")
    return message.content[0].text

if __name__ == "__main__":
    print(ask("In two sentences: what is a token in an LLM?"))