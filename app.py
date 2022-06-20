"""Flask app for Cupcakes"""

from numpy import size
from flask import Flask, url_for, render_template, redirect, flash, jsonify, request

# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake
# from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
# db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# toolbar = DebugToolbarExtension(app)


@app.get("/api/cupcakes")
def cupcakes_get_data():
    """
    Get list of all cupcakess and their data. Returns with JSON:
        {cupcakes: [{id, flavor, size, rating, image}, ...]}
    """

    cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get("/api/cupcakes/<int:cupcake-id>")
def cupcake_get_data(cupcake_id):
    """
    Get data about a single cupcake. Returns with JSON:
        {cupcake: {id, flavor, size, rating, image}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialize = cupcake.serialize()

    return jsonify(cupcake=serialize)


@app.post("/api/cupakes")
def cupcake_create():
    """
    Creates a cupcake with id, flavor, size, rating, and image.
    Returns with JSON:
        {cupcake: {id, flavor, size, rating, image}}
    """

    name = request.json["name"]
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(
        name=name,
        flavor=flavor,
        size=size,
        rating=rating,
        image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)
