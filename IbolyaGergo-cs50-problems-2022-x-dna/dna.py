import csv
import sys


def main():

    # TODO: Check for command-line usage

    if len(sys.argv) != 3:
        print("Incorrect number of arguments! Correct: python dna.py databases/large.csv sequences/5.txt")
        return

    # TODO: Read database file into a variable

    database = []
    with open(sys.argv[1], "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            person = {key: row[key] for key in row}
            database.append(person)

    # TODO: Read DNA sequence file into a variable

    with open(sys.argv[2], "r") as file:
        dnaseq = file.read()
    #print (dnaseq)

    # TODO: Find longest match of each STR in DNA sequence

    for person in database:
        match = 1
        for key in person:
            if key != "name":
                if int(person[key]) != longest_match(dnaseq, key):
                    match = 0
                    break
        if match == 1:
            print(person["name"])
            break
    if match == 0:
        print("No match")

    # TODO: Check database for matching profiles

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
