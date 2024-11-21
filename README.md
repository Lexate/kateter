# Calibration

The calibration procedure for the system is to do a full rotation at each bend angle. The rotation angle is calculated from assuming a constant speed of rotation. This is then stored as two vectors, one representing bend and rotation and the other storing sensor values at the same point.

The zero point of the sensors does seem to drift a bit over time so calibration will probably have redone at semi regular intervals.

## Python module

*Input:* record bool, A number (2~3) of sensor inputs measured in Ohms, bend angle

*Output:* None

When record bool is true it generates and writes to a file: ```time, r1, ..., rn, bend_angle```
## Python post processor
This takes the above file and computes the rotation angle. It takes a zero value from the first points
# Structure
Data is collected via the DAQ-assistant in LabVIEW. This is then passed as doubles to a python module running under python 3.10. The python function returns two doubles representing the rotation and bend of the catheter.

As a result of running python through LabVIEW the python module does not keep state between LabVIEW iterations. This means that all state must either be handled with files or passed through LabVIEW.
## Python module
*Input:* A number (2~3) of sensor inputs measured in Ohms

*Output:* Vector of two values `[bend, rot]` represented by `[α, β]` in the spec

*Short explanation:* The input values are matched to the closest sensor data vector from the calibration data, this links to a vector representing the output.

To find the best match from the calibration data the sensor values can be represented as points in n-dimensional space where n is the number of sensors. The input data can then be mapped to the same space and a closest point calculated. (*I need to look into how to do this with vectors*)
### Calibration data format
`bend, rot, r1, ..., rn`
### Possible problems
- The output from the sensors is not linear and as such distance between points might not correspond to how close the angles are.
    - This could be solved if I linearize the input in some way. maybe by plotting a function over the data from each sensor and then giving a position in that function.
- There might be ambiguity because, depending on configuration, one set of sensor values might represent multiple angles. This is hopefully not the case but it could be mitigated by:
    - Changing sensor placement in hardware.
    - (More precise calibration)
