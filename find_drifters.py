#!/usr/bin/env python3

# Import modules
import os
import sys
from extract_foraging_trips import compile_dict

# This function puts all the drifters in a new dictionary
def get_drifters(data_folder):
    drift_dict = {}
    all_dict = compile_dict(data_folder)
    for bee in all_dict:
        bee_dict = all_dict.get(bee)
        if len(bee_dict.get("readers")) > 1:
            drift_dict.update({bee: bee_dict})
    return drift_dict

# This function writes all drifter activity to file
def write_to_file(drift_dict):
    outfile = open("drifter_activity.csv", "w")
    outfile.write("UID,Date,Timestamp,ReaderID,Status\n")
    for d in drift_dict:
        act_list = drift_dict.get(d).get("records")
        for act in act_list:
            outfile.write(d + "," + ",".join(act) + "\n")
    outfile.close()
        
if __name__ == "__main__":
    # Get user variables
    data_folder = sys.argv[1]
    write_to_file(get_drifters(data_folder))