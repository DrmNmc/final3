import sqlite3


def execute_query(query_string):
    db = sqlite3.connect('project.db')
    cursor = db.cursor()
    if "select" in query_string.lower():
        try:
            results = list(cursor.execute(query_string))
        except:
            results = 'error'
    else:
        try:
            cursor.execute(query_string)
            db.commit()
            results = "success"
        except:
            results = 'error'
    db.close()
    return results
