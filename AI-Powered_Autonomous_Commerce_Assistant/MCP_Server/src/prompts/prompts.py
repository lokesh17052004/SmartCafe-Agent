from src.router.mcp_router import router
from typing import List
@router.prompt("prompt://recommend-drink")
def recommended_drink(preference:str) ->str:
    """
    Returns a prompt to recommend a drink based on the customer's preference 
    -e.g. strong,sweet,cold,hot,light
    Use this when the user asks for the recommendation
    """
    return (f"The customer is looking for something{preference}."
            f"Based on the Bean and Brew menu,suggest the most"
            f"suitable drink with a short description of why it matches their preference")

@router.prompt("prompt://bean-and-brew/caffeine-guide")
def caffeine_guide_prompt(caffeine_level: str) -> str:
    """
    Returns a prompt to guide the customer to the
    right drink based on their desired caffeine level —
    high, medium or low.
    Use this when the customer asks about caffeine
    content or wants a gentle or strong option.
    """
    return (
        f"The customer wants a drink with {caffeine_level} caffeine. "
        f"From the Bean & Brew menu recommend the best option that "
        f"matches this caffeine preference. Briefly explain the "
        f"caffeine level of the suggested drink and why it suits "
        f"their need. Keep it simple and helpful."
    )
 