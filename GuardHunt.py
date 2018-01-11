from flask import Flask
from config import DevelopmentConfig
from models import db, Users
from BlueprintMain.routes import main
from models import login_manager


def create_app(config=DevelopmentConfig) -> Flask:
    app = Flask(__name__)
    login_manager.init_app(app)

    app.config.from_object(config)
    app.register_blueprint(main)
    app.secret_key = '\x850\x81D1\x98\xee-\x80\x9cY7\xc7Io\xd40\x9d\x04'

    db.init_app(app)

    @app.before_first_request
    def add_user():
        db.create_all()
        db.session.commit()
        u = Users(password='test', email='john@example.com', username='huntc', user_type='admin')
        db.session.add(u)
        db.session.commit()


    return app


if __name__ == '__main__':
    main_app = create_app()
    main_app.run()
