import os
import pandas as pd
from skyfield.api import Loader, Topos, wgs84
from datetime import datetime, timedelta
import requests

# Initialize the Loader and timescale from Skyfield
load = Loader('.')
ts = load.timescale()

# Constants for TLE file URL and path
TLE_URL = 'https://celestrak.org/NORAD/elements/weather.txt'
TLE_FILE_PATH = 'weather.txt'

# Global variables for observer's location
OBSERVER_LAT = 40.766136  # Latitude of the observer
OBSERVER_LON = -8.387586  # Longitude of the observer
OBSERVER_ELEVATION = 330  # Elevation of the observer in meters

# Function to download the TLE file from the specified URL
def download_tle_file(url, file_path):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    with open(file_path, 'wb') as file:
        file.write(response.content)

# Function to check if a file is older than a specified number of days
def is_file_older_than_days(file_path, days=3):
    if not os.path.exists(file_path):
        return True  # Return True if the file doesn't exist
    file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
    return datetime.now() - file_mod_time > timedelta(days=days)

# Download the TLE file if it is older than the specified number of days
if is_file_older_than_days(TLE_FILE_PATH, days=3):
    download_tle_file(TLE_URL, TLE_FILE_PATH)

# Load the TLE data from the file
satellites = load.tle_file(TLE_FILE_PATH)

# Function to calculate azimuth, elevation, distance, latitude, and longitude for a given satellite and observer location
def calculate_azimuth_elevation(satellite, observer_lat, observer_lon, observer_elevation, timestamp):
    observer_location = Topos(latitude_degrees=observer_lat, longitude_degrees=observer_lon, elevation_m=observer_elevation)
    time = ts.utc(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second)
    difference = satellite - observer_location
    topocentric = difference.at(time)
    alt, az, distance = topocentric.altaz()
    lat, lon = wgs84.latlon_of(satellite.at(time))
    return az.degrees, alt.degrees, distance.km, lat.degrees, lon.degrees

# Function to add azimuth, elevation, distance, latitude, and longitude to a DataFrame
def add_azimuth_elevation_distance(df, satellites):
    results = []  # List to store results for each row
    for _, row in df.iterrows():
        try:
            timestamp = row['Timestamp']
            satellite_name = row['satellite']
            # Replace the last occurrence of "-" with a space in the satellite name
            last_dash_index = satellite_name.rfind('-')
            if last_dash_index != -1:
                satellite_name = satellite_name[:last_dash_index] + ' ' + satellite_name[last_dash_index + 1:]
            satellite = next((sat for sat in satellites if sat.name == satellite_name), None)

            if satellite is not None and pd.notna(timestamp):
                azimuth, elevation, distance_km, lat, lon = calculate_azimuth_elevation(satellite, OBSERVER_LAT, OBSERVER_LON, OBSERVER_ELEVATION, timestamp)
            else:
                azimuth = None
                elevation = None
                distance_km = None
                lat = None
                lon = None

            results.append({'Azimuth': azimuth, 'Elevation': elevation, 'Distance': distance_km, 'lat': lat, 'lon': lon})
        except Exception as e:
            print(f"Error calculating azimuth and elevation for row {row}: {e}")
            results.append({'Azimuth': None, 'Elevation': None, 'Distance': None, 'lat': None, 'lon': None})

    return df.assign(**pd.DataFrame(results))

# Main function
def main():
    df = pd.read_excel('parsed_log_data.xlsx')

    enriched_df = add_azimuth_elevation_distance(df, satellites)
    enriched_df.to_excel('final_processed_log_data_enriched.xlsx', index=False)

# Entry point of the script
if __name__ == '__main__':
    main()
