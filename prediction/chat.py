import json
import random

# Load intents from intents.json
with open("intents.json", "r") as file:
    intents = json.load(file)

def get_response(user_input):
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            if user_input.lower() in pattern.lower():
                return random.choice(intent["responses"])
    return "I don't understand that."

# Test manually in the terminal
if __name__ == "__main__":
    while True:
        msg = input("You: ")
        if msg.lower() == "exit":
            break
        print("Bot:", get_response(msg))
