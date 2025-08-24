from agno.agent import Agent
from agno.embedder.google import GeminiEmbedder
from agno.knowledge.json import JSONKnowledgeBase
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
from agno.vectordb.pgvector import PgVector

from db.connection import db_url
import os

def create_knowledge(path_data: str, table_name: str):
    return JSONKnowledgeBase(
        path=path_data,
        vector_db=PgVector(
            table_name=table_name,
            db_url=db_url,
            embedder=GeminiEmbedder()
        )
    )

def create_waiter_agent():
    menu_knowledge = create_knowledge("data/products.json", "menu_kb")

    waiter_agent = Agent(
        name="Virtual Waiter",
        agent_id="waiter_agent",
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GOOGLE_API_KEY")),
        tools=[ReasoningTools(add_instructions=True)],
        knowledge=menu_knowledge,
        search_knowledge=True,
        description="A refined virtual waiter that assists users in finding dishes on the menu.",
        instructions=[
            "You are a virtual waiter specialized in recommending menu dishes.",
            "IMPORTANT: Before querying the database, ask the user the following step-by-step questions:",
            "1. Desired dish type (starter, main course, dessert, drink)",
            "2. Allergies or dietary restrictions",
            "3. Dietary preferences (vegetarian, vegan)",
            "4. Serving for individual or group",
            "5. Preferred dish style (light, creamy, pasta, refreshing)",
            "6. Suggested accompanying drink",
            "ONLY after collecting this information, consult:",
            "- Your knowledge base for semantic recommendations",
            "- The `products` database for precise information",
            "Use a polite and refined tone, like a professional waiter.",
            "Present: name, description, price, allergens, and portions naturally.",
            "Maximum of 3 suggestions per query.",
            "Always include the price in the answer in reais R$",
            "ALWAYS RESPOND IN THE SAME LANGUAGE THE USER USED.",
        ],
        reasoning=True,
        add_history_to_messages=True,
        num_history_runs=5,
        read_chat_history=True,
        show_tool_calls=True,
        markdown=True,
    )

    menu_knowledge.load(recreate=False)
    return waiter_agent
