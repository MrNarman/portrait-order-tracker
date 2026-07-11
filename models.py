import datetime
import time

current_year = time.strftime("%Y")
ORDER_PREFIX = 'TOSH-'

A4_SINGLE_SUBJECT_BASE = 1800
A4_COUPLE_BASE = 2600
A4_GROUP_BASE = 3500

A3_SINGLE_BASE = 2500
A3_COUPLE_BASE = 3600
A3_GROUP_BASE = 5000

A4_FRAMING = 800
A3_FRAMING = 1200
RUSH_ORDER = 500
LAMINATION = 200
DIGITAL_SCAN = 300

BASE_PRICES = {
    "A4": {
        "single": A4_SINGLE_SUBJECT_BASE,
        "couple": A4_COUPLE_BASE,
        "group": A4_GROUP_BASE,
    },
    "A3": {
        "single": A3_SINGLE_BASE,
        "couple": A3_COUPLE_BASE,
        "group": A3_GROUP_BASE,
    },
}

VALID_TRANSITIONS = {
    "INQUIRY": ["CONFIRMED", "CANCELLED"],
    "CONFIRMED": ["IN_PROGRESS", "CANCELLED"],
    "IN_PROGRESS": ["COMPLETED", "CANCELLED"],
    "COMPLETED": ["DELIVERED"],
    "DELIVERED": [],       # terminal state, nothing after this
    "CANCELLED": [],       # also terminal
}

def is_valid_transition(current_state:str, new_status:str) -> bool:
    """
    Check whether moving an order from current_state to new_status
    is allowed by the defined order status flow.

    Args:
        current_state (str): The order's current status.
        new_status (str): The status being transitioned to.

    Returns:
        bool: True if the transition is allowed, False otherwise
              (including if current_state is not a recognized status).
    """

    if current_state not in VALID_TRANSITIONS:
        return False
    return new_status in VALID_TRANSITIONS[current_state]

def new_order(last_order_number:int, client_name:str, contact:str, size:str, subject_type:str, 
              framing:bool = False, rush:bool = False, lamination:bool = False, 
              digital_scan:bool = False) -> dict:
    """
    Build a new order dict with defaults for a freshly created order.

    Args:
        last_order_number (int): The most recent order number used so far.
        client_name (str): Name of the client.
        contact (str): Client's phone number or IG handle.
        size (str): "A4" or "A3".
        subject_type (str): "single", "couple", or "group".
        framing (bool): Whether framing is included. Defaults to False.
        rush (bool): Whether rush delivery is requested. Defaults to False.
        lamination (bool): Whether lamination is included. Defaults to False.
        digital_scan (bool): Whether a digital scan is included. Defaults to False.

    Returns:
        dict: A fully structured order, ready to be appended to
              data["orders"] and saved via storage.save_data().
    """
    
    order_id = f"{ORDER_PREFIX}{current_year}-{last_order_number + 1}"
    total_price = calculate_price(size,subject_type, framing, rush, lamination, digital_scan)

    order = {
        'order_id': order_id, 
        'client_name': client_name,
        'contact': contact, 
        'specs': {
            'size': size.upper(),
            'subject_type': subject_type,
            'framing': framing,
            'rush': rush,
            'lamination': lamination,
            'digital_scan': digital_scan
        },
        'price': {
            'total': total_price,
            'deposit_paid': 0,
            'balance': total_price, 
            'payment_status':"UNPAID"
        },
        'status': "INQUIRY",
        'status_history': [
            {'status': "INQUIRY", 'date': datetime.date.today().isoformat()}
        ],
        'created_date': datetime.date.today().isoformat(),
    }
    return order

def calculate_price(size, subject_type, framing=False, rush=False, lamination=False, digital_scan=False) -> int:
    """
    Calculate the total price for a portrait order.

    Args:
        size (str): Paper size, "A4" or "A3" (case-insensitive).
        subject_type (str): "single", "couple", or "group".
        framing (bool): Whether framing is included. Defaults to False.
        rush (bool): Whether rush delivery is requested. Defaults to False.
        lamination (bool): Whether lamination is included. Defaults to False.
        digital_scan (bool): Whether a digital scan is included. Defaults to False.

    Returns:
        int: Total price in KES.

    Raises:
        KeyError: If size or subject_type is not a recognized value.
    """

    size = size.upper()
    base = BASE_PRICES[size][subject_type]
    total = base

    if framing:
        total += A4_FRAMING if size == "A4" else A3_FRAMING
    if rush:
        total += RUSH_ORDER
    if lamination:
        total += LAMINATION
    if digital_scan:
        total += DIGITAL_SCAN

    return total

def determine_payment_status(total, deposit_paid) -> str:
    """
    Determine the payment status based on total price and amount paid.

    Args:
        total (int): The order's total price.
        deposit_paid (int): Amount paid so far.

    Returns:
        str: "UNPAID", "DEPOSIT", or "PAID"
    """
    if deposit_paid == 0:
        return "UNPAID"
    elif deposit_paid < total:
        return "DEPOSIT"
    else:
        return "PAID"