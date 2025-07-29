from flask import redirect, session
from functools import wraps
from datetime import datetime, date

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def calculate_days_left(due_date_str):
    today = date.today()
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    return (due_date - today).days

def get_color_class(days_left):
    if days_left <= 10:
        return "table-danger"
    elif 11 <= days_left <= 20:
        return "table-warning"
    elif 21 <= days_left <= 30:
        return "table-info"
    else:
        return ""
