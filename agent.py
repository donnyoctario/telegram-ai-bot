from groq import Groq

import os
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_ai(prompt):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are a smart assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def agent(user_input):
    if "sql" in user_input.lower():
        return ask_ai("Buat SQL query: " + user_input)
    elif "email" in user_input.lower():
        return ask_ai("Buat email profesional: " + user_input)
    elif "prd" in user_input.lower():
        return ask_ai("Buat PRD lengkap: " + user_input)
    else:
        return ask_ai(user_input)

while True:
    user_input = input("\nKamu: ")
    if user_input.lower() == "exit":
        break
    print("\nAI:", agent(user_input))