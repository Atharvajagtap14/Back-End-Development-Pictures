from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route('/picture', methods=['GET'])
def get_pictures():
    # Return the list of picture URLs in JSON format
    if data:
        return jsonify(data), 200
    else:
        return make_response(jsonify({"error": "No data found"}), 404)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        for picture in data:
            if picture.get("id") == id:
                return jsonify(picture), 200  # Return the picture as a JSON response
        return make_response(jsonify({"error": "Picture ID not found"}), 404)  # Picture not found
    else:
        return make_response(jsonify({"error": "No data available"}), 404)  # No data available


######################################################################
# CREATE A PICTURE
######################################################################
@app.route('/picture/<int:id>', methods=['POST'])
def create_picture(id):
    picture = request.get_json()
    
    # Check if the picture with the given id already exists
    for item in data:
        if item['id'] == id:
            return jsonify({"Message": f"picture with id {id} already present"}), 302
    
    # Append the picture data to the list
    data.append(picture)
    
    return jsonify(picture), 201
######################################################################
# UPDATE A PICTURE
######################################################################


@app.route('/picture/<int:id>', methods=['PUT'])
def update_picture(id):
    picture_data = request.get_json()
    
    # Find the picture with the given id
    for item in data:
        if item['id'] == id:
            # Update the picture with the incoming request data
            item.update(picture_data)
            return jsonify(item), 200
    
    # If the picture does not exist, return a 404 status code
    return jsonify({"message": "picture not found"}), 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture.get("id") == id:
            # Remove the picture from the list
            data.remove(picture)
            return make_response("", 204)
    return make_response(jsonify({"message": "picture not found"}), 404)