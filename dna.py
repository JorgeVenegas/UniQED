from sys import argv, exit
import csv


def main():
    if len(argv) < 3:
        print(len(argv))
        print("Usage: python dna.py data.csv sequence.txt")
        exit(1)

    db = argv[1]
    sq = argv[2]

    strs = {}

    with open(db, newline="") as database:
        reader = csv.reader(database)
        header = next(reader)
        numsrts = 0
        for kw in header[1:]:
            strs[kw] = 0
            numsrts += 1
        with open(sq) as sequence:
            seq = sequence.read()
            for sttr in strs:
                i = 0
                indx = -1
                actualsum = 0
                for char in seq:
                    indx += 1
                    if i <= 0:
                        actualstr = seq[indx:indx+len(sttr)]
                        if actualstr == sttr:
                            actualsum += 1
                            if strs[sttr] < actualsum:
                                strs[sttr] = actualsum
                            i = len(sttr)
                        else:
                            actualsum = 0
                            i = 1
                    i -= 1
        for row in reader:
            j = 0
            x = 1
            for data in row[1:]:
                if int(data) == strs[header[x]]:
                    j += 1
                else:
                    j = 0
                x += 1
            if j == numsrts:
                print(row[0])
                exit(0)
        print("No match")


main()