from google import genai
from dotenv import load_dotenv
import os

from product_tools import search_products, check_product_details


def create_agent():

    load_dotenv()

    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    chat = client.chats.create(
        model="gemini-3.1-flash-lite",
        config={
            "tools": [
                search_products,
                check_product_details
            ],
            "system_instruction": """
            You are an AI shopping assistant.
            
            You have access to a product database through tools.

            IMPORTANT RULES:

            1. Always use the available tools when answering
               questions about products.

            2. Product information must come ONLY from tool results.

            3. Never invent or assume product names, prices, ratings,
               discounts, specifications, or links.

            4. If the user asks about a specific product:
               - First use search_products if you do not know its product ID.
               - Then use check_product_details for complete details.

            5. If the requested information is not available in the
               tool results, clearly say that the information is not available.

            6. Do not use general knowledge to fill missing product information.

            7. For recommendations, recommend ONLY products returned
               by the product search tool.

            8. Use previous conversation context only to understand
               what the user is referring to. Always verify product
               information using the tools.
            """


        }
    )

    return client, chat


# Allows agent.py to still work from the terminal
if __name__ == "__main__":

    chat = create_agent()

    print("\n========== AI SHOPPING AGENT ==========")
    print("Type 'exit' to quit.\n")

    while True:

        user_query = input("You: ")

        if user_query.lower() == "exit":
            print("Goodbye!")
            break

        response = chat.send_message(user_query)

        print("\nAgent:", response.text)
        print()