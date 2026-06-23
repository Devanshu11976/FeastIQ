from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models import AdminUser
from app.extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    admin = AdminUser.query.filter_by(username=data['username']).first()
    
    if not admin or not admin.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=admin.id)
    
    return jsonify({
        'access_token': access_token,
        'admin': admin.to_dict()
    }), 200
