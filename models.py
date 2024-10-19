from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Episode(db.Model):
    __tablename__ = 'episodes'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    appearances = db.relationship('Appearance', backref='episode', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Episode {self.number} on {self.date}>'


class Guest(db.Model):
    __tablename__ = 'guests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer)  # this field is from the CSV
    show = db.Column(db.String(50))  # this field is from the CSV
    group = db.Column(db.String(50))  # this this field is from the CSV
    appearances = db.relationship('Appearance', backref='guest', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Guest {self.name}, Occupation: {self.occupation}, Year: {self.year}, Show: {self.show}>'


class Appearance(db.Model):
    __tablename__ = 'appearances'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)

    def __repr__(self):
        return f'<Appearance: Guest ID {self.guest_id}, Episode ID {self.episode_id}, Rating {self.rating}>'
