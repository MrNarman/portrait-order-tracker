import order_service
import models
import storage

def record_payment(data:dict, order_id:str, amount:int) -> bool | None:
    """
    Record a payment against an order, updating its balance and payment status.

    Args:
        data (dict): The full loaded data structure, containing
                      "orders" (list of order dicts) and "meta".
        order_id (str): The order_id of the order being paid.
        amount (int): The amount being paid, added to the order's deposit_paid.

    Returns:
        bool | None: True if the payment was recorded and saved,
                     None if no order matched the given order_id.
    """

    order = order_service.find_order(data, order_id)

    if order:
        order["price"]["deposit_paid"] += amount
        order["price"]["balance"] = order["price"]["total"] - order["price"]["deposit_paid"]
        order["price"]["payment_status"] = models.determine_payment_status(order["price"]["total"], order["price"]["deposit_paid"])

        storage.save_data(data)
        return True
    else:
        return None
