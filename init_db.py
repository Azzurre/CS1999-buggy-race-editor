import sqlite3

DATABASE_FILE = "database.db"

# important:
#-------------------------------------------------------------
# This script initialises your SQLite database for you, just
# to get you started... there are better ways to express the
# data you're going to need... especially outside SQLite.
# For example... maybe flag_pattern should be an ENUM (which
# is available in most other SQL databases), or a foreign key
# to a pattern table?
#
# Also... the name of the database (here, in SQLite, it's a
# filename) appears in more than one place in the project.
# That doesn't feel right, does it?
#-------------------------------------------------------------

connection = sqlite3.connect(DATABASE_FILE)
print("- Opened database successfully in file \"{}\"".format(DATABASE_FILE))

# using Python's triple-quote for multi-line strings:

connection.execute("""

  CREATE TABLE IF NOT EXISTS buggies (
    id                    INTEGER PRIMARY KEY,
    qty_wheels            INTEGER DEFAULT 4,
    flag_color            VARCHAR(50),
    flag_color_secondary  VARCHAR(50),
    flag_pattern          VARCHAR(50),
    power_type          VARCHAR(50),
    power_units          INTEGER DEFAULT 1,
    aux_power_type          VARCHAR(50),
    aux_power_units          INTEGER DEFAULT 0,
    tyres          VARCHAR(50),
    qty_tyres          INTEGER DEFAULT 4,
    armour          VARCHAR(50),
    attack          VARCHAR(50),
    qty_attacks          INTEGER DEFAULT 0,
    fireproof          VARCHAR(50),
    algo          VARCHAR(50),
    antibiotic          VARCHAR(50),
    hamster_booster          VARCHAR(50),
    banging          VARCHAR(50),
    balance          FLOAT(4),
    insulated          VARCHAR(50)
  )

""")

print("- Table \"buggies\" exists OK")

cursor = connection.cursor()

cursor.execute("SELECT * FROM buggies LIMIT 1")
rows = cursor.fetchall()
if len(rows) == 0:
  connection.commit()
  print("- Added one 4-wheeled buggy")
else:
  print("- Found a buggy in the database, nice")

print("- OK, your database is ready")

connection.close()
