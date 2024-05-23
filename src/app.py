"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"msg": f'Member with id: {id} not found'}), 404

@app.route('/member', methods=['POST'])
def add_member():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"msg": "Body info is needed"}), 400
    if "first_name" not in body:
        return jsonify({"msg": "First Name is needed"}), 400
    if "age" not in body:
        return jsonify({"msg": "Age is needed"}), 400
    if "lucky_numbers" not in body:
        return jsonify({"msg": "Age is needed"}), 400
    print(body)
    new_member_data = {
        "id": body.get("id", jackson_family._generateId()),
        "first_name": body["first_name"],
        "last-name": jackson_family.last_name,
        "age": body["age"],
        "lucky_numbers": body["lucky_numbers"] 
    }
    jackson_family.add_member(new_member_data)
    print(jackson_family._members)
    return jsonify({"msg": "New member added"}), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    if jackson_family.delete_member(id):
        print(jackson_family._members)
        return jsonify({"done": True}), 200
    else:
        return jsonify({"done": False}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
