import asyncio
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from mcp_use import MCPAgent, MCPClient
from pydantic import SecretStr
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    # Load environment variables
    load_dotenv(override=True)

    # Create configuration dictionary
    config = {
      "mcpServers": {
        "parking-mcp": {
            "type": "stdio",
            "command": "/Users/rvmeer/git/my-mcp/env/bin/python",
            "args": [
                "parking_mcp.py"
            ]
        }
      }
    }

    # Create MCPClient from configuration dictionary
    client = MCPClient.from_dict(config)

    # Create LLM
    llm = ChatOllama(
        model="gpt-oss:20b",
        temperature=0.1,
        base_url="http://localhost:11434"
    )

    # Create agent with the client
    system_prompt = (
        "You are a parking spot reservation assistant. "
        "You can use tools to reserve and cancel parking spaces, and you can also inquire about current reservations."
        "Always determine the current date and the current user to check on the reservations."
        "As extra information you can use tools to get the current date and the email address of the current user."
    )
    agent = MCPAgent(llm=llm, client=client, max_steps=30, system_prompt=system_prompt)

    # Run the query
    #await agent.run("What is the date today?")
    #await agent.run("What is my email address?")

    messages = [
        "Who has reserved a parking spot for today? If a spot is free, please tell me, but do not make the reservation.",
        "Make a reservation for me tomorrow",
        "Show the reservations for tomorrow",
        "Cancel my reservation for tomorrow"
    ]

    for message in messages:
        result = await agent.run(message)
        logger.info(f"Result: {result}")
    
    while True:
        query = input("Enter your next query (or 'exit' to quit): ")
        if query == 'exit':
            break
        result = await agent.run(query)
        logger.info(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())