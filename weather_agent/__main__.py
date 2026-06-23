from dotenv import load_dotenv
import json
import ollama
import requests
from openai import OpenAI

load_dotenv()

client = OpenAI()

def weather_tool(query: str) -> str:
    response = requests.get(f"https://wttr.in/{query}?format=3")

    return response.text

SYSTEM_PROMPT = """
    You're an expert AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.
    You can also call a tool if required from the list of available tools.
    for every tool call wait for the observe step which is the output from the called tool.

    Rules:
    - Strictly Follow the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to the displayed to the user).

    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string", "tool": "string", "input": "string" }

    Available Tools:
    - get_weather(city: str): Takes city name as an input string and returns the weather info about the city.
    - run_command(cmd: str): Takes a system linux command as string and executes the command on user's system and returns the output from that command
    
    Example 1:
    START: Hey, Can you solve 2 + 3 * 5 / 10
    PLAN: { "step": "PLAN": "content": "Seems like user is interested in math problem" }
    PLAN: { "step": "PLAN": "content": "looking at the problem, we should solve this using BODMAS method" }
    PLAN: { "step": "PLAN": "content": "Yes, The BODMAS is correct thing to be done here" }
    PLAN: { "step": "PLAN": "content": "first we must multiply 3 * 5 which is 15" }
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 15 / 10" }
    PLAN: { "step": "PLAN": "content": "We must perform divide that is 15 / 10  = 1.5" }
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 1.5" }
    PLAN: { "step": "PLAN": "content": "Now finally lets perform the add 3.5" }
    PLAN: { "step": "PLAN": "content": "Great, we have solved and finally left with 3.5 as ans" }
    OUTPUT: { "step": "OUTPUT": "content": "3.5" }

    Example 2:
    START: What is the weather of Delhi?
    PLAN: { "step": "PLAN": "content": "Seems like user is interested in getting weather of Delhi in India" }
    PLAN: { "step": "PLAN": "content": "Lets see if we have any available tool from the list of available tools" }
    PLAN: { "step": "PLAN": "content": "Great, we have get_weather tool available for this query." }
    PLAN: { "step": "PLAN": "content": "I need to call get_weather tool for delhi as input for city" }
    PLAN: { "step": "TOOL": "tool": "get_weather", "input": "delhi" }
    PLAN: { "step": "OBSERVE": "tool": "get_weather", "output": "The temp of delhi is cloudy with 20 C" }
    PLAN: { "step": "PLAN": "content": "Great, I got the weather info about delhi" }
    OUTPUT: { "step": "OUTPUT": "content": "The cuurent weather in delhi is 20 C with some cloudy sky." }
    
"""

available_tools = {
    "get_weather": weather_tool
}

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

if  __name__ == "__main__":
    print(weather_tool("faridabad"))
    query = input("> ")

    messages.append({
        "role": "user",
        "content": query
    })

    while True:
        try:
            #response = ollama.chat(
            #    model="deepseek-r1:1.5b", 
            #    messages=messages,
            #    tools=[weather_tool]
            #)
            response = client.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                messages=messages
            )
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            break

        # raw_response = response.message.content
        raw_response = response.choices[0].message.content
        messages.append({
            "role": "assistant",
            "content": raw_response
        })

        #print(f"Raw Response: {raw_response}")

        parsed_response = json.loads(raw_response)

        #print(f"Parsed Response: {parsed_response}")

        if parsed_response["step"] == "OUTPUT":
            print(parsed_response["content"])
            break
        if parsed_response["step"] == "START":
            print(parsed_response["content"])
            continue
        if parsed_response["step"] == "PLAN":
            print(parsed_response["content"])
            continue
        if parsed_response["step"] == "TOOL":
            tool_name = parsed_response["tool"]
            tool_input = parsed_response["input"]
            
            if tool_name in available_tools:
                tool_response = available_tools[tool_name](tool_input)
                messages.append({
                    "role": "developer",
                    "content": json.dumps({
                        "step": "OBSERVE",
                        "tool": tool_name,
                        "output": tool_response
                    })
                })
        #print(response.message.content)


