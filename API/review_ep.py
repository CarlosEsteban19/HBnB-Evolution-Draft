from flask import Blueprint, jsonify, request, abort
from Models.review import Review
from Models.place import Place
from Models.user import User


review_bp = Blueprint("review", __name__)


@review_bp.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """Create a new review for a specified place"""
    place = Place.get(place_id, "Place")
    if place is None:
        abort(404, description="Place not found")
    data = request.json
    if data is None:
        abort(400, description="No data provided (must be JSON)")
    fields = ["user_id", "rating", "comment"]
    for field in fields:
        if field not in data:
            abort(400, description=f"Missing {field}")
    user = User.get(data["user_id"], "User")
    if user is None:
        abort(404, description="User not found")
    if user.id == place.host_id:
        abort(400, description="Host user cannot review their own place")
    review = Review(data["user_id"], place_id,
                    data["rating"], data["comment"])
    place.add_review(review)
    user.add_review(review)
    review.save(review.id, "Review", review)
    place.save(place.id, "Place", place)
    user.save(user.id, "User", user)
    return jsonify(review.to_dict()), 201


@review_bp.route("/review/<review_id>", methods=["GET"])
def get_review(review_id):
    """Retrieve detailed information about a specific review"""
    review = Review.reload(review_id, "Review")
    if review is None:
        abort(404, description="Review not found")
    return jsonify(review), 200


@review_bp.route("/review/<review_id>", methods=["PUT"])
def update_review(review_id):
    """Update an existing review"""
    review = Review.get(review_id, "Place")
    if review is None:
        abort(404, description="Review not found")
    comment = request.json["comment"]
    rating = request.json["rating"]
    review.comment = comment
    review.rating = rating
    review.update(review.id, "Review", review)
    return jsonify(review.to_dict()), 201


@review_bp.route("/review/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """Delete a review"""
    review = Review.get(review_id, "Review")
    if review is None:
        abort(404, description="Review not found")
    review.delete(review.id, "Review")
    return "Review deleted", 204


@review_bp.route("/places/<place_id>/reviews", methods=["GET"])
def get_place_reviews(place_id):
    """Retrieve all reviews for a specific place"""
    place = Place.get(place_id, "Place")
    if place is None:
        abort(404, description="Place not found")
    if place.reviews is None:
        abort(404, description="Place has no reviews")
    place_reviews = [review.to_dict() for review in place.reviews]
    return jsonify(place_reviews), 200


@review_bp.route("/users/<user_id>/reviews", methods=["GET"])
def get_user_reviews(user_id):
    """Retrieve all reviews written by a specific user"""
    user = User.get(user_id, "User")
    if user is None:
        abort(404, description="User not found")
    if user.reviews is None:
        abort(404, description="User has no reviews")
    user_reviews = [review.to_dict() for review in user.reviews]
    return jsonify(user_reviews), 200
