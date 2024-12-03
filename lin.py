# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
# ]
# ///
import numpy as np
import csv
import random
import time

def closest_point(path: str, sensors: tuple):
    """Takes in a path to a calibration file and a tuple of sensors values and outputs
    the angle of the closest calibration value in the provided file.
    """
    t1 = time.time_ns()
    b = np.array(sensors)

    #              (distance, (bend, rot))
    angles = []
    n_samples = 5

    # Create an array of all angle pairs with their distance to the sensor values
    with open(path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')

        for row in reader:
            a = np.array([float(x) for x in row[2:]])

            distance = np.linalg.norm(a - b)
        
            angles.append((distance, tuple([float(row[0]), float(row[1])])))
    
    # Sort array by distance
    closest = sorted(angles, key=lambda x: x[0])[:n_samples]

    # Average bend and rotation values
    bend_av = 0
    rot_av = 0

    for p in closest:
        bend_av += p[1][0]
        rot_av += p[1][1]
    
    bend_av = bend_av / n_samples
    rot_av = rot_av / n_samples

    print(f"total_time: {time.time_ns() - t1} ns")
    return (bend_av, rot_av)

def closest_point_bad(path: str, sensors: tuple):
    """Takes in a path to a calibration file and a tuple of sensors values and outputs
    the angle of the closest calibration value in the provided file.
    """
    t1 = time.time_ns()
    b = np.array(sensors)

    closest_dist = 100000000000
    closest_ang = (0, 0)
    distance = 0
    with open(path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')

        for row in reader:
            a = np.array([float(x) for x in row[2:]])

            distance = np.linalg.norm(a - b)

            if distance < closest_dist:
                closest_dist = distance
                closest_ang = tuple([float(row[0]), float(row[1])])
    
    print(f"total_time: {time.time_ns() - t1} ns")
    return closest_ang

def generate_bench(n: int):
    """Generates a test file (bench.csv) of `n: int` random values for testing the 
    performance of `closest_point()`
    """
    with open("bench.csv", mode="w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for i in range(n):
            writer.writerow([random.random() * 100, random.random() * 100, random.random() * 10000, random.random() * 10000, random.random() * 10000])

def count_lines_in_csv(file_path):
    """Returns the number of lines in the provided csv file"""
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        line_count = sum(1 for row in reader)  # Count each row
    return line_count

def circle_angle(path: str):
    """Takes a recording of one rotation at continous speed at a specified "bend" angle 
    and returns a file with calculated angles for rotation in the format expected by
    `closest_point`
    """
    with open(path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')

        num_points = count_lines_in_csv(path)
        angle_increment = 360 / num_points # deg

        with open(path + ".cal", mode = 'w', newline='') as cal_file:
            writer = csv.writer(cal_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            rot = 0

            for row in reader:
                writer.writerow([row[4], rot, row[1], row[2], row[3]])
                rot += angle_increment

def zero_zero(path: str):
    """Takes the recording of the zero position of the sensors and outputs
    a file in the format expected by `closest_point` with rotation set to 
    zero
    """
    with open(path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        rot = 0

        with open(path + ".cal", mode = 'w', newline='') as cal_file:
            writer = csv.writer(cal_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for row in reader:
                writer.writerow([row[4], rot, row[1], row[2], row[3]])

def norm_cal(cal_path: str, zero_path: str):
    ####### Calc average zero #########
    num_zero = count_lines_in_csv(zero_path)

    r1_zav = 0
    r2_zav = 0
    r3_zav = 0

    with open(zero_path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')

        for row in reader:
            r1_zav += float(row[2])
            r2_zav += float(row[3])
            r3_zav += float(row[4])

    r1_zav = r1_zav / num_zero
    r2_zav = r2_zav / num_zero
    r3_zav = r3_zav / num_zero

    ####### Calc cal width #########
    r1_min = 100000000
    r1_max = 0
    r2_min = 100000000
    r2_max = 0
    r3_min = 100000000
    r3_max = 0
    with open(cal_path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')

        for row in reader:
            if float(row[2]) > r1_max:
                r1_max = float(row[2])
            if float(row[2]) < r1_min:
                r1_min = float(row[2])

            if float(row[3]) > r2_max:
                r2_max = float(row[3])
            if float(row[3]) < r2_min:
                r2_min = float(row[3])

            if float(row[4]) > r3_max:
                r3_max = float(row[4])
            if float(row[4]) < r3_min:
                r3_min = float(row[4])

    r1_width = abs(r1_min - r1_max)
    r2_width = abs(r2_min - r2_max)
    r3_width = abs(r3_min - r3_max)

    ###### write normalized data to file ######
    with open(cal_path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')

        with open(cal_path + ".norm", mode = 'w', newline='') as cal_file:
            writer = csv.writer(cal_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
            for row in reader:
                #writer.writerow([row[0], row[1], 
                #                 (float(row[2]) - r1_zav) / r1_width, 
                #                 (float(row[3]) - r2_zav) / r2_width, 
                #                 (float(row[4]) - r3_zav) / r3_width
                #                 ])
                writer.writerow([row[0], row[1], 
                                 (float(row[2]) - r1_min) / r1_width, 
                                 (float(row[3]) - r2_min) / r2_width, 
                                 (float(row[4]) - r3_min) / r3_width
                                 ])
    
    print(f"r1_max: {r1_max}, r2_max: {r2_max}, r3_max: {r3_max}")
    print(f"r1_min = {r1_min} \nr2_min = {r2_min} \nr3_min = {r3_min}")
    print(f"r1_zav = {r1_zav} \nr2_zav = {r2_zav} \nr3_zav = {r3_zav}")
    print(f"r1_w = {r1_width} \nr2_w = {r2_width} \nr3_w = {r3_width}")



if __name__ == "__main__":
    zero_zero("Calibration/deg0.csv")
    circle_angle("Calibration/deg15_1.csv")
    circle_angle("Calibration/deg15_2.csv")
    circle_angle("Calibration/deg15_3.csv")
    circle_angle("Calibration/deg15_4.csv")

    circle_angle("Calibration/deg30_1.csv")
    circle_angle("Calibration/deg30_2.csv")
    circle_angle("Calibration/deg30_3.csv")
    circle_angle("Calibration/deg30_4.csv")

    circle_angle("Calibration/deg45_1.csv")
    circle_angle("Calibration/deg45_2.csv")
    circle_angle("Calibration/deg45_3.csv")
    circle_angle("Calibration/deg45_4.csv")
    
    #norm_cal("Calibration/cal.csv", "Calibration/Cal_1/deg0.csv.cal")
    #norm_cal("Calibration/cal2.csv", "Calibration/deg0.csv.cal")
    norm_cal("Calibration/cal4.csv", "Calibration/deg0.csv.cal")

    print(closest_point("C:/Users/lexa/Documents/Kateter/Calibration/cal3.csv.norm", (0.3, 0.8, 0.5)))
    print(closest_point_bad("C:/Users/lexa/Documents/Kateter/Calibration/cal3.csv.norm", (0.3, 0.8, 0.5)))
