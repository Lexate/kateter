import numpy as np
import csv
import random
import time

def closest_point(path: str, sensors: tuple):
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
    with open("bench.csv", mode="w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for i in range(n):
            writer.writerow([random.random() * 100, random.random() * 100, random.random() * 10000, random.random() * 10000, random.random() * 10000])

def count_lines_in_csv(file_path):
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        line_count = sum(1 for row in reader)  # Count each row
    return line_count

def circle_angle(path: str):
    with open(path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')

        num_points = count_lines_in_csv(path)
        angle_increment = 360 / num_points # deg

        with open(path + ".cal", mode = 'w', newline='') as cal_file:
            writer = csv.writer(cal_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            rot = 0

            for row in reader:
                writer.writerow(row[4], rot, row[1], row[2], row[3])
                rot += angle_increment

                

if __name__ == "__main__":
    #generate_bench(5000)

    #time.sleep(1)
    
    #print(f"{closest_point('bench.csv', (-1.0, -1.0, -1.0))}")

    circle_angle("measurements/circle_copy.csv")