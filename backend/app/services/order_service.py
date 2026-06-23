from datetime import datetime, timedelta
from app.extensions import db
from app.models import Order, OrderItem, Customer, MenuItem

VALID_STATUS_TRANSITIONS = {
    'pending': ['confirmed'],
    'confirmed': ['preparing'],
    'preparing': ['ready'],
    'ready': ['delivered'],
    'delivered': []
}

def create_order(customer_email, customer_phone, items_data):
    """
    Create a new order with items.
    items_data: list of dicts with menu_item_id and quantity
    """
    # Find or create customer
    customer = Customer.query.filter_by(email=customer_email).first()
    if not customer:
        customer = Customer(
            email=customer_email,
            phone=customer_phone
        )
        db.session.add(customer)
        db.session.flush()  # Get the ID
    
    # Validate all menu items exist and are available
    menu_items = {}
    for item_data in items_data:
        menu_item = MenuItem.query.filter_by(
            id=item_data['menu_item_id'],
            available=True
        ).first()
        if not menu_item:
            raise ValueError(f"Menu item {item_data['menu_item_id']} not found or unavailable")
        menu_items[menu_item.id] = menu_item
    
    # Create order
    order = Order(
        customer_id=customer.id,
        status='pending',
        total_amount=0
    )
    db.session.add(order)
    db.session.flush()  # Get the order ID
    
    # Create order items with price snapshot
    total_amount = 0
    for item_data in items_data:
        menu_item = menu_items[item_data['menu_item_id']]
        order_item = OrderItem(
            order_id=order.id,
            menu_item_id=menu_item.id,
            quantity=item_data['quantity'],
            unit_price=menu_item.price  # Snapshot price at order time
        )
        db.session.add(order_item)
        total_amount += item_data['quantity'] * menu_item.price
    
    # Update total amount
    order.total_amount = total_amount
    db.session.commit()
    
    # Calculate estimated time (15-30 minutes)
    import random
    estimated_minutes = random.randint(15, 30)
    
    return order, estimated_minutes

def update_order_status(order_id, new_status):
    """
    Update order status with validation of transitions
    """
    order = Order.query.get(order_id)
    if not order:
        raise ValueError("Order not found")
    
    current_status = order.status
    
    # Validate transition
    if new_status not in VALID_STATUS_TRANSITIONS.get(current_status, []):
        raise ValueError(f"Invalid status transition from {current_status} to {new_status}")
    
    order.status = new_status
    order.updated_at = datetime.utcnow()
    db.session.commit()
    
    return order

def get_order(order_id):
    """Get order by ID with all details"""
    order = Order.query.get(order_id)
    if not order:
        raise ValueError("Order not found")
    return order
