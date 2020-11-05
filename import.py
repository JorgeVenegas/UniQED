from sys import argv, exit
import csv
from cs50 import SQL


if len(argv) < 2:
    print("Incorrect usage.")
    exit(1)

ctrs = argv[1]

db = SQL("sqlite:///students.db")

with open(ctrs) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        fname = row['name'].split()
        house = row['house']
        birth = row['birth']

        first = fname[0]
        if len(fname) == 3:
            middle = fname[1]
            last = fname[2]
        else:
            middle = None
            last = fname[1]
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?);", first, middle, last, house, birth)
