import calendar
from datetime import datetime, timedelta

import unidecode

# -- Admin ----------------------------------------------------------------

def get_a_week():
    current_date = datetime.now().date()
    result = {str(current_date - timedelta(days=i)): 0 for i in range(7)}
    return result


def get_a_year(year):
    first_day = datetime(year, 1, 1).date()
    last_day = datetime(year, 12, 31).date()
    result = {str(first_day + timedelta(days=i)): 0 for i in range((last_day - first_day).days + 1)}
    return result


def get_a_month(year, month):
    first_day = datetime(year, month, 1).date()
    _, last_day = calendar.monthrange(year, month)
    result = {str(first_day + timedelta(days=i)): 0 for i in range(last_day)}
    return result

def convert_to_slug(text):
    text = text.replace("/", " ")
    text = text.replace(" - ", " ")
    no_accents = unidecode(text)
    slug = no_accents.lower().replace(" ", "-")
    slug = "".join(char if char.isalnum() or char == "-" else "" for char in slug)
    return slug

def get_order_by_id(order_list, target_order_id):
    for order in order_list:
        if order.get("orderID") == target_order_id:
            return order
    return None

# -- Web ----------------------------------------------------------------

