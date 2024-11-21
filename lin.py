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

if __name__ == "__main__":
    zero_zero("Calibration/deg0.csv")
    circle_angle("Calibration/deg15_1.csv")
    circle_angle("Calibration/deg15_2.csv")
    circle_angle("Calibration/deg15_3.csv")

    circle_angle("Calibration/deg30_1.csv")
    circle_angle("Calibration/deg30_2.csv")
    circle_angle("Calibration/deg30_3.csv")
    circle_angle("Calibration/deg30_4.csv")

    circle_angle("Calibration/deg45_1.csv")
    circle_angle("Calibration/deg45_2.csv")
    circle_angle("Calibration/deg45_3.csv")
    circle_angle("Calibration/deg45_4.csv")
    circle_angle("Calibration/deg45_5.csv")