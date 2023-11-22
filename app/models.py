from app import db


post_liker = db.Table(
    'post_liker',
    db.Column('user_id', db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey(
        'post.id', ondelete='CASCADE'), primary_key=True)
)


comment_liker = db.Table(
    'comment_liker',
    db.Column('user_id', db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('comment_id', db.Integer, db.ForeignKey(
        'comment.id', ondelete='CASCADE'), primary_key=True)
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    price = db.Column(db.Integer, nullable=True)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey(
        'ingredient.id', ondelete='CASCADE'), nullable=True)

    user = db.relationship('User', backref=db.backref('post_set'))
    liker = db.relationship('User', secondary=post_liker,
                            backref=db.backref('post_liker_set'))
    ingredient = db.relationship('Ingredient', backref=db.backref('post_set'))
    # image_id = db.Column(db.Integer, db.ForeignKey(
    #     'image.id', ondelete='CASCADE'), nullable=True)
    # image = db.relationship('User', backref=db.backref('post_set'))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete='CASCADE'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=True)
    post = db.relationship('Post', backref=db.backref('comment_set'))
    user = db.relationship('User', backref=db.backref('comment_set'))
    liker = db.relationship('User', secondary=comment_liker,
                            backref=db.backref('comment_liker_set'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=True)
    price = db.Column(db.Integer, unique=False, nullable=True)
    unit = db.Column(db.Integer, unique=False, nullable=True)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(150), unique=False, nullable=True)
    post_id = db.Column(db.Integer, nullable=False)
