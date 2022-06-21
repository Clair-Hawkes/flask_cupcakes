"""Flask app for Cupcakes"""

from itsdangerous import Serializer
from flask import Flask, jsonify, request

# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake

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


@app.get("/api/cupcakes/<int:cupcake_id>")
def cupcake_get_data(cupcake_id):
    """
    Get data about a single cupcake. Returns with JSON:
        {cupcake: {id, flavor, size, rating, image}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialize = cupcake.serialize()

    return jsonify(cupcake=serialize)


@app.post("/api/cupcakes")
def cupcake_create():
    """
    Creates a cupcake instance with id, flavor, size, rating, and image and adds
    to db.
    Takes flavor, size, rating, and image.
    Returns with JSON:
        {cupcake: {id, flavor, size, rating, image}}
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json.get("image")
    image = image if image else None

    # alternate method
    # image = request.get_json()["image"]

    new_cupcake = Cupcake(
        flavor=flavor,
        size=size,
        rating=rating,
        image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)

@app.patch('/api/cupcakes/<int:cupcake_id>')
def cupcake_update_values(cupcake_id):
    """
    Update a cupcake by id. Any value(s) can be updated.
    Updates instance and commits update to database.
    Returns JSON:
        {cupcake: {id, flavor, size, rating, image}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    flavor = request.json.get("flavor")
    if flavor:
        cupcake.flavor = flavor

    size = request.json.get("size")
    if size:
        cupcake.size = size

    rating = request.json.get("rating")
    if rating:
        cupcake.rating = rating

    image = request.json.get("image")
    if image:
        cupcake.image = image

    # possible_updates = ['flavor','size','rating','image']

    # for update in possible_updates:
    #     if update:
    #         cupcake.(update)

    db.session.commit()

    # TODO: Why dont we re-initialize cupcake after commit?
    # cupcake = Cupcake.query.get(cupcake_id)
    serialize = cupcake.serialize()

    return (jsonify(cupcake=serialize))



@app.delete('/api/cupcakes/<int:cupcake_id>')
def cupcake_delete(cupcake_id):
    """
    Delete a cupcake instance and remove from db via id.
    Takes JSON cupcake ID.
    returns JSON {deleted: [cupcake-id]}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return {"deleted":cupcake_id}
