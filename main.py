from functions import *
import os.path


def main():
    print(f"Welcome to the VCF Analyzer. This tool is generate the following details about one or more VCF files: ")
    print(f" 1. Number of SNVs")
    print(f" 2. Number of Indels")
    print(f" 3. Number of SNVs on each chromosome")
    print(f" 4. The mean read depth")
    print(f" 5. The SNV concordance (if you analyze 2 or more files)")

    firstAnswer = input("Type 'start' to begin or 'help' to get more info on VCF files: ")

    if firstAnswer.lower() == 'help':
        help()

    print("\nLet's analyze some files!")
    analyzeVCF()

    response = input("Do you have more files to analyze? (y/n): ")

    while response.lower() != 'n' and response.lower() != 'no' and response.lower() != 'y' and response.lower() != 'yes':
        print("I do not understand your response.")
        response = input("Do you have more files to analyze? (y/n): ")

    while response.lower() == 'y' or response.lower() == 'yes':
        print("\n")
        analyzeVCF()
        response = input("Do you have more files to analyze? (y/n): ")
        while response.lower() != 'n' and response.lower() != 'no' and response.lower() != 'y' and response.lower() != 'yes':
            print("I do not understand your response.")
            response = input("Do you have more files to analyze? (y/n): ")

    if response.lower() == 'n' or response.lower() == 'no':
        print("Goodbye")
        return


main()