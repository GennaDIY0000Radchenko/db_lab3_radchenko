import psycopg2

username = 'postgres'
password = '314159265'
host = 'localhost'
port = 5432

database = "lab_2"
conn = psycopg2.connect(user=username, password=password, dbname=database)
cur = conn.cursor()


def reformat(line):
    try:
        return f'"{line.isoformat()}"'
    except AttributeError:
        try:
            return f'"{line.strip()}"'
        except AttributeError:
            return str(line).replace("None", "null")


tables = []
cur.execute("SELECT * FROM pg_catalog.pg_tables")
for row in cur:
    if row[0] == "public":
        tables.append(row[1])

for table in tables:
    cur.execute("select tablename, column_name from pg_catalog.pg_tables left join information_schema.columns on "
                "pg_catalog.pg_tables.tablename = information_schema.columns.table_name "
                f"where table_schema = 'public' and schemaname = 'public' and tablename = '{table}' "
                "order by tablename, ordinal_position")
    col_names = [row[1] for row in cur]
    cur.execute(f"select * from {table}")
    text = "["
    for row in cur:
        text += "{"
        for i in range(len(col_names)):
            text += f'"{col_names[i]}" : {reformat(row[i])}, '
        text = text[:-2]
        text += "},\n"
    text = text[:-2] + "]"

    file = open(f"export_json/{table}.json", "w+")
    file.write(text)
    file.close()
