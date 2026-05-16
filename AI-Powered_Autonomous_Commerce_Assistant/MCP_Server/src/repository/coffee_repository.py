import uuid
from typing import List, Optional
from src.repository.error_repository import ErrorRepository
from src.repository.database import get_db
from src.repository.schema import MenuItemSchema, OrderSchema, OrderItemSchema, ErrorLogSchema,Customer
from src.utils.exceptions.custom_app_exception import DatabaseConnectionException,CustomerNotFoundException

error=ErrorRepository()
class CoffeeRepository:

    def get_menu_items(self) -> List[MenuItemSchema]:
        try:
            with get_db() as session:
                query = session.query(MenuItemSchema).filter(MenuItemSchema.is_active.is_(True)).order_by(MenuItemSchema.item_name.asc()).all()
                return query
        except DatabaseConnectionException:
            raise
        except Exception as e:
            error.error(
                file_name="coffee_repository",
                function_name="get_menu_items",
                message=f"Failed to fetch menu items: {str(e)}"
            )
            raise DatabaseConnectionException(detail=f"Failed to fetch menu items: {str(e)}")

    def get_menu_item_by_name(self, name: str) -> Optional[MenuItemSchema]:
        try:
            with get_db() as session:
                item = session.query(MenuItemSchema).filter(
                    MenuItemSchema.item_name.ilike(name)
                ).first()
                return item
        except DatabaseConnectionException:
            raise
        except Exception as e:
            error.error(
                file_name="coffee_repository",
                function_name="get_menu_item_by_name",
                message=f"Failed to fetch menu item by name: {str(e)}"
            )
            raise DatabaseConnectionException(detail=f"Failed to fetch menu item by name: {str(e)}")

    def get_order_by_code(self, order_code: str) -> Optional[OrderSchema]:
        try:
            with get_db() as session:
                order = session.query(OrderSchema).filter(OrderSchema.order_code == order_code).first()
                return order
        except DatabaseConnectionException:
            raise
        except Exception as e:
            error.error(
                file_name="coffee_repository",
                function_name="get_order_by_code",
                message=f"Failed to fetch order: {str(e)}"
            )
            raise DatabaseConnectionException(detail=f"Failed to fetch order: {str(e)}")

    def create_order(
        self,
        customer_id: str,
        total_price: float,
        status: str = "PREPARING"
    ) -> OrderSchema:
        try:
            with get_db() as session:
                if len(customer_id) == 36:
                    cust = session.query(Customer).filter(Customer.customer_id == customer_id).first()
                    if not cust:
                        raise CustomerNotFoundException(customer_id)
                    else:
                        order_code = f"ORD-{uuid.uuid4().hex[:8].upper()}"
                        order = OrderSchema(
                            order_code=order_code,
                            customer_id=customer_id,
                            status=status,
                            total_price=total_price,
                            created_by="SYSTEM",
                            updated_by="SYSTEM"
                        )

                        session.add(order)
                        session.commit()
                        session.refresh(order)
                        return order                    
        except DatabaseConnectionException:
            raise
        except Exception as e:
            error.error(
                file_name="coffee_repository",
                function_name="create_order",
                message=f"Failed to create order customer not found: {str(e)}"
            )
            raise DatabaseConnectionException(detail=f"Failed to create order: {str(e)}")

    def create_order_items(self, order_id: str, items: list) -> None:
        try:
            with get_db() as session:
                for item in items:
                    record = OrderItemSchema(
                        order_id=order_id,
                        item_id=item["item_id"],
                        quantity=item["quantity"],
                        price=item["price"],
                        created_by="SYSTEM",
                        updated_by="SYSTEM"
                    )
                    session.add(record)
                session.commit()
        except DatabaseConnectionException:
            raise
        except Exception as e:
            error.error(
                file_name="coffee_repository",
                function_name="create_order_items",
                message=f"Failed to create order items: {str(e)}"
            )
            raise DatabaseConnectionException(detail=f"Failed to create order items: {str(e)}")

    def reduce_stock(self, item_id: str, quantity: int) -> None:
        try:
            with get_db() as session:
                item = session.query(MenuItemSchema).filter(
                    MenuItemSchema.item_id == item_id
                ).first()
                if not item:
                    return
                item.stock = max(item.stock - quantity, 0)
                session.commit()
        except DatabaseConnectionException:
            raise
        except Exception as e:
            error.error(
                file_name="coffee_repository",
                function_name="reduce_stock",
                message=f"Failed to update stock: {str(e)}"
            )
            raise DatabaseConnectionException(detail=f"Failed to update stock: {str(e)}")


   