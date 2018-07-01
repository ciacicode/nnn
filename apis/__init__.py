from flask_restplus import Api
from .resume import api as ns1


api = Api(version="0.0.1", title="Nearly Nameless Nick", description="Remove unconcious bias in your recruitment process")
api.add_namespace(ns1)
