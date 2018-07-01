from flask import Flask
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app, version="0.0.1", title="Nearly Nameless Nick", description="Remove unconcious bias in your recruitment process")


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

if __name__ == '__main__':
    app.run(debug=True)
