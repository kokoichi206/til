import openai
import json

def get_current_weather(location, unit="celsius"):
    weather_info = {
        "location": location,
        "temperature": 20,
        "unit": unit,
        "forecast": ["sunny", "windy", "cloudy"],
    }
    return json.dumps(weather_info)

functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location to get the weather for.",
                },
                "unit": {
                    "type": "string",
                    "description": "The unit to get the temperature in.",
                    "enum": ["celsius", "fahrenheit"],
                },
            },
            "required": ["location"],
        }
    },
]

messages = [
    {"role": "user", "content": "What's the weather like in New York?"},
]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    functions=functions,
)

# content = null, function_call が返ってくる。
#
# {
#   "id": "chatcmpl-8Hth7jPnRhO1nulRTNW01ifgqpgwc",
#   "object": "chat.completion",
#   "created": 1699276357,
#   "model": "gpt-3.5-turbo-0613",
#   "choices": [
#     {
#       "index": 0,
#       "message": {
#         "role": "assistant",
#         "content": null,
#         "function_call": {
#           "name": "get_current_weather",
#           "arguments": "{\n  \"location\": \"New York\",\n  \"unit\": \"celsius\"\n}"
#         }
#       },
#       "finish_reason": "function_call"
#     }
#   ],
#   "usage": {
#     "prompt_tokens": 87,
#     "completion_tokens": 25,
#     "total_tokens": 112
#   }
# }
print(response)

response_message = response["choices"][0]["message"]

available_functions = {
    "get_current_weather": get_current_weather,
}

function_name = response_message["function_call"]["name"]
function_to_call = available_functions[function_name]
function_arguments = json.loads(response_message["function_call"]["arguments"])

function_response = function_to_call(
    location=function_arguments.get("location"),
    unit=function_arguments.get("unit"),
)
print(function_response)

messages.append(response_message)
# role = function として追加。
messages.append(
    {
        "role": "function",
        "name": function_name,
        "content": function_response,
    }
)

second_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    functions=functions,
)

print(second_response)
