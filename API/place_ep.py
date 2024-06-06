from flask import Blueprint, jsonify, request, abort
from models import Place

place_bp = Blueprint("place", "place")


@place_bp.route("/places", methods=["POST"])
def create_place(user_id):
    """create a place"""
    if user_id not in request.json:
        abort(400)
    


@place_bp.route("/places", methods=["GET"])
def get_places():
    """get all places"""
    return jsonify(Place.all()), 200


@place_bp.route("/places/<place_id>", methods=["GET"])
def get_place(place_id):
    """get a place"""
    return jsonify(Place.get(place_id)), 200


@place_bp.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id, user_id):
    """update a place"""
    if user_id not in request.json:
        abort(400)
    
    

@place_bp.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """delete a place"""
    return jsonify(Place.delete(place_id)), 204
