from sys import argv, exit
import csv
from cs50 import SQL


if len(argv) < 2:
    print("Incorrect usage.")
    exit(1)

house = argv[1]

db = SQL("sqlite:///students.db")

students = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", house)

for row in students:
    if row['middle'] == None:
        name = row['first'] + " " + row['last']
    else:
        name = row['first'] + " " + row['middle'] + " " + row['last']
    print(f"{name}, born {row['birth']}")