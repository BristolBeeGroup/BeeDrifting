#!/usr/bin/env python3

# Import modules
import os
import sys
from correct_files import time_diff

# Function to extract date from file name, returns "None" if wrong file (format)
def get_date(file_name):
    if file_name.startswith("log_"):
        name_split = file_name.split("_")
        date_info = "_".join(name_split[1:4])
        return date_info

# Function to put the data from all supplied "_corrected.csv" files in one dictionary
def compile_dict(data_folder):
    file_list = os.listdir(data_folder)
    all_dict = {}
    for f in file_list:
        if f.endswith("_corrected.csv"):
            date_info = get_date(f)
            file_path = os.path.join(data_folder, f)
            infile = open(file_path)
            for line in infile:
                if not line.startswith("UID"):
                    line_list = line.strip("\n").split(",")
                    if all_dict.get(line_list[0]) is None:
                        bee_record = {"readers": [line_list[2]], 
                                      "records": [(date_info, line_list[1], line_list[2], line_list[3])]}
                        all_dict.update({line_list[0]: bee_record})
                    else:
                        bee_dict = all_dict.get(line_list[0])
                        if line_list[2] not in bee_dict.get("readers"):
                            bee_dict.get("readers").append(line_list[2])
                        bee_dict.get("records").append((date_info, line_list[1], line_list[2], line_list[3]))
    return all_dict

# Function to extract the foraging trips out of a dictionary and write them to file
# Drifters are marked in a column
def for_trips(all_dict, min_duration, max_duration):
    outfile = open("foraging_trips.csv", "w")
    outfile.write("Date,Bee,ReaderDeparting,ReaderArriving,Start,End,Duration,Drifter\n")
    for individual in all_dict:
        ind_dict = all_dict.get(individual)
        if len(ind_dict.get("readers")) > 1:
            drifter = "yes"
        else:
            drifter = "no"
        rec_list = ind_dict.get("records")
        for r in rec_list[0:len(rec_list)-1]:
            if r[3] == "Departing" and rec_list[rec_list.index(r) + 1][3] == "Arriving":
                # Test if departing and arriving on same day:
                if r[0] == rec_list[rec_list.index(r) + 1][0]:
                    duration = time_diff(r[1], rec_list[rec_list.index(r) + 1][1])
                    if int(min_duration) <= duration <= int(max_duration):
                        outfile.write(r[0] + "," + individual + "," + r[2] + "," +
                                      rec_list[rec_list.index(r) + 1][2] + "," +
                                      r[1] + "," + rec_list[rec_list.index(r) + 1][1] +
                                      "," + str(duration) + "," + drifter + "\n")
    outfile.close()

if __name__ == "__main__":
    # Get user variables
    data_folder = sys.argv[1]
    min_duration = sys.argv[2]
    max_duration = sys.argv[3]
    all_dict = compile_dict(data_folder)
    for_trips(all_dict, min_duration, max_duration)           