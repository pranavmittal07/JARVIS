from groq import Groq
from json import load, dump
import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve environment variables
username = os.getenv("USERNAME")
assistant_name = os.getenv("ASSISTANT_NAME")
Groq_API_KEY = os.getenv("GROQ_API_KEY")

# Check if essential variables are set
if not all([username, assistant_name, Groq_API_KEY]):
    raise ValueError("Ensure USERNAME, ASSISTANT_NAME, and GROQ_API_KEY are set in the .env file.")

# Initialize Groq client
client = Groq(api_key=Groq_API_KEY)

# Set the system prompt
system_prompt = f"""
Hello, I am {username}. You are a very accurate and advanced AI chatbot named {assistant_name}.
*** Do not tell time unless I ask. Reply concisely. ***
*** Always reply in English, regardless of the question's language. ***
*** Do not include notes or mention your training data in responses. ***
"""

system_chat = [{"role": "system", "content": system_prompt}]

# Define the path for the chat log
chatlog_directory = "Data"
chatlog_path = os.path.join(chatlog_directory, "Chatlog.json")

# Ensure the directory exists
if not os.path.exists(chatlog_directory):
    os.makedirs(chatlog_directory)


def real_time_information():
    """Generate real-time information for context."""
    current_date_time = datetime.datetime.now()
    return (
        f"Please use this real-time information if needed:\n"
        f"Day: {current_date_time.strftime('%A')}\n"
        f"Date: {current_date_time.strftime('%d')}\n"
        f"Month: {current_date_time.strftime('%B')}\n"
        f"Year: {current_date_time.strftime('%Y')}\n"
        f"Time: {current_date_time.strftime('%H:%M:%S')}.\n"
    )


def load_chatlog():
    """Load the chat log from a JSON file."""
    if not os.path.exists(chatlog_path):
        with open(chatlog_path, "w") as f:
            dump([], f)
    with open(chatlog_path, "r") as f:
        return load(f)


def save_chatlog(messages):
    """Save the chat log to a JSON file."""
    with open(chatlog_path, "w") as f:
        dump(messages, f, indent=4)


def answer_modifier(answer):
    """Clean and format the AI's response."""
    lines = answer.split("\n")
    return "\n".join(line.strip() for line in lines if line.strip())


def chatbot(query):
    """Process user input and return a response."""
    try:
        # Load chat log
        messages = load_chatlog()

        # Append user query to the messages
        messages.append({"role": "user", "content": query})

        # Generate a response from the Groq client
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=system_chat + [{"role": "user", "content": real_time_information()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
        )

        # Collect AI response
        answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content

        # Clean and validate the AI's response
        answer = answer.replace("</s>", "").strip()
        if not answer:
            return "I'm sorry, I couldn't generate a response. Please try again."

        # Save the chat log with the assistant's response
        messages.append({"role": "assistant", "content": answer})
        save_chatlog(messages)

        # Return the formatted answer
        return answer_modifier(answer)

    except Exception as e:
        # Handle errors and reset the chat log
        save_chatlog([])  # Clear chatlog to avoid corrupted logs
        return f"An error occurred: {str(e)}. Please try again."




if __name__ == "__main__":
    print(f"Chatbot {assistant_name} is ready! Type 'exit' to end the session.")
    while True:
        user_input = input("Enter your question: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        print(chatbot(user_input))