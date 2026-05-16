from src.router.mcp_router import router
from typing import Dict,List
import json
from src.repository.coffee_repository import CoffeeRepository
from src.repository.error_repository import ErrorRepository
from src.utils.exceptions.custom_app_exception import (AppBaseException,MenuItemNotFoundException,OrderNotFoundException,InsufficientStockException,InvalidRequestException,)
from mcp.types import TextContent,ResourceContents
repo = CoffeeRepository()
error=ErrorRepository()


@router.resource("menu://items")
def check_menu() -> str:
    """
    Returns all active menu items from Bean & Brew
    This is a read only resource us this to fetch the full menu including prices,tax rate and stock status
    """
    try:
        items = repo.get_menu_items()
        result= {
            "items": [
                {
                    "item_name": item.item_name,
                    "description": item.description,
                    "item_price": float(item.item_price),
                    "tax_rate": float(item.tax_rate),
                    "in_stock": item.stock > 0,
                }
                for item in items
            ]
        }
        print(json.dumps(result))
        return (json.dumps(result))
       
    except AppBaseException:
        raise
    except Exception as exc:
        error.error(
                file_name="tools",
                function_name="check_menu",
                message=f"Failed to fetch menu: {str(exc)}"
            )
        raise ValueError(f"Failed to fetch menu: {str(exc)}")
    
@router.resource("resource://shop-info")
def shop_info() ->str:
    """
    Returns Bean and Brew Shop details including name,address,
    working,hours,contact information and social media links
    Use this when the user asks about the shop name,address
    timings,contact or anything related to the shop itself
    """

    shop_info={
        "shop_name":"Bean and Brew",
        "tagline":"Brewed with love,serverd with warmth",
        "address":"12,Coffee Street,Navalur,Chennai,Tamil Nadu,600001,India",
        "working_hours":"All days available from 9:00 AM to 10:00 PM",
        "contact":{
            "phone":"+91 99445 96758",
            "email":"beanandbrew@gmail.com",
            "whatsapp":"+91 99445 96758"
        },
        "social_media":{
            "instagram":"beanandbrew_chennai",
        },
        "facilities":[
            "Free Wifi",
            "Indoor seating",
            "Outdoor Seating",
            "Take away",
            "Online Ordering",
            "Pet Friendly"
        ],
        "payment_mode":[
            "cash",
            "UPI",
            "Credit Card",
            "Debit Card",
            "Net Banking"
        ],
        "about":"Bean and Brew is a cozy spexiality coffee shop in the heart of chennai,we have got the perfect cup and corner for you "
    }
    return json.dumps(shop_info)
