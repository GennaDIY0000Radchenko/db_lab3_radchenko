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
        return line.isoformat()
    except AttributeError:
        try:
            return line.strip()
        except AttributeError:
            return str(line)


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
    text = str([row[1] for row in cur])[1:-1].replace("'", "") + "\n"
    cur.execute(f"select * from {table}")
    for row in cur:
        text += str([reformat(el) for el in row])[1:-1].replace("'", "").replace(", ", ",") + "\n"

    file = open(f"export_csv/{table}.csv", "w+")
    file.write(text)
    file.close()

