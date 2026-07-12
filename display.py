def format_order_summary(order:dict) -> str:
    """
    Gets order details and formats them into a summary
    Args:
        order (dict): A single order dict, as returned by find_order or create_order.
    Returns:
        str : order_summary -A summary of the order formatted
    """
    order_summary = f"ID:{order['order_id']}\n Client: {order['client_name']} \n Contact: {order['contact']} \n Payment: {order['price']['payment_status']} \n Specs: {order['specs']['size']}-{order['specs']['subject_type']}"

    return order_summary

def print_order_list(list_orders:list):
    """
    Prints a list of formatted orders

    Args:
        list_orders (list): A list containing several orders
    """

    if not list_orders:
        print("No orders found.")
        return

    for order in list_orders:
        print(format_order_summary(order))
        print('-' * 30)

def print_dashboard(data: dict):
    """
    Print an overview of all orders: total count, total pending
    balance, and a breakdown of orders by status.

    Args:
        data (dict): The full loaded data structure, containing
                      "orders" (list of order dicts) and "meta".
    """
    total_orders = len(data["orders"])

    total_balance = 0
    for order in data["orders"]:
        total_balance += order['price']['balance']

    status_counts = {}
    for order in data["orders"]:
        status = order["status"]
        if status in status_counts:
            status_counts[status] += 1
        else:
            status_counts[status] = 1

    print(f"Total Orders: {total_orders}")
    print(f"Total Pending Balance: {total_balance}")
    print("Orders by Status:")
    for status, count in status_counts.items():
        print(f"  {status}: {count}")