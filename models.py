"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect the models.py file to our Flask Application"""

    db.app = app
    db.init_app(app)

class Cupcake(db.Model):

    __tablename__ = 'cupcakes'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    flavor = db.Column(
        db.String(20),
        nullable=False
    )

    size = db.Column(
        db.String(20),
        nullable=False
    )

    rating = db.Column(
        db.Integer,
        nullable=False
    )

    image = db.Column(
        db.Text,
        default='https://tinyurl.com/demo-cupcake',
        nullable=False
    )

    def serialize(self):
        """Serialize to dictionary."""

        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image
        }




