from flask import Flask, jsonify
from flask_restful import Api, Resource
import subprocess

app = Flask(__name__)
app.secret_key = "EstoEstaDisenadoParaSerInseguro"
api = Api(app)

#Defines API endpoints

class Command(Resource):
    def get(self, cmd):
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return jsonify({"out": result.stdout})

api.add_resource(Command, "/supermegaultrasecretpath/sys/command/<string:cmd>")


if __name__ == "__main__":
    app.run(debug=False, port=5000)
