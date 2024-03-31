import requests

# Constants for API access
API_URL = "https://guanaco-submitter.chai-research.com/endpoints/onsite/chat"
HEADERS = {"Authorization": "Bearer CR_6700b8e747434541924772becb8fa85a"}

def send_message(memory, prompt, bot_name, user_name, chat_history):
    """
    Sends a message to the chatbot API and returns the response.
    
    Parameters:
    - memory: A string representing the bot's memory of the conversation.
    - prompt: The current prompt for the bot.
    - bot_name: The name of the bot.
    - user_name: The name of the user.
    - chat_history: A list of dictionaries representing the conversation history.
    
    Returns:
    - A dictionary containing the API's response.
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
    - chat_history: A list of dictionaries representing the conversation history.
    
    Returns:
    - A string that represents the updated memory based on chat history.
    """
    memory = " | ".join(f"{item['sender']}: {item['message']}" for item in chat_history)
    return memory

def chat_loop():
    """
    Runs the main chat loop, allowing the user to interact with the bot.
    Handles user input, sends messages to the bot, and displays bot responses.
    Includes functionality to quit the chat.
    """
    # Character Information
    character = input(f"\nWho would you like to talk to? (Please enter their name): ")

    # Initial setup
    memory = ""
    prompt = f'An engaging conversation with {character}.'
    bot_name = character
    user_name = "User"
    chat_history = []

    print(f"\n{character}: Hello, I'm {character}! Ask me anything, type 'quit' to exit.")

    def is_quit_command(user_message):
        """
        Determines whether the user's message is a command to quit the chat.
        
        Parameters:
        - user_message: The message entered by the user.
        
        Returns:
        - A boolean indicating whether the command is to quit.
        """
        normalized_message = user_message.lower()
        if normalized_message in ['quit', 'q']:
            return True
        elif sorted(normalized_message) == sorted('quit'):
            while True:
                confirmation = input("Did you mean 'quit'? (type 'yes' or 'no'): ").lower()
                if confirmation in ['yes', 'y']:
                    return True
                elif confirmation in ['no', 'n']:
                    print("Returning to conversation...")
                    return False
                else:
                    print("Please enter a valid response.")
                    continue
        return False

    # Main chat loop
    while True:
        user_message = input(f'\nYou: ')
        if is_quit_command(user_message):
            break
        
        chat_history.append({"sender": user_name, "message": user_message})
        memory = update_memory(chat_history)

        response = send_message(memory, prompt, bot_name, user_name, chat_history)
        if response and "model_output" in response:
            bot_message = response["model_output"]
            print(f"\n{bot_name}: {bot_message}")
            chat_history.append({"sender": bot_name, "message": bot_message})
        else:
            print("Error: Could not retrieve bot's message.")

if __name__ == "__main__":
    chat_loop()