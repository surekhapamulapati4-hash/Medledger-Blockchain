from werkzeug.security import generate_password_hash, check_password_hash
from backend.db import hospitals_collection


def create_hospital(data):
    data["password"] = generate_password_hash(data["password"])
    hospitals_collection.insert_one(data)


def get_hospital_by_id(hospital_id):
    return hospitals_collection.find_one({
        "hospital_id": hospital_id
    })


def verify_hospital_login(hospital_id, password):

    hospital = hospitals_collection.find_one({
        "hospital_id": hospital_id
    })

    if not hospital:
        return None

    if not check_password_hash(hospital["password"], password):
        return None

    return hospital