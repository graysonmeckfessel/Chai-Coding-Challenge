import requests

# Constants for API access
API_URL = "https://guanaco-submitter.chai-research.com/endpoints/onsite/chat"
HEADERS = {"Authorization": "Bearer CR_6700b8e747434541924772becb8fa85a"}

def send_message(memory, prompt, bot_name, user_name, chat_history):
    """
    Sends a message to the chatbot API and returns the response.

    Parameters:
    memory (str): The bot's memory of the conversation.
    prompt (str): The current prompt for the bot.
    bot_name (str): The name of the bot.
    user_name (str): The name of the user.
    chat_history (list): A list of dictionaries representing the conversation history.

    Returns:
    dict: The response from the API.
    """
    payload = {
        "memory": memory,
        "prompt": prompt,
        "bot_name": bot_name,
        "user_name": user_name,
        "chat_history": chat_history
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

def update_memory(chat_history):
    """
    Updates the memory string based on the entire chat history.

    Parameters:
    chat_history (list): A list of dictionaries representing the conversation history.

    Returns:
    str: A string that represents the updated memory based on chat history.
    """
    memory = " | ".join(f"{item['sender']}: {item['message']}" for item in chat_history)
    return memory

def chat_loop(bot1_name, bot2_name, initial_topic):
    """
    The main chat loop allowing two AI bots to interact based on an initial topic.

    Parameters:
    bot1_name (str): Name of the first bot.
    bot2_name (str): Name of the second bot.
    initial_topic (str): The initial topic of conversation.
    """
    
    memory = initial_topic
    prompt = initial_topic
    chat_history = []

    # Max exchanges chosen to mirror max exchanges on Chai App
    max_exchanges = 70
    exchanges = 0

    while exchanges < max_exchanges:
        # Prepare the message for Bot1 or Bot2
        sender_name, receiver_name = (bot1_name, bot2_name) if exchanges % 2 == 0 else (bot2_name, bot1_name)
        response = send_message(memory, prompt, sender_name, receiver_name, chat_history)
        if response and "model_output" in response:
            bot_message = response["model_output"]
            print(f"\n{sender_name}: {bot_message}")
            chat_history.append({"sender": sender_name, "message": bot_message})
            memory = update_memory(chat_history)  # Update memory after each exchange
        else:
            print(f"Error: Could not retrieve {sender_name}'s message.")
            break

        exchanges += 1

if __name__ == "__main__":
    bot1_name = input(f"\nWelcome to the chatroom! (Type 'ctrl c' to quit)\n\nPlease enter the name of the first character: ")
    bot2_name = input("Please enter the name of the second character: ")
    initial_topic = input("What would you like them to talk about?: ")
    chat_loop(bot1_name, bot2_name, initial_topic)