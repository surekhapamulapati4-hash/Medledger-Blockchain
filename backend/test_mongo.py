from backend.db import hospitals_collection

test = {
    "hospital_id": "test_hospital",
    "hospital_name": "Test Hospital",
    "email": "test@hospital.com",
    "password": "test123",
    "address": "Test City"
}

hospitals_collection.insert_one(test)
print("✅ MongoDB Insert Successful")
