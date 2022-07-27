"""Flask app for Cupcakes"""

from flask import Flask, request, render_template, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Debug Toolbar
from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SHHHH!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)


@app.route("/")
def homepage():
    """Home page"""

    return render_template("index.html")


@app.route("/api/cupcakes")
def get_cupcakes():
    """Get data about all cupcakes"""

    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]

    return jsonify(cupcakes=cupcakes)


@app.route("/api/cupcakes", methods=['POST'])
def add_cupcake():
    """Add cupcake and return data about new cupcake"""

    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)
    
    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.to_dict()), 201)


@app.route("/api/cupcakes/<int:cupcake_id>")
def show_cupcake(cupcake_id):
    """Get data about a single cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    return jsonify(cupcake=cupcake.to_dict())


@app.route("/api/cupcakes/<int:cupcake_id>", methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update data about a single cupcake"""

    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())


@app.route("/api/cupcakes/<int:cupcake_id>", methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete a single cupcake and return confirmation message"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")