import os
from dotenv import load_dotenv
import argparse
import json
from openai import OpenAI

from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get('OPENROUTER_API_KEY')
if api_key is None:
    raise RuntimeError('API key not found!')

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

def generate_content(client, messages):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions
    )
    if response is None:
        raise RuntimeError("No valid response received!")
    return response

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

for _ in range(20):

    # call the model, handle responses, etc.
    response = generate_content(client, messages)
    message = response.choices[0].message
    if args.verbose:
        print(f"ASSISTANT -> {message.content}")
    messages.append(message)

    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            messages.append(result_message)
            if args.verbose:
                print(f"TOOL CALL -> {result_message['content']}")
        continue
    else:
        print(message.content)
        break
    
    print("Max. number of iterations reached!!!")
    exit(1)

#if args.verbose:
#    print(f'User prompt: {args.user_prompt}')
#    print(f'Prompt tokens: {response.usage.prompt_tokens}')
#    print(f'Response tokens: {response.usage.completion_tokens}')
#    print('Response:')
#print(message.content)
