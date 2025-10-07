"""
Tests demonstrating different test categories and execution strategies.
"""
import pytest
import platform
from order_processor import OrderProcessor, Order, OrderItem, OrderStatus

# Test data
SAMPLE_ORDER = Order(
    order_id="123",
    customer_id="456",
    items=[
        OrderItem("prod1", 2, 10.0),
        OrderItem("prod2", 1, 20.0)
    ]
)

@pytest.fixture
def processor():
    """Create an OrderProcessor instance."""
    return OrderProcessor("mock://db")

@pytest.mark.slow
def test_bulk_processing(processor):
    """Test processing multiple orders (marked as slow)."""
    orders = [
        Order("1", "c1", [OrderItem("p1", 1, 10.0)]),
        Order("2", "c2", [OrderItem("p2", 2, 20.0)]),
        Order("3", "c3", [OrderItem("p3", 3, 30.0)])
    ]
    
    results = processor.bulk_process(orders)
    assert all(results)
    assert all(order.status == OrderStatus.COMPLETED for order in orders)

@pytest.mark.integration
def test_order_processing_flow(processor):
    """Test complete order processing flow."""
    order = SAMPLE_ORDER
    
    # Validate
    assert processor.validate_order(order)
    
    # Process
    assert processor.process_order(order)
    
    # Verify final state
    assert order.status == OrderStatus.COMPLETED
    assert order.total == 40.0

@pytest.mark.platform("Windows")
def test_windows_specific(processor):
    """Test Windows-specific behavior."""
    if platform.system() != "Windows":
        pytest.skip("Test requires Windows")
    
    order = SAMPLE_ORDER
    assert processor.process_order(order)

@pytest.mark.flaky(reruns=3, reruns_delay=1)
def test_potentially_flaky(processor):
    """Test that might need retries."""
    import random
    
    # Simulate occasional failures
    if random.random() < 0.3:  # 30% chance of failure
        raise RuntimeError("Random failure")
    
    assert processor.process_order(SAMPLE_ORDER)

@pytest.mark.parametrize("invalid_order", [
    pytest.param(Order("", "c1", [OrderItem("p1", 1, 10.0)]), id="empty-order-id"),
    pytest.param(Order("o1", "", [OrderItem("p1", 1, 10.0)]), id="empty-customer-id"),
    pytest.param(Order("o1", "c1", []), id="no-items"),
    pytest.param(Order("o1", "c1", [OrderItem("p1", 0, 10.0)]), id="zero-quantity"),
    pytest.param(Order("o1", "c1", [OrderItem("p1", 1, -1.0)]), id="negative-price")
])
def test_invalid_orders(processor, invalid_order):
    """Test various invalid order scenarios."""
    assert not processor.validate_order(invalid_order)

def test_parallel_safe(processor, tmp_path):
    """
    Test that's safe for parallel execution.
    Uses tmp_path fixture to ensure isolated test data.
    """
    # Create order with unique ID using tmp_path
    order_id = f"order_{tmp_path.name}"
    order = Order(order_id, "c1", [OrderItem("p1", 1, 10.0)])
    
    assert processor.process_order(order)

@pytest.mark.requires_network
def test_network_dependent(processor):
    """Test that requires network access."""
    # This test will be skipped if network is not available
    order = SAMPLE_ORDER
    assert processor.process_order(order)