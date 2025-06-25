from flask import Blueprint, send_from_directory
test_bp = Blueprint('test', __name__)
@test_bp.route('/test-html')
def test_html():
    """Test HTML route"""
    return send_from_directory('/app/bookshop', 'bookshop-frontend.html')
@test_bp.route('/test-ui')
def test_ui():
    """Test UI route"""
    return send_from_directory('/app/bookshop', 'bookshop-frontend.html') 