from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import MenuItem
from app.extensions import db

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('', methods=['GET'])
def get_menu():
    category = request.args.get('category')
    
    query = MenuItem.query.filter_by(available=True)
    
    if category:
        query = query.filter_by(category=category)
    
    items = query.all()
    
    # Group by category
    grouped = {}
    for item in items:
        if item.category not in grouped:
            grouped[item.category] = []
        grouped[item.category].append(item.to_dict())
    
    return jsonify(grouped), 200

@menu_bp.route('', methods=['POST'])
@jwt_required()
def create_menu_item():
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('category') or not data.get('price'):
        return jsonify({'error': 'Name, category, and price required'}), 400
    
    item = MenuItem(
        name=data['name'],
        category=data['category'],
        price=float(data['price']),
        available=data.get('available', True)
    )
    
    db.session.add(item)
    db.session.commit()
    
    return jsonify(item.to_dict()), 201

@menu_bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_menu_item(item_id):
    item = MenuItem.query.get(item_id)
    
    if not item:
        return jsonify({'error': 'Menu item not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        item.name = data['name']
    if 'category' in data:
        item.category = data['category']
    if 'price' in data:
        item.price = float(data['price'])
    if 'available' in data:
        item.available = data['available']
    
    db.session.commit()
    
    return jsonify(item.to_dict()), 200

@menu_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_menu_item(item_id):
    item = MenuItem.query.get(item_id)
    
    if not item:
        return jsonify({'error': 'Menu item not found'}), 404
    
    # Soft delete
    item.available = False
    db.session.commit()
    
    return jsonify({'message': 'Menu item deleted'}), 200
