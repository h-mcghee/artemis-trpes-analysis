# Artemis Code

For processing time-resolved photoelectron data at the ARTEMIS facility

## Data Structure

process.py takes a run folder and t0 (stage position) to generate tof / delay matrix

### Data structure

Run folder (e.g "275 transdce_XUV_real_scan") contains subdirectories (N = 20, N = 40 etc) which are the cumulatively saved photoelectron counts. 

The full data set is therefore the max N file (in this example, N = 1152)

Within each N directory is the pixel to TOF conversion file (TDC Time.tsv), and a .tsv file for each stage delay position (eg -22.98000.tsv).

For each delay file, the photoelectron counts are found in the first column. 

From these files, process.py:

* converts pixel to TOF times from "TDC Time.tsv"
* Generates a list of delay stage position in mm (from the filename) and converts to delay time in fs. This requires the estimated t0 stage position (must be entered manually)
* Takes the photoelectron counts and generates a tof/delay matrix (using the file for the maximum number of cycles). This is plotted and saved in the "processed_runs" directory for future analysis.

### Example usage

The data folder contains an example run from a previous experiment:

McGhee, Henry G., et al. "Ultrafast photochemical processes in 1, 2-dichloroethene measured with a universal XUV probe." *Physical Chemistry Chemical Physics* 26.45 (2024): 28406-28416.

Only
