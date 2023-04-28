from flask import redirect, url_for

def go_to_main():
    return redirect(url_for("main_page"))