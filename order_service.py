import datetime
import storage
import models

def create_order(data: dict, client_name: str, contact: str, size: str, subject_type: str, 
                 framing:bool = False, rush:bool = False,lamination:bool = False,digital_scan:bool = False) -> dict:
    """
        Args:
            data (dict): The full loaded data structure, containing
                      "orders" (list of order dicts) and "meta".
            client_name (str): Name of the client.
            contact (str): Client's phone number or IG handle.
            size (str): "A4" or "A3".
            subject_type (str): "single", "couple", or "group".
            framing (bool): Whether framing is included. Defaults to False.
            rush (bool): Whether rush delivery is requested. Defaults to False.
            lamination (bool): Whether lamination is included. Defaults to False.
            digital_scan (bool): Whether a digital scan is included. Defaults to False.

        Return: new (dict): Returns a dictionary of the newly created order
    """
    previous_order_num = data["meta"]["last_order_number"]

    new = models.new_order(previous_order_num, client_name, contact, size, subject_type, framing, rush, lamination, digital_scan)
    data["orders"].append(new)

    data["meta"]["last_order_number"] = previous_order_num + 1

    storage.save_data(data)
    return new

def find_order(data: dict, order_id:str) -> dict | None:
    """
    Search for an order by its order_id.

    Args:
        data (dict): The full loaded data structure, containing
                      "orders" (list of order dicts) and "meta".
        order_id (str): The order_id to search for.

    Returns:
        dict | None: The matching order dict if found, otherwise None.
    """

    for order in data["orders"]:
        if order["order_id"] == order_id:
            return order
        
    return None

def update_status(data: dict, order_id: str, new_status: str) -> bool | None:
    """
    Update order status by its order_id.

    Args:
        data (dict):The full loaded data structure, containing
                      "orders" (list of order dicts) and "meta".
        order_id (str): The order_id to search for.
        new_status (str): The next status to be updated to
    Returns:
    bool | None: None if the order was not found,
                 True if the transition was valid and saved,
                 False if the transition was invalid.
    """
    order = find_order(data, order_id)

    if order:
       if models.is_valid_transition(order['status'], new_status):
            order['status'] = new_status
            order['status_history'].append({
                'status': new_status,
                'date': datetime.date.today().isoformat()
            })
            storage.save_data(data)

            return True # Successful transition
       else: 
           return False # Transition Failed

    else:
        return None #Order not found

def filter_orders(data, status= None, client_name= None):
    ...