import numpy as np
import glob as glob
import re
import os
import pandas as pd

def load_tof_axis(run_folder):
    """
    Load the TOF axis from the TDC Time.tsv file in the given folder.

    Args:
        folder_path (str): The path of the folder containing the TDC Time.tsv file.

    Returns:
        np.array: The TOF axis in ns.
    """
    return np.genfromtxt(f"{run_folder}/TDC Time.tsv")

def load_max_N(run_folder):
    """ 
    Find the directory with the maximum N value in the given path (run folder).

    Args:
        path (str): The path of the run folder.

    Returns:
        str: The path of the directory with the maximum N value

    """
    # Use glob to find all directories that contain 'N=' in their names
    n_directories = glob.glob(f'{run_folder}/*N=*')

    # Extract the N values and find the directory with the maximum N value
    max_n_dir = max(n_directories, key=lambda d: int(re.search(r'N=(\d+)', d).group(1)))

    print(f"Found directory with maximum N value: {max_n_dir}")

    return max_n_dir

def load_delay_time(file_path, t0):
    """
    Converts delay position in mm for a given file into delay time in fs (the delay position is extracted from the file name).

    Args:
        file_path (str): Path to the file (e.g., 'data/275 transducer_XUV_real_scan/N=600/-21.450000.tsv').
        t0 (float): t0 value for the run. This is the estimated delay position in mm at which the pump and probe beams overlap.

    Returns:
        float: Delay time in femtoseconds (fs).
    """
    # Extract the base file name and remove the extension
    file_name = os.path.basename(file_path)
    base_name, _ = os.path.splitext(file_name)

    # Attempt to convert the base name to a float (delay position in mm)
    try:
        delay_pos = float(base_name)
    except ValueError as e:
        raise ValueError(f"Failed to extract delay position from file name '{file_name}'.") from e

    # Speed of light in fs/mm
    SPEED_OF_LIGHT_FS_MM = 0.000299792458

    # Calculate delay time in fs
    delay_time = 2 * (delay_pos - t0) / SPEED_OF_LIGHT_FS_MM

    return delay_time


def load_delay_data(run_folder,t0):
    """ 
    Load the delay data from the given run folder.

    Args:
        run_folder (str): The path of the run folder.
        t0 (float): t0 value for the run.

    Returns:
        pd.DataFrame: A DataFrame containing the delay times (fs) and photoelectron spectra
    """

    max_n_dir = load_max_N(run_folder)
    flist = (glob.glob(f'{max_n_dir}/*'))
    if not flist:
        raise FileNotFoundError(f"No files found in {max_n_dir}")

    delay = []
    pes = []
    for f in flist:
        delay.append(load_delay_time(f,t0))
        pes.append(np.genfromtxt(f)[:,0]) # data is in FIRST column of .tsv file

    df = pd.DataFrame({'delay':delay,
                        'pes':pes})
    if len(delay) != 0:
        df = df.sort_values(by='delay').reset_index(drop = True)
    else:
        pass

    return df

def init_mat(run_folder,t0):
    """ 
    Initialize a matrix containing the TOF axis, delay times, and photoelectron spectra.

    Args:
        run_folder (str): The path of the run folder.
        t0 (float): t0 value for the run.

    Returns:
        np.array: A matrix containing the TOF axis, delay times, and photoelectron spectra.
        first row contains TOF axis, first column contains delay times, and the rest of the matrix contains photoelectron spectra.
    """

    tof = load_tof_axis(run_folder)

    df = load_delay_data(run_folder,t0)

    x = np.array(tof)
    y = np.array(df.delay)
    z = np.vstack(df.pes)

    a = np.pad(z,((1,0),(1,0)),mode = 'constant')
    a[1:,0] = y
    a[0,1:] = x

    return a

def tof2eBE(x, hv, s, t0, E0):
    m = 9.11e-31 #mass of electron in kg
    e = 1.602e-19 #elementary charge in Coulombs
    #need to convert Joules to eV, so multiply by e
    return hv - ((1/e)*0.5 * m * ((s / ((x-t0)*1e-9))**2)) - E0

def jacobian(x,hv,s,t0,E0):
    """returns jacobian correction factor for tof to eBE conversion"""
    m = 9.11e-31 #mass of electron in kg
    e = 1.602e-19
    J = ((e*((x - t0)*1e-9)**3) / (m*(s**2)))
    return J

def calibrate(x,y,hv,s,t0,E0,jac = True):
    """ performs tof calibration with jacobian
    returns x axis and jacobian corrected y axis"""
    eBE = tof2eBE(x,hv,s,t0,E0)
    mask = (x > t0) & (eBE >0)
    if jac:
        J = jacobian(x,hv,s,t0,E0)
    else:
        J = np.ones_like(x)
    if y.ndim == 1:
        return eBE[mask], y[mask]*J[mask]
    else:
        return eBE[mask], y[:,mask]*J[mask]


