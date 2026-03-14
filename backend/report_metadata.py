from datetime import datetime
from backend.db import reports_collection


def store_metadata(report_id, hospital, issue_date, hospital_id, file_name, report_hash):
    reports_collection.insert_one({
        "report_id": report_id,
        "hospital": hospital,
        "hospital_id": hospital_id,
        "file_name": file_name,
        "hash": report_hash,
        "issue_date": issue_date,
        "created_at": datetime.now()
    })


def get_metadata(report_id):
    return reports_collection.find_one({"report_id": report_id})


def get_reports_by_hospital(hospital_id):
    return list(
        reports_collection.find({"hospital_id": hospital_id})
        .sort("created_at", -1)
    )
