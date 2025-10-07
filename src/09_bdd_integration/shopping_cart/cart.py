"""
Core shopping cart functionality.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional
from decimal import Decimal

@dataclass
class Product:
    """Product model."""
    id: str
    name: str
    price: Decimal

@dataclass
class CartItem:
    """Shopping cart item."""
    product: Product
    quantity: int

    @property
    def total(self) -> Decimal:
        """Calculate total price for this item."""
        return self.product.price * self.quantity

class ShoppingCart:
    """Shopping cart implementation."""
    
    def __init__(self):
        """Initialize an empty cart."""
        self._items: Dict[str, CartItem] = {}
    
    def add_item(self, product: Product, quantity: int = 1) -> None:
        """Add a product to the cart."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if product.id in self._items:
            # Update quantity if product already in cart
            current_item = self._items[product.id]
            current_item.quantity += quantity
        else:
            # Add new item to cart
            self._items[product.id] = CartItem(product, quantity)
    
    def remove_item(self, product_id: str) -> None:
        """Remove a product from the cart."""
        self._items.pop(product_id, None)
    
    def update_quantity(self, product_id: str, quantity: int) -> None:
        """Update the quantity of a product."""
        if quantity <= 0:
            self.remove_item(product_id)
        elif product_id in self._items:
            self._items[product_id].quantity = quantity
    
    def get_item(self, product_id: str) -> Optional[CartItem]:
        """Get a specific item from the cart."""
        return self._items.get(product_id)
    
    @property
    def items(self) -> List[CartItem]:
        """Get all items in the cart."""
        return list(self._items.values())
    
    @property
    def total(self) -> Decimal:
        """Calculate total price of the cart."""
        return sum(item.total for item in self._items.values())
    
    @property
    def is_empty(self) -> bool:
        """Check if cart is empty."""
        return len(self._items) == 0
    
    def clear(self) -> None:
        """Remove all items from the cart."""
        self._items.clear()