import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from data_processing import load_tof_axis, load_max_N, load_delay_time, load_delay_data, init_mat



if __name__ == '__main__':
    run_folder = 'data/275 transdce_XUV_real_scan'
    t0 = -22.95
    save = True
    out_file = 'processed_data/run_275_processed.txt'
    a = init_mat(run_folder, t0)

    x = a[0,1:]
    y = a[1:,0]
    z = a[1:,1:]

    fig,ax = plt.subplots()

    ax.set_xlabel('TOF (ns)')
    ax.set_ylabel('Delay (fs)')
    ax.set_title(run_folder)
    ax.pcolormesh(x,y,z)
    cbar = plt.colorbar(ax.pcolormesh(x,y,z))

    ax.set_xlim(3580,3780)

    if save:
        np.savetxt(out_file,a, header = '# [0,1:] = TOF, [1:,0] = Delay, [1:,1:] = PES')

    plt.show()