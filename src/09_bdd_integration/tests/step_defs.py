"""
Step definitions for shopping cart BDD tests.
"""
from decimal import Decimal
from pytest_bdd import given, when, then, parsers
from shopping_cart.cart import ShoppingCart, Product

# Fixtures and shared objects
@given("the shopping cart is empty", target_fixture="cart")
def empty_cart():
    """Create a new empty shopping cart."""
    return ShoppingCart()

@given(parsers.parse('the following products exist:'), target_fixture="product_catalog")
def product_catalog():
    """Create a product catalog."""
    return {
        "PROD1": Product("PROD1", "Test Product 1", Decimal("10.00")),
        "PROD2": Product("PROD2", "Test Product 2", Decimal("20.00")),
        "PROD3": Product("PROD3", "Test Product 3", Decimal("30.00")),
    }

# Given steps
@given(parsers.parse('I have added product "{product_id}" with quantity {quantity:d}'))
def add_product_to_cart(cart, product_catalog, product_id, quantity):
    """Add a product to the cart with given quantity."""
    product = product_catalog[product_id]
    cart.add_item(product, quantity)

# When steps
@when(parsers.parse('I add product "{product_id}" with quantity {quantity:d}'))
def add_product(cart, product_catalog, product_id, quantity):
    """Add a product to the cart."""
    product = product_catalog[product_id]
    cart.add_item(product, quantity)

@when(parsers.parse('I remove product "{product_id}" from the cart'))
def remove_product(cart, product_id):
    """Remove a product from the cart."""
    cart.remove_item(product_id)

@when(parsers.parse('I update the quantity of product "{product_id}" to {quantity:d}'))
def update_product_quantity(cart, product_id, quantity):
    """Update the quantity of a product in the cart."""
    cart.update_quantity(product_id, quantity)

# Then steps
@then(parsers.parse("the cart should contain {count:d} item"))
def check_cart_size(cart, count):
    """Check the number of items in the cart."""
    assert len(cart.items) == count

@then("the cart should be empty")
def check_cart_empty(cart):
    """Check that the cart is empty."""
    assert cart.is_empty

@then(parsers.parse("the cart total should be {total:f}"))
def check_cart_total(cart, total):
    """Check the total price of the cart."""
    assert cart.total == Decimal(str(total))