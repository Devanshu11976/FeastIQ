from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.services.analytics_service import (
    get_order_analytics,
    get_feedback_analytics,
    get_segment_analytics,
    get_loyalty_analytics
)

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/orders', methods=['GET'])
@jwt_required()
def orders_analytics():
    analytics = get_order_analytics()
    return jsonify(analytics), 200

@analytics_bp.route('/feedback', methods=['GET'])
@jwt_required()
def feedback_analytics():
    analytics = get_feedback_analytics()
    return jsonify(analytics), 200

@analytics_bp.route('/segments', methods=['GET'])
@jwt_required()
def segments_analytics():
    analytics = get_segment_analytics()
    return jsonify(analytics), 200

@analytics_bp.route('/loyalty', methods=['GET'])
@jwt_required()
def loyalty_analytics():
    analytics = get_loyalty_analytics()
    return jsonify(analytics), 200
