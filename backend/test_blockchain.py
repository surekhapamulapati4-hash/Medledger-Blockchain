from blockchain import store_hash, get_hash

report_id = "test-report-001"
hash_value = "abc123hash"

store_hash(report_id, hash_value)
result = get_hash(report_id)

print("Stored Hash:", result)
