""" takes a processed .txt file (generated from process.py)
applies TOF calibration and Jacobian correction using functions and parameters from tof_calib.py
saves a new .txt file with the calibrated data ({}_jac.txt)"""

import numpy as np
import matplotlib.pyplot as plt
import os

from functions import calibrate

data_path = "processed_data/run_275_processed.txt"
calib_file_path = 'calibrations/calib_params.txt'

data = np.genfromtxt(data_path)
params = np.genfromtxt(calib_file_path)

x = data[0,1:]
y = data[1:,0]
z = data[1:,1:]

eBE, calib_z = calibrate(x,z,*params)

new_mat = np.zeros((len(y)+1,len(eBE)+1))
new_mat[1:,0] = y
new_mat[0,1:] = eBE
new_mat[1:,1:] = calib_z

#outfile is datapath minus .txt + _jac.txt
base_name, ext = os.path.splitext(data_path)  # Separate the full path into base name and extension
output_path = f"{base_name}_jac{ext}"  # Append '_jac' before the extension

np.savetxt(output_path, new_mat)
if __name__ == '__main__':
    fig,ax = plt.subplots()
    ax.plot(eBE,np.sum(calib_z[0:4],axis=0))
    plt.show()


#calib file path 


