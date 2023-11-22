from commercial_app import db
from commercial_app import login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


tags = db.Table('posts_tag',
                db.Column('blogposts_id', db.Integer,
                          db.ForeignKey('post.id'), nullable=False),
                db.Column('tag_id', db.Integer, db.ForeignKey(
                    'tag.id'), nullable=False)
                )

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    client_secret = db.Column(db.String,nullable=False)
    posts = db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return f"Admin('username: {self.username}', 'Email: {self.email}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    product_image = db.Column(
        db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    # should provide list of values...
    tags = db.relationship('Tag', secondary=tags, backref='posts')

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    address = db.Column(db.Text)
    password = db.Column(db.String(60), nullable=False)
    cart = db.relationship('Cart',backref='owner',uselist=False,lazy=True)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    total_price = db.Column(db.Integer)
    cart_products = db.relationship('CartProduct',backref='products',lazy=True)

class CartProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer,db.ForeignKey('post.id'),nullable=False)
    cart_id = db.Column(db.Integer,db.ForeignKey('cart.id'),nullable=False)
    quantity = db.Column(db.Integer,nullable=False)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.Text, unique=True)

    def __init__(self, tagname):
        self.tagname = tagname

    def __repr__(self):
        return f'Tag(tagname={self.tagname})'
