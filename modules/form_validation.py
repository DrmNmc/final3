import re
from flask import flash


def validate_form(username, email, password, confirm_password):
    """errors left commented out to replace with flash() as required"""
    errors = {}

    if not re.match(r"^[a-zA-Z0-9]{3,20}$", username):
        # errors["username"] = "Invalid username: Must be between 3 and 20 characters and contain only letters and numbers."
        flash("Invalid username: Must be between 3 and 20 characters and contain only letters and numbers.")

    if not re.match(r"^[a-zA-Z0-9._%+-]{2,}@([a-zA-Z0-9-]{2,}\.)+[a-zA-Z]{2,}$", email):
        # errors["email"] = "Invalid email address: Must have at least 2 characters before and after '@', and only letters after '.'."
        flash("Invalid email address: Must have at least 2 characters before and after '@', and only letters after '.'.")

    if not re.match(r"^(?=.*[A-Z])(?=.*\W).{8,}$", password):
        # errors["password"] = "Invalid password: Must be at least 8 characters long, with at least one uppercase letter and one special character."
        flash("Invalid password: Must be at least 8 characters long, with at least one uppercase letter and one special character.")

    if password != confirm_password:
        # errors["confirm_password"] = "Passwords do not match."
        flash("Passwords do not match.", "error")

    return errors
