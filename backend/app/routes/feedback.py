from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import Feedback, Order, Customer
from app.extensions import db

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('', methods=['POST'])
def create_feedback():
    data = request.get_json()
    
    if not data or not data.get('order_id') or not data.get('customer_email') or not data.get('rating'):
        return jsonify({'error': 'order_id, customer_email, and rating required'}), 400
    
    # Validate rating
    try:
        rating = int(data['rating'])
        if rating < 1 or rating > 5:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400
    
    # Validate order exists and belongs to customer
    order = Order.query.get(data['order_id'])
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    if order.customer.email != data['customer_email']:
        return jsonify({'error': 'Order does not belong to this customer'}), 403
    
    # Validate order is delivered
    if order.status != 'delivered':
        return jsonify({'error': 'Can only review delivered orders'}), 400
    
    # Check for existing feedback
    existing = Feedback.query.filter_by(order_id=data['order_id']).first()
    if existing:
        return jsonify({'error': 'Feedback already exists for this order'}), 400
    
    # Create feedback
    feedback = Feedback(
        order_id=data['order_id'],
        customer_id=order.customer_id,
        rating=rating,
        comment=data.get('comment')
    )
    
    db.session.add(feedback)
    db.session.commit()
    
    return jsonify(feedback.to_dict()), 201

@feedback_bp.route('', methods=['GET'])
@jwt_required()
def get_feedbacks():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    rating_filter = request.args.get('rating', type=int)
    
    query = Feedback.query
    
    if rating_filter:
        query = query.filter_by(rating=rating_filter)
    
    pagination = query.order_by(Feedback.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'feedbacks': [f.to_dict() for f in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@feedback_bp.route('/order/<int:order_id>', methods=['GET'])
def get_feedback_by_order(order_id):
    feedback = Feedback.query.filter_by(order_id=order_id).first()
    
    if not feedback:
        return jsonify({'error': 'Feedback not found'}), 404
    
    return jsonify(feedback.to_dict()), 200
