# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask
from config import Config

import v1
import views


def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)
    app.register_blueprint(v1.bp, url_prefix='/v1')
    app.register_blueprint(views.bp, url_prefix='/views')
    return app

if __name__ == '__main__':
    create_app().run(debug=True)
