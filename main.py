# It seems like LabView only calls the function that has been specified and as such we don't have in memory state if we want to run 
# the function in a loop.
import csv
import time

def stepthrough(path: str):
    """This function steps through a file of sensor values and writes the coresponding 
    output from main to a file.
    """
    with open(path, mode="r") as csv_file:
        reader = csv.reader(csv_file, delimiter = ',')

        for row in reader:
            if row[0][0] == '#':
                continue

            rot, bend = main(float(row[1]), float(row[2]), 0)
            
            print(f"rot: {rot}, bend: {bend}, resistance: {', '.join(row)}")

            with open(path + ".output", mode="a", newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
                writer.writerow([row[0], row[1], row[2], rot])


def cal(r1: float, r2: float, r3: float, bend: float, start_stop: bool):
    """Takes sensor values as well as a value for the "bend" / deflection of the katheter 
    and writes this to a file in the format expected by `circle_angle()` in lin.py 
    """
    import csv
    from datetime import datetime
    import numpy as np
    rot = 0

    with open(f"C:/Users/lexa/Documents/Kateter/Calibration/deg{int(bend)}.csv", mode="a", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
        writer.writerow([datetime.now(), r1, r2, r3, bend, start_stop])

    return (bend, rot)

def main(r1: float, r2: float, r3: float):
    """Takes sensor values in the same order as calibrated and outputs the bend and rotation
    of the catheter. To change the calibration values used or multiple that the rotation rounds 
    to change the variables at the begining of the method.
    """
    import lin
    path = "C:/Users/lexa/Documents/Kateter/Calibration/cal.csv"
    rot_multiple = 90

    (bend, rot) = lin.closest_point(path, (r1, r2, r3))

    rot = round(rot / rot_multiple) * rot_multiple

    return (bend, rot)

def main_norm(r1: float, r2: float, r3: float):
    """Takes sensor values in the same order as calibrated and outputs the bend and rotation
    of the catheter. To change the calibration values used or multiple that the rotation rounds 
    to change the variables at the begining of the method.
    """
    import lin
    path = "C:/Users/lexa/Documents/Kateter/Calibration/cal.csv.norm"
    rot_multiple = 90
    
    r1_zav = 4339.790551957599 
    r2_zav = 4521.036211813887 
    r3_zav = 4718.461220826446
    r1_w = 200.89433800000006 
    r2_w = 121.8990759999997 
    r3_w = 31.675459999999475

    (bend, rot) = lin.closest_point(path, ((r1 - r1_zav) / r1_w, (r2 - r2_zav) / r2_w, (r3 - r3_zav) / r3_w))

    rot = round(rot / rot_multiple) * rot_multiple

    return (bend, rot)

if __name__ == "__main__":
    pass