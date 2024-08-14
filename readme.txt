Satellite Data Processing and Visualization

This project processes satellite pass data from satdump logs, calculates azimuth and elevation, and generates various visualizations, including coverage maps and polar plots. 
The project also creates a summary HTML file with detailed information and links to all generated visualizations.

Prerequisites
Required Python Libraries
To install the required Python libraries, run the following command:

pip install pandas numpy matplotlib cartopy folium jinja2 Pillow skyfield requests openpyxl scipy

Directory Structure
Ensure that your project directory is set up as follows:

python
Skopiuj kod
main directory (root) - run all script files from this directory
│
├── logs         # Folder containing satdump log files
│
├── images       # Folder containing products copied from satdump live_output
│
├── templates    # Folder containing HTML templates for generating summary and visualizations
│
└── *.py         # Python scripts (log_parser.py, add_azel.py, generate_summary.py, combined_coverage.py)
Configuration
Before running the scripts, you need to set the observer's location in log_parser.py:

OBSERVER_LAT: Observer's latitude
OBSERVER_LON: Observer's longitude
OBSERVER_ELEVATION: Observer's elevation (in meters)
Running the Project
Follow this order to run the scripts and generate the final output:

log_parser.py: Parses the satdump logs and extracts relevant data.
add_azel.py: Calculates azimuth, elevation, and lat/lon data based on the observer's location.
generate_summary.py: Generates the final summary HTML file (summary.html) with links to visualizations.
combined_coverage.py: Generates additional combined coverage maps:
snr_heatmap_cartopy.png - SNR heatmap using Cartopy
snr_heatmap_folium.html - SNR heatmap using Folium
Viewing the Results
After running the scripts, open the summary.html file in your browser to view the generated summary and visualizations.

Additional coverage files will be created in the images directory:

images/polar_plot_all_inverted.png
images/polar_plot_all.png
Example
An example of the final output can be viewed here.

Acknowledgments
Special thanks to Antonio "t0nito" Pereira for providing test data for this project.
