print("\nMODELS\n")

from src.llm import *

models = get_available_models()

print()

for model_name in models:

    print(
        get_model_details(
            model_name
        )
    )