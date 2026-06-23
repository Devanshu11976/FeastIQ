from datetime import datetime, timedelta
from app.extensions import db
from app.models import Customer, Order

def segment_customers():
    """
    Segment all customers based on their order history (last 90 days)
    """
    ninety_days_ago = datetime.utcnow() - timedelta(days=90)
    
    customers = Customer.query.all()
    
    for customer in customers:
        # Count orders in last 90 days
        recent_orders = Order.query.filter(
            Order.customer_id == customer.id,
            Order.created_at >= ninety_days_ago
        ).all()
        
        total_orders = len(recent_orders)
        
        if total_orders == 0:
            customer.segment = 'Inactive'
        else:
            # Calculate average order value
            total_value = sum(order.total_amount for order in recent_orders)
            avg_value = total_value / total_orders
            
            # Segment assignment
            if total_orders >= 10 or avg_value >= 1000:
                customer.segment = 'VIP'
            elif 4 <= total_orders <= 9 and 400 <= avg_value <= 999:
                customer.segment = 'Regular'
            else:
                customer.segment = 'Occasional'
    
    db.session.commit()
    
    # Return segment counts
    segments = {}
    for customer in customers:
        segments[customer.segment] = segments.get(customer.segment, 0) + 1
    
    return segments
