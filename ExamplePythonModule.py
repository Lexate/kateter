# It seems like LabView only calls the function that has been specified and as such we don't have in memory state if we want to run 
# the function in a loop.
import csv
import time

def stepthrough():
    with open("C:/Users/lexa/Documents/Kateter/measurements/rotation_test_1.csv", mode="r") as csv_file:
        reader = csv.reader(csv_file, delimiter = ',')

        for row in reader:
            if row[0][0] == '#':
                continue

            rot, bend = main(float(row[1]), float(row[2]), 0)
            
            print(f"rot: {rot}, bend: {bend}, resistance: {', '.join(row)}")
            #time.sleep(0.1)
            with open("C:/Users/lexa/Documents/Kateter/measurements/rot_t1_decode.csv", mode="a", newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
                writer.writerow([row[0], row[1], row[2], rot])


def main(r1: float, r2: float, r3: float, bend: float):
    import csv
    from datetime import datetime
    import numpy as np
    rot = 0

    with open("C:/Users/lexa/Documents/Kateter/deg45.csv", mode="a", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
        writer.writerow([datetime.now(), r1, r2, r3, bend])

    return (bend, rot)

if __name__ == "__main__":
    #stepthrough()
    main(0,0,0)