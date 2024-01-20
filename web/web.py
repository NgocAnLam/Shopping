from flask import Blueprint
from web.home import web_home_bp
from web.account import web_account_bp
from web.category import web_category_bp
from web.product import web_product_bp
from web.user import web_user_bp
from web.shopping_cart import web_shopping_cart_bp
from web.comment import web_comment_bp

web_bp = Blueprint('web', __name__)


web_bp.register_blueprint(web_category_bp, url_prefix = '/')
web_bp.register_blueprint(web_product_bp, url_prefix = '/')
web_bp.register_blueprint(web_user_bp, url_prefix = '/')
web_bp.register_blueprint(web_shopping_cart_bp, url_prefix = '/')
web_bp.register_blueprint(web_account_bp, url_prefix = '/')
web_bp.register_blueprint(web_home_bp, url_prefix = '/')
web_bp.register_blueprint(web_comment_bp, url_prefix = '/')
