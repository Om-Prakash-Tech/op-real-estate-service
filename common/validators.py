from dateutil import parser
import re

def validate_str(value):
    if not isinstance(value, str):
        return False
    if not value.strip():
        return False
    # Additional validation logic for strings can be added here
    return True

def validate_int(value):
    if not isinstance(value, int):
        return False
    # Additional validation logic for integers can be added here
    return True

def validate_bool(value):
    if not isinstance(value, bool):
        return False
    # Additional validation logic for booleans can be added here
    return True

def validate_email(value):
    if not isinstance(value, str):
        return False
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        return False
    # Additional validation logic for email addresses can be added here
    return True

def validate_phone(value):
    if not re.match(r"^\d{10}$", str(value)):
        return False
    # Additional validation logic for phone numbers can be added here
    return True

def validate_datetime(value):
    if not isinstance(value, str):
        return False
    try:
        # Parse the incoming date string into a Python datetime object
        parser.parse(value)
    except Exception as e:
        return False
    return True

# def validate_duration(value):
#     # Duration is a string in the format HH:MM and it should be less than 12 hours
#     if not isinstance(value, str):
#         return False
#     if not re.match(r"^\d{1,2}:\d{2}$", value):
#         return False
#     hours, minutes = map(int, value.split(':'))
#     if hours > 12:
#         return False
#     if minutes > 59:
#         return False
#     return True

def validate_name(value):
    if not isinstance(value, str):
        return False
    if re.search(r"[^a-zA-Z\s\u0900-\u097F\u00C0-\u024F\u1E00-\u1EFF\u00C0-\u1FFF]", value):
        return False
    # Additional validation logic for names can be added here
    return True

def validate_password(value):
    pattern = re.compile(r'^(?!\s+)(?!.*\s+$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[$^*.[\]{}()?"!@#%&/\\,><\':;|_~`=+\- ])[A-Za-z0-9$^*.[\]{}()?"!@#%&/\\,><\':;|_~`=+\- ]{8,256}$')
    return bool(pattern.match(str(value)))
    