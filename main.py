import storage
import models


test_data = {
    "orders": [
        {"order_id": "TOSH-2026-001", "client_name": "Test Client", "status": "INQUIRY"}
    ],
    "meta": {"last_order_number": 1}
}

# storage.save_data(test_data)
# reloaded = storage.load_data()
# print(reloaded)

# models.create_order(0, "Godrick Narman")
# print(models.calculate_price('a3', 'single', True, True, True, True))

# models.is_valid_transition("INQUIRY", "CONFIRME")

order = models.new_order(0, "Jane Doe", "0712345678", "a4", "single", framing=True)
print(order)