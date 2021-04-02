import os

from flask import Flask, render_template
from werkzeug.middleware.shared_data import SharedDataMiddleware

from . import settings, controllers, models
from .extensions import db, s3

project_dir = os.path.dirname(os.path.abspath(__file__))


def create_app(config_object=settings):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)

    from .models import user
    from .models import photo

    with app.app_context():
        db.create_all()

    app.add_url_rule(
        '/uploads/<filename>',
        'uploaded_file',
        build_only=True
    )

    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/uploads': settings.UPLOAD_FOLDER
    })

    response = s3.list_buckets()
    print('buckets:')
    for bucket in response['Buckets']:
        print(f' {bucket["Name"]}')

    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(controllers.home.blueprint)
    app.register_blueprint(controllers.auth.blueprint)
    app.register_blueprint(controllers.join.blueprint)
    app.register_blueprint(controllers.about.blueprint)
    app.register_blueprint(controllers.art.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""
    @app.errorhandler(401)
    def internal_error(error):
        return render_template('401.html'), 401

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    return None
