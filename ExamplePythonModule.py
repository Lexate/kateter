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


def main(r1: float, r2: float, r3: float):
    import csv
    from datetime import datetime

    #bend = 0
    #rot = 0

    #r_margin = 20 # +- Ohm
    #z_threshold = 100 # Ohm

    #r1_zero = 4500 # Ohm
    #r2_zero = 4050 ##4200 # Ohm
    #r3_zero = 0 # Ohm

    #r1_dif = r1_zero - r1
    #r2_dif = r2_zero - r2
    #r3_dif = r3_zero - r3

    with open("C:/Users/lexa/Documents/circle.csv", mode="a", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
        writer.writerow([datetime.now(), r1, r2, r3])
    #if r_margin > abs(r1_dif) and r_margin > abs(r2_dif): # No deflection
    #    rot = 999 
    #elif r1_dif < -r_margin and r2_dif > r_margin:  # 0 deg and 90 deg
    #    if abs(r1_dif) > z_threshold:
    #        rot = 0 
    #    else:
    #        rot = 90
    #elif r1_dif > r_margin and r2_dif < -r_margin:  # 270 deg
    #    rot = 270
    #elif r1_dif > r_margin and r2_dif > r_margin:   # 180 deg
    #    rot = 180

    return (rot, bend)

if __name__ == "__main__":
    stepthrough()