import boto3
from urllib.parse import quote_plus
from typing import Union
from src.repository.error_repository import ErrorRepository
from src.models.model import OrderDetails,MenuDetails,ChatResponse,OffContext,OtherResponse
from langchain.agents.structured_output import ToolStrategy
from langchain_aws import ChatBedrock
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from settings import settings
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langchain_core.runnables import RunnableConfig
from src.agent.prompts import SYSTEM_PROMPT
from src.utils.exceptions.custom_app_exception import AppBaseException
from src.utils.exceptions.error_codes import ErrorCode, ErrorCodeStatus
from langchain.agents.middleware.summarization import SummarizationMiddleware

Response_type=Union[OrderDetails,MenuDetails,OffContext]
error=ErrorRepository()

async def get_llm(max_tokens=2000,temperature=0.3) -> ChatBedrock:
    client = boto3.client(
        service_name="bedrock-runtime",
        region_name=settings.aws_region,
    )
    return ChatBedrock(
        client=client,
        model_id=settings.model_id,
        provider=settings.provider,
        model_kwargs={
            "max_tokens": max_tokens,
            "temperature": temperature,
        },
    )

def _get_db_uri() -> str:
    encoded_password = quote_plus(settings.db_password)
    return (
        f"postgresql://{settings.db_username}:{encoded_password}"
        f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    )



async def _detect_intent(message: str) -> dict:
    """
    Detect what the user is asking and return
    only the resources and prompts needed.

    Returns:
        {
            "load_menu": bool,
            "load_shop_info": bool,
            "prompt": {
                "prompt_name": str,
                "arguments": dict
            } | None
        }
    """
    msg = message.lower().strip()

    load_menu = any(w in msg for w in [
        "menu", "drink", "coffee", "price",
        "espresso", "cappuccino", "latte",
        "mocha", "cold brew", "matcha",
        "available", "what do you have",
        "what can i order", "how much",
        "recommend", "suggest"
    ])

    load_shop_info = any(w in msg for w in [
        "shop", "address", "location", "where",
        "timing", "hours", "open", "close",
        "contact", "phone", "email", "whatsapp",
        "parking", "wifi", "facility", "payment",
        "how to reach", "directions", "instagram",
        "social media", "about the shop"
    ])

    prompt = None

    if any(w in msg for w in [
        "caffeine", "strong coffee", "strong drink",
        "low caffeine", "decaf", "energise", "energy",
        "keep me awake", "mild", "gentle", "light coffee"
    ]):

        caffeine_level = "medium"
        if any(w in msg for w in [
            "high", "strong", "energise",
            "energy", "keep me awake"
        ]):
            caffeine_level = "high"
        elif any(w in msg for w in [
            "low", "less", "decaf",
            "mild", "gentle", "light"
        ]):
            caffeine_level = "low"
        prompt = {
            "prompt_name": "prompt://bean-and-brew/caffeine-guide",
            "arguments": {
                "caffeine_level": caffeine_level
            }
        }
  
    elif any(w in msg for w in [
        "recommend", "suggest", "something",
        "what should i", "i want something",
        "i feel like", "i am looking for",
        "sweet", "cold", "hot", "strong",
        "light", "refreshing", "creamy"
    ]):

        preference = "good"  # default
        if any(w in msg for w in ["sweet", "sugary"]):
            preference = "sweet"
        elif any(w in msg for w in ["cold", "iced", "chilled"]):
            preference = "cold"
        elif any(w in msg for w in ["hot", "warm"]):
            preference = "hot"
        elif any(w in msg for w in ["strong", "bold"]):
            preference = "strong"
        elif any(w in msg for w in ["light", "mild", "gentle"]):
            preference = "light"
        elif any(w in msg for w in ["creamy", "smooth"]):
            preference = "creamy"
        elif any(w in msg for w in ["refreshing"]):
            preference = "refreshing"

        prompt = {
            "prompt_name": "prompt://recommend-drink",
            "arguments": {"preference": preference}
        }
 
    return {
        "load_menu": load_menu,
        "load_shop_info": load_shop_info,
        "prompt": prompt
    }


