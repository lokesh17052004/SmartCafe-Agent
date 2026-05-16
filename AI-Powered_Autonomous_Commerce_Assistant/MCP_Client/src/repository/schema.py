import uuid
from sqlalchemy import (
    Column, String, Numeric, Boolean, Integer,
    Text, TIMESTAMP, ForeignKey, Float, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.repository.database import Base


class MenuItemSchema(Base):
    __tablename__ = "menu_items"

    item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    item_price = Column(Float(precision=7), nullable=False)
    tax_rate = Column(Float(precision=5), nullable=False)
    stock = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    created_by = Column(String(100), nullable=False, default="SYSTEM")
    updated_by = Column(String(100), nullable=True)
    updated_at = Column(TIMESTAMP, onupdate=func.now(), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    order_items = relationship("OrderItemSchema", back_populates="menu_item")


class OrderSchema(Base):
    __tablename__ = "orders"

    order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_code = Column(String(100), unique=True, nullable=False)
    customer_name = Column(String(100), nullable=False)
    status = Column(String(50),CheckConstraint("status IN ('PREPARING', 'READY', 'SERVED')"),nullable=False,default="PREPARING")
    total_price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    created_by = Column(String(100), nullable=False, default="SYSTEM")
    updated_by = Column(String(100), nullable=True)
    updated_at = Column(TIMESTAMP, onupdate=func.now(), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    items = relationship("OrderItemSchema", back_populates="order")


class OrderItemSchema(Base):
    __tablename__ = "order_items"

    order_items_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.order_id"), nullable=False)
    item_id = Column(UUID(as_uuid=True), ForeignKey("menu_items.item_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    created_by = Column(String(100), nullable=False, default="SYSTEM")
    updated_by = Column(String(100), nullable=True)
    updated_at = Column(TIMESTAMP, onupdate=func.now(), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    order = relationship("OrderSchema", back_populates="items")
    menu_item = relationship("MenuItemSchema", back_populates="order_items")


class ErrorLogSchema(Base):
    __tablename__ = "error_logs"

    error_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_name = Column(Text, nullable=True)
    function_name = Column(Text, nullable=True)
    message = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    created_by = Column(String(100), nullable=False, default="SYSTEM")
    updated_by = Column(String(100), nullable=True)
    updated_at = Column(TIMESTAMP, onupdate=func.now(), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)