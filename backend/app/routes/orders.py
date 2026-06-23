from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.order_service import create_order, update_order_status, get_order
from app.models import Order
from app.extensions import db

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('', methods=['POST'])
def create_new_order():
    data = request.get_json()
    
    if not data or not data.get('customer_email') or not data.get('customer_phone') or not data.get('items'):
        return jsonify({'error': 'customer_email, customer_phone, and items required'}), 400
    
    if not isinstance(data['items'], list) or len(data['items']) == 0:
        return jsonify({'error': 'items must be a non-empty list'}), 400
    
    try:
        order, estimated_minutes = create_order(
            data['customer_email'],
            data['customer_phone'],
            data['items']
        )
        return jsonify({
            'order': order.to_dict(),
            'estimated_time_minutes': estimated_minutes
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    pagination = Order.query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'orders': [order.to_dict() for order in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_single_order(order_id):
    try:
        order = get_order(order_id)
        return jsonify(order.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@orders_bp.route('/<int:order_id>/status', methods=['PATCH'])
@jwt_required()
def update_status(order_id):
    data = request.get_json()
    
    if not data or not data.get('status'):
        return jsonify({'error': 'status required'}), 400
    
    try:
        order = update_order_status(order_id, data['status'])
        return jsonify(order.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
