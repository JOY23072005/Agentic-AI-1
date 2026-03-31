import json

import os
from dotenv import load_dotenv

# import your modules
from llm.gemini import GeminiLLM
from tools import tool_map

# -------- SYSTEM PROMPT --------
SYSTEM_PROMPT = """
You are an AI agent.

You have access to tools:
- add(a, b) <- use this to add numbers
- multiply(a, b) <- use this to multiply numbers
- divide(a, b) <- use this to divide numbers
- current_time() <- use this to know the current time
- remember(key, value) <- use this to store user info eg - likes,dislikes,about user etc.
- recall(key) <- use this to access the stored info of user

Rules:
1. If tool is needed → respond ONLY in JSON:
{"tool": "tool_name", "args": {...}}

2. If multiple steps required:
   - Call ONE tool at a time
   - Wait for result before next step

3. Do NOT explain JSON
4. Give final answer in plain text only
"""


# -------- AGENT CLASS --------
class Agent:
    def __init__(self, llm):
        self.llm = llm
        self.max_steps = 5

    def run(self, user_input: str):
        history = [f"User: {user_input}"]

        for step in range(self.max_steps):

            prompt = SYSTEM_PROMPT + "\n" + "\n".join(history)

            response = self.llm.generate(prompt)
            text = response.strip()

            print(f"\n🧠 Step {step+1} Response:\n{text}")

            # -------- TRY TOOL --------
            try:
                data = json.loads(text)

                if "tool" in data:
                    tool_name = data["tool"]
                    args = data.get("args", {})

                    if tool_name not in tool_map:
                        print("❌ Unknown tool")
                        return

                    print(f"🔧 Tool called: {tool_name}")

                    try:
                        result = tool_map[tool_name](**args)
                    except Exception as e:
                        result = f"Error: {str(e)}"

                    print(f"📦 Tool result: {result}")

                    # store in history
                    history.append(f"Tool {tool_name} returned: {result}")
                    continue

            except:
                pass

            # -------- FINAL ANSWER --------
            print(f"\n🤖 Final Answer:\n{text}")
            return

        print("⚠️ Max steps reached")


# -------- MAIN --------
if __name__ == "__main__":
    load_dotenv()

    # print("key : ",os.getenv('GEMINI_API_KEY'))
    llm = GeminiLLM(api_key=os.getenv('GEMINI_API_KEY'))

    agent = Agent(llm)

    print("🚀 Agent Started (type 'exit' to quit)\n")
 
    while True:
        user = input("You: ")
        if user.lower() == "exit":
            break

        agent.run(user)