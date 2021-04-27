# program name - covid_data_entry.py
# Author: Gokce Gokmen, A01258386, set C,ACIT 1515
# Date: April 26, 2021

"""
This program is designed to add new covid cases to the existing csv file
"""

import csv
import sys


def display(data_list):
    # Displays the data to be entered or saved
    print("\nThe following case data has been entered")

    for data_dictionary in data_list:

        for k, v in data_dictionary.items():
            print(v," ", end='')

        print("")

def open_file(file_name):
    # Opens existing file to read data and store as a dictionary
    try:

        data = []
        file = open(file_name, 'r')
        print("File", file_name, "exists! New data will be appended to this file!")
        decision = input("Do you want to continue [y/n] : ")

        if decision.upper() == "N":
            print("Have a good day!")
            exit()

        reader = csv.DictReader(file)

        for row in reader:
            data.append(row)

        return data

    except IOError:
        print("File not found!")
        exit()


def take_input():
    # Takes inputs from user
    date = input("\nEnter the date the case was identified [YYYY-MM-DD] : ")
    area = input("Enter the health area where the case ocurred (? for list) : ")

    if area == "?":
        print("FR - Fraser")
        print("IN - Interior")
        print("NO - Northern")
        print("OC - Out of Canada")
        print("VC - Vancouver Coastal")
        print("VI - Vancouver Island")
        area = input("Enter the health are where the case occured:")

    gender = input("Enter the date the case was identified [M,F, or U(Unknown)] : ").upper()
    age = int(input("Enter patient age : "))

    if age < 10:
        age_string = "<10"

    elif age >= 90:
        age_string = "90+"

    else:
        div = int(age / 10)
        age_string = str(div * 10) + "-" + str((div * 10) + 9)

    return date, area, gender, age_string


def format_input():
    # Converts taken inputs to dictionary
    new_data_list = []

    while True:

        date, area, gender, age_string = take_input()

        area_dict = {"FR": "Fraser", "IN": "Interior", "NO": "Northern", "OC": "Out of Canada",
                     "VC": "Vancouver Coastal", "VI": "Vancouver Island"}

        if area.upper() in area_dict.keys():
            ha = area_dict[area.upper()]
        elif area in area_dict.values():
            ha = area
        else:
            print("Wrong area! please re-enter inputs!")
            continue

        new_dict = {"Reported_Date": date, "HA": ha, "Sex": gender, "Age_Group": age_string,
                    "Classification_Reported": "Lab-diagnosed"}

        display([new_dict])

        save = input("\nEnter S to keep this case data,anything else to discard it: ")

        if save.upper() == "S":
            new_data_list.append(new_dict)

        case = input("\nDo you want to add another case [y/n] : ")

        if case.upper() == "N":
            return new_data_list


def write_to_file(file_name, data_to_write):
    # Writes to the file combined with the data entered and the data read from the file
    decision = input("\nDo you want to save changes [y/n]: ")

    if decision.upper() == "Y":
        csv_columns = ["Reported_Date", "HA", "Sex", "Age_Group", "Classification_Reported"]

        try:

            with open(file_name, 'w') as csvfile:

                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in data_to_write:
                    writer.writerow(data)

            print("Changes saved!")

        except IOError:
            print("I/O error")

    else:
        print("Changes not saved!")


def main():

    # From the command line, the file name is taken as an argument and the file extension is checked.
    # The received file is retrieved and stored in the dictionary list.
    # Data from the user is taken and a dictionary list is created.
    # Finally, these two lists are combined and written to the file.

    try:
        file_name = sys.argv[1]
    except Exception:
        print("Missing <file name> argument!")
        exit()

    if file_name.split(".")[1] != "csv":
        print("Wrong extension!")
        exit()

    file_content = open_file(file_name)

    print("\nCOVID-19 Data Entry Tool")
    print("========================")

    new_data = format_input()
    display(new_data)
    write_to_file(file_name, file_content + new_data)


main()
