from app.database.database import get_db_connection

def run_sql_query(query: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def get_db_schema():
    schema = {}

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table_name_tuple in tables:
            table_name = table_name_tuple[0]

            # Get column info for each table
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()

            # Extract column name and type
            schema[table_name] = [
                {"name": col[1], "type": col[2]} for col in columns
            ]

    return schema
