from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True  # Compact JSON responses

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# ----------------------------
# /plants Resource (GET and POST)
# ----------------------------
class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return [plant.to_dict() for plant in plants], 200

    def post(self):
        try:
            data = request.get_json()

            # Validate input data
            name = data.get('name')
            image = data.get('image')
            price = data.get('price')

            if not all([name, image, price]):
                return {"error": "Missing required fields: name, image, and price"}, 400

            # Create and save new plant
            new_plant = Plant(name=name, image=image, price=price)
            db.session.add(new_plant)
            db.session.commit()

            return new_plant.to_dict(), 201

        except Exception as e:
            return {"error": str(e)}, 400

# ----------------------------
# /plants/<id> Resource (GET)
# ----------------------------
class PlantByID(Resource):
    def get(self, id):
        plant = db.session.get(Plant, id)
        if plant:
            return plant.to_dict(), 200
        return {"error": "Plant not found"}, 404

# ----------------------------
# Register resources with API
# ----------------------------
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

# ----------------------------
# Run the server
# ----------------------------
if __name__ == '__main__':
    app.run(port=5555, debug=True)
