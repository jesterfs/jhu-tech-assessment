from pathlib import Path
import json
from datetime import datetime
import time



# this function controls the process
def analyzeVCF():
    # Gets the files from user
    files = get_files()
    # sends files to be analyzed
    analyze_files(files)


# Gets input from user
def get_files():
    # array of files
    files = []

    file = input("Please enter full file path: ")
    my_file = Path(file.strip())

    # varifies that the file exists
    while my_file.is_file() == False:
        print('file does not exist')
        file = input("Please enter full file path: ")
        my_file = Path(file.strip())

    # adds file names to array
    files.append(file.strip())

    answer = input("Do you have another file? y/n: ")
    while answer.lower() != 'n' and answer.lower() != 'no':
        file = input("Please enter full file path: ")
        my_file = Path(file.strip())

        # varifies that the file exists
        while my_file.is_file() == False:
            print('file does not exist')
            file = input("Please enter full file path: ")
            my_file = Path(file.strip())

        files.append(file.strip())
        answer = input("Do you have another file? y/n: ")

    # returns the array of files to be analyzed
    return files


# Produces the printed results
def analyze_files(files):

    result = loopOverFiles(files)

    numFiles = len(files)

    # prints results if analyzing multiple files
    if numFiles > 1:
        print("\n")
        print(f"\nYou analyzed {numFiles} files, and between them there are:")
        print(f"{result['SNVs']} SNVs and {result['indels']} Indels")
        print(f"The breakdown of SNVs per chromosome are:")
        for chrom in result['snv_by_chrom']:
            print(f"{result['snv_by_chrom'][chrom]} SNVs on chromosome {chrom}")
        print(f"The mean read depth is {result['read_depth_mean']}")
        print(f"And the SNV concordance is {result['concordance']}%")

    # prints results if analyzing one file
    else:
        print("\n")
        print(f"\nIn {files[0]}, there are:")
        print(f"{result['SNVs']} SNVs and {result['indels']} Indels")
        print(f"The breakdown of SNVs per chromosome is:")
        for chrom in result['snv_by_chrom']:
            print(f"{result['snv_by_chrom'][chrom]} SNVs on chromosome {chrom}")
        print(f"The mean read depth is {result['read_depth_mean']}\n")


    json_file_name = datetime.now().strftime("%A_%d_%b_%Y_%H:%M:%S_%p")
    with open(f"{json_file_name}.json", "w") as outfile:
        json.dump(result, outfile)

        # returns results as dictionary

    print("\n")
    print(f"These results have been saved in the current folder as {json_file_name}.json")
    return result


# parses the file and gets results
def loopOverFiles(files):
    SNVs = 0
    unique_SNVs = 0
    snv_by_chrom = {}
    indels = 0
    read_depth_total = 0
    num_variants = 0

    duplicates = 0

    length = sum(file_len(file) for file in files)
    intro_lines = 0

    # storing alt, chromosome, and position as strings separated by spaces so we can calculate duplicates
    collection = set()

    # sets up dictionary of results
    results = {"SNVs": 0, "snv_by_chrom": {}, "indels": 0, "read_depth_mean": 0, "num_variants": 0, "duplicates": 0}

    # using generator expressions to loop through files and lines in files
    lines = (line for file in files for line in open(file, 'r'))
    # loop through each line in the file
    for line in lines:
        # header lines all start with "#", so this skips them
        if line.startswith('#'):
            intro_lines += 1
            continue
        # fields in VCF files are split by tabs, so this separates them within the line
        fields = line.strip().split('\t')
        # Get the appropriate fields
        chromosome = fields[0]
        position = fields[1]
        ID = fields[2]
        ref = fields[3]
        alt = fields[4]

        string = f"{alt} {chromosome} {position}"

        # checks if variant is an SNV
        if len(ref) == 1 and len(alt) == 1 and ref != alt:
            SNVs += 1
            results["SNVs"] += 1

            # checks if an identical variant is already in collection
            # if yes, it's a duplicate
            if string in collection:
                duplicates += 1
            # if no, it's added to collection
            else:
                collection.add(string)
                unique_SNVs += 1

            # Calculates SNV by chromosome
            if chromosome in snv_by_chrom:
                snv_by_chrom[chromosome] += 1
            else:
                snv_by_chrom[chromosome] = 1

        # checks if variant is Indel
        if len(ref) != len(alt):
            indels += 1
            results["indels"] += 1

        # gets the read depth of each variant
        # splits up the format and sample fields
        format_fields = fields[8].split(':')
        sample_fields = fields[9].split(':')
        # gets the index of DP
        dp_index = format_fields.index('DP')
        # grabs data at the index of DP in the sample fields
        dp = sample_fields[dp_index]

        # adds to the total read depth
        read_depth_total += int(dp)
        # adds to the num_variants so we can get average
        num_variants += 1

        print(f"{num_variants + intro_lines} out of {length}", end='\r')

    # formats the results dictionary and does necessary calculations
    results["read_depth_mean"] = read_depth_total / num_variants
    results["snv_by_chrom"] = snv_by_chrom
    # results["duplicates"] = duplicates
    results["concordance"] = (duplicates / unique_SNVs) * 100
    return results

def file_len(filename):
    with open(filename) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1


# simple help menu in case the user is unfamilar with topic
def help():
    print("Enter the number of the help topic:")
    print(" 1. What are SNVs?")
    print(" 2. What are Indels?")
    print(" 3. What is Read Depth?")
    print(" 4. What is SNV concordance?")

    answer = input("Enter a topic number or type q to go back: ")

    answers = [
        "An SNV is a type of genetic variation where a single nucleotide base in the DNA sequence has been altered. You can tell a variant is an SNV in a VCF file when both the Ref and Alt fields are a single letter and different. We expect a single nucleotide, and while the variant still only has one nucleotide, it has been changed. I.E. the Ref is A and the Alt is C.",
        "An indel is a type of genetic variation where nucleotides have either been added or deleted. You can tell a variant is an indel in a VCF file when the Alt field is either shorter or longer than the alt field. I.E. the Ref is ABC and the Alt is AC.",
        "Read depth is a measure of how many times a particular position in the DNA sequence has been sequenced in a given sample. It tells you how many times the DNA has been read at that specific position. In a VCF file, it is represented as DP in the VCF file.",
        "SNV concordance is the percentage of identical SNVs between two or more VCF files. They must have the same Alt on the same Chromosome at the same position."]

    while int(answer) > len(answers) or int(answer) < 0:
        answer = input(f"please enter a number between 1 and {len(answers)}")

    while answer != "q":
        print("\n")
        print(answers[int(answer) - 1])
        answer = input("\nEnter a topic number or type q to go back: ")
        while int(answer) > len(answers) or int(answer) < 0:
            answer = input(f"please enter a number between 1 and {len(answers)}")

