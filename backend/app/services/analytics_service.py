from datetime import datetime, timedelta
from sqlalchemy import func, extract
from app.extensions import db
from app.models import Order, OrderItem, Feedback, Customer
from app.services.segmentation_service import segment_customers

def get_order_analytics():
    """
    Get order analytics for the last 30 days
    """
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    # Daily orders (last 30 days)
    daily_orders = db.session.query(
        func.date(Order.created_at).label('date'),
        func.count(Order.id).label('count')
    ).filter(
        Order.created_at >= thirty_days_ago
    ).group_by(
        func.date(Order.created_at)
    ).order_by(
        func.date(Order.created_at)
    ).all()
    
    daily_orders_dict = {str(date): count for date, count in daily_orders}
    
    # Peak hours (last 30 days)
    peak_hours = db.session.query(
        extract('hour', Order.created_at).label('hour'),
        func.count(Order.id).label('count')
    ).filter(
        Order.created_at >= thirty_days_ago
    ).group_by(
        extract('hour', Order.created_at)
    ).order_by(
        extract('hour', Order.created_at)
    ).all()
    
    peak_hours_dict = {int(hour): count for hour, count in peak_hours}
    
    # Popular items (top 5 by quantity ordered)
    popular_items = db.session.query(
        MenuItem.name,
        func.sum(OrderItem.quantity).label('total_quantity')
    ).join(
        OrderItem, MenuItem.id == OrderItem.menu_item_id
    ).join(
        Order, OrderItem.order_id == Order.id
    ).filter(
        Order.created_at >= thirty_days_ago
    ).group_by(
        MenuItem.id, MenuItem.name
    ).order_by(
        func.sum(OrderItem.quantity).desc()
    ).limit(5).all()
    
    popular_items_dict = [{'name': name, 'quantity': total} for name, total in popular_items]
    
    # Average order value (last 30 days)
    avg_order_value = db.session.query(
        func.avg(Order.total_amount)
    ).filter(
        Order.created_at >= thirty_days_ago
    ).scalar()
    
    return {
        'daily_orders': daily_orders_dict,
        'peak_hours': peak_hours_dict,
        'popular_items': popular_items_dict,
        'avg_order_value': round(avg_order_value or 0, 2)
    }

def get_feedback_analytics():
    """
    Get feedback analytics
    """
    # Average rating
    avg_rating = db.session.query(
        func.avg(Feedback.rating)
    ).scalar()
    
    # Rating distribution
    rating_distribution = db.session.query(
        Feedback.rating,
        func.count(Feedback.id).label('count')
    ).group_by(
        Feedback.rating
    ).all()
    
    rating_dist_dict = {rating: count for rating, count in rating_distribution}
    
    # Recent negative feedback (rating <= 2, last 10)
    recent_negative = Feedback.query.filter(
        Feedback.rating <= 2
    ).order_by(
        Feedback.created_at.desc()
    ).limit(10).all()
    
    recent_negative_list = [f.to_dict() for f in recent_negative]
    
    return {
        'avg_rating': round(avg_rating or 0, 2),
        'rating_distribution': rating_dist_dict,
        'recent_negative': recent_negative_list
    }

def get_segment_analytics():
    """
    Get customer segment counts
    """
    # Run segmentation first
    segment_counts = segment_customers()
    
    return segment_counts

def get_loyalty_analytics():
    """
    Get loyalty metrics
    """
    # Repeat rate: % customers with more than 1 order
    total_customers = Customer.query.count()
    customers_with_multiple_orders = db.session.query(
        Customer.id
    ).join(
        Order, Customer.id == Order.customer_id
    ).group_by(
        Customer.id
    ).having(
        func.count(Order.id) > 1
    ).count()
    
    repeat_rate = (customers_with_multiple_orders / total_customers * 100) if total_customers > 0 else 0
    
    # Retention 30d: % customers who ordered in both last 30 and prev 30 days
    now = datetime.utcnow()
    last_30_days = now - timedelta(days=30)
    prev_30_days = now - timedelta(days=60)
    
    customers_last_30 = db.session.query(Order.customer_id).filter(
        Order.created_at >= last_30_days
    ).distinct().all()
    
    customers_prev_30 = db.session.query(Order.customer_id).filter(
        Order.created_at >= prev_30_days,
        Order.created_at < last_30_days
    ).distinct().all()
    
    last_30_set = {c[0] for c in customers_last_30}
    prev_30_set = {c[0] for c in customers_prev_30}
    
    retained_customers = len(last_30_set & prev_30_set)
    retention_rate = (retained_customers / len(prev_30_set) * 100) if prev_30_set else 0
    
    return {
        'repeat_rate': round(repeat_rate, 2),
        'retention_30d': round(retention_rate, 2)
    }
