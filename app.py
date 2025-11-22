from flask import Flask
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from web.views import web_bp
    from api.tasks_api import api_bp
    
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    with app.app_context():
        db.create_all()
    
    print("\nRegistered Routes:")
    for rule in app.url_map.iter_rules():
        print(rule, "->", rule.endpoint)
        print()
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8000)
