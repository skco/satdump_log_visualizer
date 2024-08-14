required Python libraries installation commandline:
pip install pandas numpy matplotlib cartopy folium jinja2 Pillow skyfield requests openpyxl scipy


You need to set  values in log_parser.py ​​to your location:
OBSERVER_LAT
OBSERVER_LON 
OBSERVER_ELEVATION 


required directory structure:
main directory - run scripts files inside this directory
   logs - folder with satdump logs
   images - folder with products copied from satdump live_output
   templates - html templates 

The order in which the scripts should be run:
log_parser.py - log parser script
add_azel.py   - calculate az, el and lat,lon data
generate_summary.py - generate final 

combined_coverage.py - script for generate more combined coverage maps (snr_heatmap_cartopy.png and snr_heatmap_folium.html)

Then open fiile summary.html

additional coverage files  will be created:

images\polar_plot_all_inverted
images\polar_plot_all

example:
http://radioastro.pl/log_project20/index.html

