from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database.connection import Base


class Customer(Base):
    """
    Customer records — the primary actor in our e-commerce domain.
    """
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    city = Column(String(80), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # One customer can have many orders
    orders = relationship("Order", back_populates="customer")


class Product(Base):
    """
    Product catalog entries.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    category = Column(String(80), nullable=False, index=True)
    price = Column(Float, nullable=False)

    # One product can appear in many order items
    order_items = relationship("Order", back_populates="product")


class Order(Base):
    """
    Order transactions — links a customer to a product with a quantity.
    Represents the core many-to-many relationship between Customer and Product.
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    order_date = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    product = relationship("Product", back_populates="order_items")
    # One order has one payment
    payment = relationship("Payment", back_populates="order", uselist=False)


class Payment(Base):
    """
    Payment records — tracks money received for each order.
    """
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True, index=True)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)

    # Back-reference to the parent order
    order = relationship("Order", back_populates="payment")