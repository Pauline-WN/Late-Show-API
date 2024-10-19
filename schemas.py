from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validates, ValidationError
from models import Appearance, Episode, Guest
from flask import url_for

class AppearanceSchema(SQLAlchemyAutoSchema):
    # HATEOAS: Including a self-link to the appearance resource
    links = fields.Method("generate_appearance_links")

    class Meta:
        model = Appearance
        include_fk = True
        load_instance = True

    rating = fields.Int(required=True)

    @validates('rating')
    def check_rating(self, value):
        if value < 1 or value > 5:
            raise ValidationError("Rating must be between 1 and 5.")

    # Method to generate HATEOAS links for Appearance
    def generate_appearance_links(self, obj):
        return {
            "self": url_for("singleappearanceresource", appearance_id=obj.id, _external=True),
            "episode": url_for("singleepisoderesource", episode_id=obj.episode_id, _external=True),
            "guest": url_for("singleguestresource", guest_id=obj.guest_id, _external=True),
        }


class EpisodeSchema(SQLAlchemyAutoSchema):
    appearance_list = fields.Nested('AppearanceSchema', many=True, exclude=("episode",))
    links = fields.Method("generate_episode_links")  # HATEOAS links

    class Meta:
        model = Episode
        include_fk = True
        load_instance = True

    # Method to generate HATEOAS links for Episode
    def generate_episode_links(self, obj):
        return {
            "self": url_for("singleepisoderesource", episode_id=obj.id, _external=True),
            "appearances": url_for("appearancecreationresource", episode_id=obj.id, _external=True)
        }


class GuestSchema(SQLAlchemyAutoSchema):
    appearance_list = fields.Nested('AppearanceSchema', many=True, exclude=("guest",))
    links = fields.Method("generate_guest_links")  # HATEOAS links

    class Meta:
        model = Guest
        include_fk = True
        load_instance = True

    # Method to generate HATEOAS links for Guest
    def generate_guest_links(self, obj):
        return {
            "self": url_for("singleguestresource", guest_id=obj.id, _external=True),
            "appearances": url_for("appearancecreationresource", guest_id=obj.id, _external=True)
        }
