# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "matplotlib",
#     "numpy",
# ]
# ///
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import csv

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

n = 100

ax.set_title("Kalibrerings punkter")

ax.set_xlabel('r1')
ax.set_ylabel('r2')
ax.set_zlabel('r3')

zdeg = mpatches.Patch(color=(114/255, 135/255, 253/255), label='0°')
ftdeg = mpatches.Patch(color=(64/255, 160/255, 43/255), label='15°')
tdeg = mpatches.Patch(color=(230/255, 69/255, 83/255), label='30°')
ffdeg = mpatches.Patch(color=(136/255, 57/255, 239/255), label='45°')
ax.legend(handles=[zdeg, ftdeg, tdeg, ffdeg])

with open("Calibration/cal3.csv.norm", mode='r', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')

    colour = (0, 0, 0)

    for row in reader:
        match float(row[0]):
            case 0:
                colour = [(114/255, 135/255, 253/255)] # lavender
            case 15:
                colour = [(64/255, 160/255, 43/255)] # green
            case 30:
                colour = [(230/255, 69/255, 83/255)] # maroon
            case 45:
                colour = [(136/255, 57/255, 239/255)] # mauve

        print(f"{float(row[2])}, {float(row[3])}, {float(row[4])}")
        ax.scatter(float(row[2]), float(row[3]), float(row[4]), marker='o', c=colour)

fig.savefig("output.jpg", dpi=1000)