async def run_agent(message: str,thread_id:str = "default") -> dict:
    try:
        mcp_client= MultiServerMCPClient({
            "bean and brew":{
                "url":settings.mcp_server_url,
                "transport":"streamable-http"
                }})

        intent = await _detect_intent(message)
        print(f"\n[Intent] {intent}")

 
        tools = await mcp_client.get_tools()

        prompt_messages=[]
        prompt_context = ""
        if intent["prompt"]:
            prompt_messages = await mcp_client.get_prompt(
                server_name="bean and brew",
                prompt_name=intent["prompt"]["prompt_name"],
                arguments=intent["prompt"]["arguments"]
            )
            print(
                f"\n[Prompt] Loaded "
                f"{len(prompt_messages)} message(s):"
            )
            for msg in prompt_messages:
                print(
                    f"  [{msg.type.upper()}] "
                    f"{msg.content[:100]}..."
                )
            if prompt_messages:
                prompt_context = (
                    f"\nPrompt Guidance:\n"
                    f"{prompt_messages[0].content}"
                )


        resource_context = ""

        if intent["load_menu"]:
            menu_blobs = await mcp_client.get_resources(
                server_name='bean and brew',
                uris="menu://items"
            )
            print(f"\n[Resource] Loaded menu resource")
            for blob in menu_blobs:
                try:
                    text = blob.as_bytes().decode(
                        "utf-8", errors="replace"
                    )
                    uri = blob.metadata.get(
                        "uri", "menu"
                    )
                    resource_context += (
                        f"\n[{uri}]\n{text}\n"
                    )
                except Exception:
                    continue

        if intent["load_shop_info"]:
            shop_blobs = await mcp_client.get_resources(
                server_name="bean and brew",
                uris="resource://shop-info"
            )
            print(f"\n[Resource] Loaded shop-info resource")
            for blob in shop_blobs:
                try:
                    text = blob.as_bytes().decode(
                        "utf-8", errors="replace"
                    )
                    uri = blob.metadata.get(
                        "uri", "shop-info"
                    )
                    resource_context += (
                        f"\n[{uri}]\n{text}\n"
                    )
                except Exception:
                    continue

        summarizer=SummarizationMiddleware(
            model=await get_llm(max_tokens=3000,temperature=0),
            trigger=("messages",10),
            keep=("messages",4)
        )

        async with AsyncPostgresSaver.from_conn_string(_get_db_uri()) as checkpointer:
            await checkpointer.setup()

            system_text = prompt_messages[0].content if prompt_messages else ""

            if resource_context:
                system_text += f"\n\nHere is the available context:\n{resource_context}"

            llm = await get_llm()
            agent = create_agent(
            model=llm,
            tools=tools,
            middleware=[summarizer],
            checkpointer=checkpointer,
            system_prompt=SystemMessage(content=SYSTEM_PROMPT),
            response_format=ToolStrategy(Response_type),
            )

            context_parts = []
            if resource_context:
                context_parts.append(resource_context)
            if prompt_context:
                context_parts.append(prompt_context)
            
            message_with_context = (
                "\n".join(context_parts)
                + f"\n\nUser Message:\n{message}"
            )

            config = RunnableConfig(
                        configurable={"thread_id": thread_id}
                    )

            result = await agent.ainvoke({
                "messages": [
                    HumanMessage(content=message_with_context),
                ]
            },config)
           
            print(result)
            return result

    except AppBaseException:
        raise
    except Exception as exc:
        raise AppBaseException(
            error_code=ErrorCodeStatus.get(
                ErrorCode.AGENT_INVOKE_FAILED, "BB_AGENT_001"
            ),
            message=f"Agent invocation failed: {str(exc)}",
            status_code=500,
        )

