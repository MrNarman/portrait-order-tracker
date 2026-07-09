import storage


test_data = {
    "orders": [
        {"order_id": "TOSH-2026-001", "client_name": "Test Client", "status": "INQUIRY"}
    ],
    "meta": {"last_order_number": 1}
}

storage.save_data(test_data)
reloaded = storage.load_data()
print(reloaded)