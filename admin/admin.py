from flask import Blueprint
from admin.product import admin_product_bp
from admin.account import admin_account_bp
from admin.customer import admin_customer_bp
from admin.dashboard import admin_dashboard_bp
from admin.process import admin_process_bp
from admin.transit import admin_transit_bp

admin_bp = Blueprint('admin', __name__)

admin_bp.register_blueprint(admin_product_bp, url_prefix='/product')
admin_bp.register_blueprint(admin_customer_bp, url_prefix='/customer')
admin_bp.register_blueprint(admin_dashboard_bp, url_prefix='/dashboard')
admin_bp.register_blueprint(admin_process_bp, url_prefix='/process')
admin_bp.register_blueprint(admin_transit_bp, url_prefix='/transit')
admin_bp.register_blueprint(admin_account_bp, url_prefix='/')
