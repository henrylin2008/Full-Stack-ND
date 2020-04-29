import psycopg2

connection = psycopg2.connect('dbname=mangodb user=mango password=mango port=5433')

cursor = connection.cursor()


cursor.execute('DROP TABLE IF EXISTS tb2')


# (re)create the todos table
# (note: triple quotes allow multiline text in python)
cursor.execute("""
  CREATE TABLE tb2 (
    id INTEGER PRIMARY KEY,
    completed VARCHAR NOT NULL
  );
""")

# string composition: using a tuple
# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
cursor.execute('INSERT INTO tb2 (id, completed) VALUES (%s, %s);', (1, True))

# string composition: using dictionary 
SQL = 'INSERT INTO tb2 (id, completed) VALUES (%(id)s, %(completed)s);'

data = {
  'id': 2,
  'completed': False
 }
cursor.execute(SQL, data)
# commit, so it does the executions on the db and persists in the db
connection.commit()

cursor.close()
connection.close()