#!/usr/bin/env python3

# Import modules
import sys
import os
import datetime

# Function which calculates difference between two time points in seconds
# Function assumes t2 is after t1
def time_diff(t1, t2):
    t1 = datetime.datetime.strptime(t1, '%H:%M:%S.%f').time()
    t2 = datetime.datetime.strptime(t2, '%H:%M:%S.%f').time()
    h1, m1, s1 = t1.hour, t1.minute, t1.second
    h2, m2, s2 = t2.hour, t2.minute, t2.second
    t1_secs = s1 + 60 * (m1 + 60*h1)
    t2_secs = s2 + 60 * (m2 + 60*h2)
    return(t2_secs - t1_secs)

# Function which deducts 120 seconds from timestamp
def deduct_time(t):
    t = datetime.datetime.strptime(t, '%H:%M:%S.%f').time()
    h, m, s, ms = t.hour, t.minute, t.second, t.microsecond
    t_secs = s + 60 * (m + 60 * h)
    t_new = t_secs - 120
    new_h = str(t_new // 3600)
    new_m = str((t_new % 3600) // 60)
    new_s = str(t_new - (60 * int(new_m)) - (3600 * int(new_h)))
    if len(new_h) < 2: new_h = "0" + str(new_h)
    if len(new_m) < 2: new_m = "0" + str(new_m)
    if len(new_s) < 2: new_s = "0" + str(new_s)
    new_stamp = new_h + ":" + new_m + ":" + new_s + "." + str(ms)
    return new_stamp

# Function which creates for an input file a dictionary with individual bees as keys and recordings as entries in chronological order.
def bee_dict(file_name):
    ind_dict = {}
    if file_name.startswith("log"):
        file_path = os.path.join(data_f, file_name)
        infile = open(file_path)
        for line in infile:
            if line.startswith("20"):
                line_list = line.strip("\n").split(",")
                time = deduct_time(line_list[0].split(" ")[1])
                record = (time, line_list[2], line_list[9],
                              line_list[10], line_list[11])
                if ind_dict.get(line_list[3]) is None:
                    ind_dict.update({line_list[3]: [record]})
                else:
                    ind_dict.get(line_list[3]).append(record)
    else:
        print("File name "+ file_name +" unexpected.")
    return ind_dict
                    
# Function which can filter a file dictionary, user can fill in time in seconds
def filter_records(file_name, ar_dep, dep_ar):
    ar_dep = int(ar_dep)
    dep_ar = int(dep_ar)
    filt_dict = {}
    ind_dict = bee_dict(file_name)
    for bee in ind_dict:
        bee_records = ind_dict.get(bee)
        if len(bee_records) == 1:
            filt_dict.update({bee: bee_records})
        else:
            new_records = [bee_records[0]]
            for r in bee_records[1:len(bee_records) - 1]:
                if "Unknown"in r:
                    i = bee_records.index(r)
                    if bee_records[i - 1][2] == "Departing" and bee_records[i + 1][2] == "Departing":
                        if time_diff(bee_records[i - 1][0], bee_records[i][0]) >= dep_ar \
                          and time_diff(bee_records[i][0], bee_records[i + 1][0]) >= ar_dep:
                            new_records.append((r[0],r[1],"Arriving",r[3],r[4]))
                        else:
                            new_records.append(r)
                    elif bee_records[i - 1][2] == "Arriving" and bee_records[i + 1][2] == "Arriving":
                        if time_diff(bee_records[i - 1][0], bee_records[i][0]) >= ar_dep \
                          and time_diff(bee_records[i][0], bee_records[i + 1][0]) >= dep_ar:
                            new_records.append((r[0],r[1],"Departing",r[3],r[4]))
                        else:
                            new_records.append(r)
                    else:
                        new_records.append(r)
                else:
                    new_records.append(r)
            new_records.append(bee_records[-1])
            filt_dict.update({bee: new_records})
    return filt_dict
    
# Function which writes the dictionary to file
def write_out(file_name, ar_dep, dep_ar):
    if file_name.endswith(".csv"):
        name_split = file_name.strip(".csv")
        file_path = os.path.join(data_f, name_split + "_corrected.csv")
        outfile = open(file_path, "w")
        outfile.write("UID,Timestamp,ReaderID,Status,Ant1,Ant2\n")
        filt_dict = filter_records(file_name, ar_dep, dep_ar)
        for b in filt_dict:
            write_records = filt_dict.get(b)
            for w in write_records:
                outfile.write(b + "," + ",".join(w) + "\n")
    else:
        print("File format " + file_name + " unexpected.")

if __name__ == "__main__":
    # Get user variables
    data_f = sys.argv[1]
    ar_dep = sys.argv[2].split(",")[0]
    dep_ar = sys.argv[2].split(",")[1]

    # Get list of input files
    file_list = os.listdir(data_f)
    for f in file_list:
        write_out(f, ar_dep, dep_ar)