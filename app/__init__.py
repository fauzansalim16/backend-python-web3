# FILE: app/__init__.py
from flask import Flask
import click
import os
from .config import Config
from .extensions import db, ma, migrate, jwt
from .routes import all_blueprints 
from seed import run_specific_seeder, run_all_seeders

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    jwt.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)


    @app.cli.command("seed")
    @click.option("--name", help="Seeder name to run")
    def seed(name):
        """Run a specific seeder by name."""
        if name:
            run_specific_seeder(name)
        else:
            print("Please provide a seeder name using --name or use `flask seed_all` to run all seeders.")

    @app.cli.command("seed_all")
    def seed_all():
        """Run all seeders."""
        run_all_seeders()

    return app