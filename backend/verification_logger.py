from datetime import datetime, timedelta
from backend.db import verification_logs


# ================= GET IST TIME =================
def get_ist_time():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)


# ================= LOG VERIFICATION =================
def log_verification(
    report_id,
    report_hospital_id,
    report_hospital_name,

    verified_by,
    verified_by_hospital_id=None,
    verified_by_hospital_name=None,

    branch_name=None,

    original_hash=None,
    scanned_hash=None,
    scanned_file=None,

    result="Genuine",

    # NEW FIELDS
    ip_address=None,
    location=None,
    latitude=None,
    longitude=None
):

    ist_time = get_ist_time()

    verification_logs.insert_one({

        # REPORT INFO
        "reportId": report_id,
        "reportHospitalId": report_hospital_id,
        "reportHospitalName": report_hospital_name,

        # VERIFIED BY
        "verifiedBy": verified_by,
        "verifiedByHospitalId": verified_by_hospital_id,
        "verifiedByHospitalName": verified_by_hospital_name,

        # BRANCH
        "branchName": branch_name,

        # HASH INFO
        "originalHash": original_hash,
        "scannedHash": scanned_hash,

        # FILE INFO
        "scannedFile": scanned_file,

        # LOCATION INFO (NEW)
        "ipAddress": ip_address,
        "location": location,
        "latitude": latitude,
        "longitude": longitude,

        # TIME INFO
        "verifiedAt": ist_time,
        "verifiedAtStr": ist_time.strftime("%d %b %Y, %I:%M %p"),

        # RESULT
        "result": result
    })


# ================= GET LOGS =================
def get_verification_logs(filter_query=None):

    if filter_query is None:
        filter_query = {}

    return list(
        verification_logs
        .find(filter_query)
        .sort("verifiedAt", -1)
    )