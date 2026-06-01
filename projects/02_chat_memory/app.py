from src.llm import ask_llm
from src.prompts import SYSTEM_PROMPT


def main():

    print("\nMemory Chatbot Started")
    print("Type 'quit' to exit.\n")

    conversation_history = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    while True:

        user_question = input("You: ")

        if user_question.lower() == "quit":
            print("\nGoodbye!")
            break

        conversation_history.append(
            {
                "role": "user",
                "content": user_question
            }
        )

        response = ask_llm(conversation_history)

        conversation_history.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        print(f"\nBot: {response}\n")


if __name__ == "__main__":
    main()