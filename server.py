from flask import Flask
from admin.admin import admin_bp
from web.web import web_bp

app = Flask(__name__)
app.secret_key = "my_secret_key"

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(web_bp, url_prefix='/')

if __name__ == "__main__":
    app.run(debug=True)
