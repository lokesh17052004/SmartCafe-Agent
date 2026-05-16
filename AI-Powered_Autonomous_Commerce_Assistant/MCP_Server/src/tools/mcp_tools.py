from typing import Any, Dict, List
from src.router.mcp_router import router
from src.repository.coffee_repository import CoffeeRepository
from src.repository.error_repository import ErrorRepository
from src.utils.exceptions.custom_app_exception import (AppBaseException,MenuItemNotFoundException,OrderNotFoundException,InsufficientStockException,InvalidRequestException,)

repo = CoffeeRepository()
error=ErrorRepository()



@router.tool
def check_inventory(item_name: str) -> Dict:
    """
    Check the stock quantity of a specific menu item by name.
    Use when the user asks if a specific drink is available or how many are left.

    Arguments:
        item_name (str): Name of the menu item. Must match the menu name exactly (case-insensitive).

    Returns:
        {
            "item_name": str,        # Matched menu item name
            "stock": int,            # Number of units available
            "in_stock": bool         # True if stock > 0
        }
    """
    try:
        item = repo.get_menu_item_by_name(item_name)
        if not item:
            error.error(
                file_name="tools",
                function_name="check_inventory",
                message="Menu item not found"
            )
            raise MenuItemNotFoundException(item_name)
        return {
            "item_name": item.item_name,
            "stock": item.stock,
            "in_stock": item.stock > 0,
        }
    except AppBaseException:
        raise
    except Exception as exc:
        error.error(
                file_name="tools",
                function_name="check_inventory",
                message=f"Failed to check inventory: {str(exc)}"
            )
        raise ValueError(f"Failed to check inventory: {str(exc)}")


@router.tool
def check_order_status(order_code: str) -> Dict:
    """
    Look up the current status of an order using its order code.
    Use when the user provides an order code and asks about their order status.

    Arguments:
        order_code (str): The unique order code (e.g. ORD-A1B2C3D4).

    Returns:
        {
            "order_id": str,       # Internal UUID of the order
            "order_code": str,     # Unique order reference code
            "status": str,         # Current status: PREPARING, READY, or SERVED
            "total_price": float   # Total price of the order
        }
    """
    try:
        order = repo.get_order_by_code(order_code)
        if not order:
            error.error(
                file_name="tools",
                function_name="get_order_by_code",
                message=f"Failed to fetch order"
            )
            raise OrderNotFoundException(order_code)
        return {
            "order_id": str(order.order_id),
            "order_code": order.order_code,
            "status": order.status,
            "total_price": float(order.total_price),
        }
    except AppBaseException:
        raise
    except Exception as exc:
        error.error(
                file_name="tools",
                function_name="check_order_status",
                message=f"Failed to check order status: {str(exc)}"
            )
        raise ValueError(f"Failed to check order status: {str(exc)}")


@router.tool
def add_order(customer_id: str, items: List[Dict[str, Any]]) -> Dict:
    """Place a new order for a customer.

    Args:
        customer_id: The id of the customer placing the order.
        items: A list of dicts with 'item' (str) and 'quantity' (int) keys.
               Example: [{"item": "Latte", "quantity": 2}, {"item": "Espresso", "quantity": 1}]
    """
    try:
        if not items:
            error.error(
                file_name="tools",
                function_name="add_order",
                message="Order items cannot be empty."
            )
            raise InvalidRequestException("Order items cannot be empty.")
  
        order_items = []
        total_price = 0.0

        for item in items:
            item_name = item.get("item")
            quantity = item.get("quantity")
            if not item_name or quantity <= 0:
                error.error(
                file_name="tools",
                function_name="add_order",
                message="Each item must include item_name and quantity > 0."
            )
                raise InvalidRequestException("Each item must include item_name and quantity > 0.")

            menu_item = repo.get_menu_item_by_name(item_name)
            if not menu_item:
                error.error(
                file_name="tools",
                function_name="add_order",
                message=f"'{item_name}' is not on our menu. Cannot place order."
            )
                raise ValueError(f"'{item_name}' is not on our menu. Cannot place order.")
            if menu_item.stock < quantity:
                error.error(
                file_name="tools",
                function_name="add_order",
                message="Rrquired quantity is more than stock available"
            )
                raise InsufficientStockException(menu_item.item_name, menu_item.stock)

            item_total = menu_item.item_price * quantity
            tax_amount = item_total * (menu_item.tax_rate / 100)
            line_price = round(item_total + tax_amount, 2)
            total_price += line_price

            order_items.append({
                "item_id": str(menu_item.item_id),
                "quantity": quantity,
                "price": line_price,
            })

        order = repo.create_order(
            customer_id=customer_id,
            total_price=round(total_price, 2),
            status="PREPARING",
        )
        repo.create_order_items(order_id=str(order.order_id), items=order_items)
        for item in order_items:
            repo.reduce_stock(item["item_id"], item["quantity"])

        return {
            "order_id": str(order.order_id),
            "order_code": order.order_code,
            "status": order.status,
            "total_price": float(order.total_price),
        }
    except (AppBaseException):
        raise
    except Exception as exc:
        error.error(
                file_name="tools",
                function_name="add_order",
                message=f"Failed to place order: {str(exc)}"
            )
        raise ValueError(f"Failed to place order: {str(exc)}")





