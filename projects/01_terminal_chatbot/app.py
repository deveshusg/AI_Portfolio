from src.llm import ask_llm


def main():

    print("\nTerminal Chatbot Started")
    print("Type 'quit' to exit.\n")

    while True:

        user_question = input("You: ")

        if user_question.lower() == "quit":
            print("\nGoodbye!")
            break

        response = ask_llm(user_question)

        print(f"\nBot: {response}\n")


if __name__ == "__main__":
    main()