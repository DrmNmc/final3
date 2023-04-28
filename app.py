from flask import Flask, render_template, request, url_for, redirect, flash, session
from modules.caesar_cipher import caesar_cipher
from modules import form_validation as form_validation_module
import sqlite3
from modules.execute_query import execute_query
"""
I left the commented code for errors before adding flash() in form validation.
"""
app = Flask(__name__)
app.config['SECRET_KEY'] = 'K>~EEAnH_x,Z{q.43;NmyQiNz1^Yr7'
app.config['DEBUG'] = True


@app.route("/", methods=["GET"])
def main_page():
    return render_template("index.html")


@app.route("/caesar", methods=["GET", "POST"])
def caesar_cipher_route():
    """Hello Flask: Caesar Cipher"""
    if request.method == "POST":
        text = request.form["text"]
        shift = int(request.form["shift"])
        action = request.form["action"]
        mode = 1 if action == "encrypt" else -1
        result_text = caesar_cipher(text, shift, mode)
        return render_template("caesar/index.html", result_text=result_text)
    else:
        return render_template("caesar/index.html")


@app.route("/form_validation", methods=["GET", "POST"])
def form_validation():
    """Refill the Flask: Form_validation with Flash()"""
    success = None
    form_submitted = None

    if request.method == "POST":
        form_submitted = request.form.get("form_submitted")
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # errors = form_validation_module.validate_form(username, email, password, confirm_password)
        form_validation_module.validate_form(username, email, password, confirm_password)

    #     if not errors:
    #         return redirect(url_for("form_validation_success"))
    #     else:
    #         return render_template("form_validation/index.html", username=username, email=email, errors=errors)
    # else:
    #     return render_template("form_validation/index.html", errors={})
    if not session.get('_flashes'):
        if form_submitted:
            success = True
            flash("The form has been submitted successfully.", "success")
            return redirect(url_for("form_validation_success"))

    return render_template("form_validation/index.html")


@app.route("/form_validation/success", methods=["GET"])
def form_validation_success():
    """Form Validation Redirect as Required"""
    return render_template("form_validation/success_page.html")


@app.route('/sqlite_example', methods=['GET', 'POST'])
def sqlite_example_index():
    if request.method == 'POST':
        session['table'] = request.form['table']

        if session['table'] == 'movies':
            session['columns'] = ['movie_id', 'title', 'year_released', 'director']
        else:
            session['columns'] = ['director_id', 'last_name', 'first_name']

        query_type = '/' + request.form['query_type'].lower()

        return redirect(query_type)
    else:
        query_types = ['INSERT', 'SELECT', 'UPDATE', 'DELETE']

        session.clear()

    return render_template("sqlite_example/index.html", tab_title="Movie SQL Project", query_types=query_types, home=True)


@app.route('/insert', methods=['GET', 'POST'])
def insert_query():
    if request.method == 'POST':
        columns = ', '.join(session['columns'][1:])
        values = request.form['values']
        table = session['table']

        sql_query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        results = execute_query(sql_query)
    else:
        sql_query = ''
        results = ''

    return render_template("sqlite_example/insert.html", tab_title="INSERT query", home=False, sql_query=sql_query, results=results)


@app.route('/select', methods=['GET', 'POST'])
def select_query():
    if request.method == 'POST':
        table = session['table']
        columns = request.form['columns']
        condition = request.form['condition']
        sql_query = f"SELECT {columns} FROM {table}"
        if condition != '':
            sql_query += f" WHERE {condition}"

        if columns == '*':
            session['selected_columns'] = session['columns'].copy()
        else:
            session['selected_columns'] = columns.split(',')

        results = execute_query(sql_query)
    else:
        sql_query = ''
        results = ''

    return render_template("sqlite_example/select.html", tab_title="SELECT query", home=False, sql_query=sql_query, results=results)


@app.route('/update', methods=['GET', 'POST'])
def update_query():
    if request.method == 'POST':
        new_value = request.form['new_value']
        condition = request.form['condition']
        table = session['table']

        sql_query = f"UPDATE {table} SET {new_value}"
        if condition != '':
            sql_query += f" WHERE {condition}"
        results = execute_query(sql_query)
    else:
        sql_query = ''
        results = ''

    return render_template("sqlite_example/update.html", tab_title="UPDATE query", home=False, sql_query=sql_query, results=results)


@app.route('/delete', methods=['GET', 'POST'])
def delete_query():
    if request.method == 'POST':
        condition = request.form['condition']
        table = session['table']
        sql_query = f"DELETE FROM {table} WHERE {condition}"
        results = execute_query(sql_query)
    else:
        sql_query = ''
        results = ''

    return render_template('sqlite_example/delete.html', tab_title='DELETE query', home=False, sql_query=sql_query, results=results)


if __name__ == "__main__":
    app.run(debug=True)
