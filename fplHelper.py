from datetime import datetime, timedelta
import math
import re

def get_line(lines, desired_key):
    found_index = None

    for index, line in enumerate(lines):
        if desired_key in line:
            found_index = index
            break

    if found_index is not None:
        key_value_pair = lines[found_index].split("=")
        if len(key_value_pair) == 2:
            result = key_value_pair[1]
            return result.strip()  # Return the text after "=" (trimmed of leading/trailing whitespace)
        else:
            return "Invalid format for key-value pair."
    else:
        return "Key not found in the list."

def excel_date_to_mmddyyyy(excel_date):
    # Excel date starts from January 1, 1900
    base_date = datetime(1899, 12, 30)  # Excel erroneously considers 1900 as a leap year, so we subtract 2 days

    # Calculate the number of days from the base date
    delta_days = timedelta(days=int(excel_date))

    # Obtain the datetime object
    result_datetime = base_date + delta_days

    # Format the datetime as mm/dd/yyyy, stripping off leading zeros for month and day
    result_formatted = result_datetime.strftime('%m/%d/%Y').lstrip("0").replace("/0", "/")

    return result_formatted

# Define a custom key function to extract the substring between the last "\\" and ".fpl"
def get_sort_key(file_path):
    return file_path.rsplit('\\', 1)[-1][:-4]  # Extract the substring and remove ".fpl"

# Define a custom key function to extract the day number from the file name
def get_day_number(file_path):
    match = re.search(r'_day_(\d+)-', file_path)
    return int(match.group(1)) if match else 0

def hours_to_minutes(decimal_hours):
    minutes = float(decimal_hours) * 60
    return str(int(minutes))


def meters_to_feet(meters):
    meters = float(meters)
    feet = meters * 3.28084
    feet = int(round(feet,0))
    feet_str = str(feet) + ' ft'
    return feet_str

def km_to_nmi(km):
    km = float(km)
    nmi = km * 0.539957
    nmi = int(round(nmi,0))
    nmi_str = str(nmi) + ' nm'
    return nmi_str

def calculate_cloud_base_above_start(start_elev, cloud_base, start_height):
    start_elev = int(start_elev.split()[0])
    cloud_base = int(cloud_base.split()[0])
    start_height = int(start_height.split()[0])
    print('start_elev',start_elev)
    print('cloud_base',cloud_base)
    print('start_height',start_height)
    cb_above_start = .5*start_elev + cloud_base - start_height
    cb_above_start = int(cb_above_start)
    print('cb_above_start',cb_above_start)
    cb_above_start_str = str(cb_above_start) + ' ft'
    return cb_above_start_str

def calculate_inversion_depth(inversion_height, cloud_base):
    inversion_height = int(inversion_height.split()[0])
    cloud_base = int(cloud_base.split()[0])
    
    depth = inversion_height - cloud_base
    depth_str = str(depth) + ' ft'
    return depth_str
    

def mps_to_kts(wind_speed_mps):
    # Convert string to float (assuming wind_speed_mps is a string)
    wind_speed_mps = float(wind_speed_mps)

    # Conversion factor: 1 m/s = 1.94384 knots
    wind_speed_kts = wind_speed_mps * 1.94384
    
    wind_speed_kts = round(wind_speed_kts,0)

    # Format the result as a string with ' kts' appended
    result_string = f"{wind_speed_kts:.0f} kts"

    return result_string


def get_cloud_base_height(T_C, DP_C):
    # Given convergence rate
    CR = 4.33  # Modify this if needed
    T_C = float(T_C)
    DP_C = float(DP_C)
    # Convert Celsius to Fahrenheit
    T = (T_C * 9/5) + 32
    DP = (DP_C * 9/5) + 32
    
    # Calculate Temperature Dew Point Spread (TDS)
    TDS = T - DP
    
    # Calculate the height of the cloud base
    height_of_cloud_base = (TDS / CR) * 1000
    
    height_of_cloud_base = str(int(height_of_cloud_base))
    
    height_of_cloud_base_format = f"{height_of_cloud_base} ft"
    
    return height_of_cloud_base_format


def get_distance(x1, y1, x2, y2):
    """Calculate the Euclidean distance between two points (x1, y1) and (x2, y2)."""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calculate_total_distance(lines):
    """Calculate the total distance between teleportation points."""
    count_line = get_line(lines, 'Count')
    if count_line.isdigit():
        count = int(count_line)
        total_distance = 0

        for i in range(1, count -1):
            x_key = f'TPPosX{i}'
            y_key = f'TPPosY{i}'
            
            x1 = float(get_line(lines, x_key))
            y1 = float(get_line(lines, y_key))

            x2 = float(get_line(lines, f'TPPosX{i+1}'))
            y2 = float(get_line(lines, f'TPPosY{i+1}'))

            distance = get_distance(x1, y1, x2, y2)
            total_distance += distance
            
        total_distance_nmi = round(total_distance * 0.000539957,1)
        total_distance_nmi_str = str(total_distance_nmi) + ' nm'
        return total_distance_nmi_str
    else:
        return "Invalid 'Count' value in the file."


def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)






def wind_variation_map(value):
    enum = {
        '0':'None',
        '1':'Low',
        '2':'Medium',
        '3':'High'
        }
    enum_value = enum.get(value)
    return enum_value
    
def turbulence_map(value):
    enum = {
        '0':'None',
        '1':'Light',
        '2':'Moderate',
        '3':'Strong',
        '4':'Severe'
        }
    enum_value = enum.get(value)
    return enum_value    
    
    
def checked_not_checked_map(value):
    enum = {
        '0':'No',
        '1':'Yes'
        }
    enum_value = enum.get(value)
    return enum_value       
    
def thermals_strength_map(value):
    enum = {
        '0':'Very weak',
        '1':'Weak',
        '2':'Moderate',
        '3':'Strong',
        '4':'Very strong'
        }
    enum_value = enum.get(value)
    return enum_value  
    
def thermals_variation_map(value):
    enum = {
        '0':'None',
        '1':'Very low',
        '2':'Low',
        '3':'Medium',
        '4':'High',
        '5':'Very high'
        }
    enum_value = enum.get(value)
    return enum_value      
    
    
def thermals_width_map(value):
    enum = {
        '0':'Very narrow',
        '1':'Narrow',
        '2':'Normal',
        '3':'Wide',
        '4':'Very wide'
        }
    enum_value = enum.get(value)
    return enum_value     
    
def thermals_activity_map(value):
    enum = {
        '0':'None',
        '1':'Very low',
        '2':'Low',
        '3':'Normal',
        '4':'High'
        }
    enum_value = enum.get(value)
    return enum_value      
 
 
def thermals_flats_activity_map(value):
    enum = {
        '0':'Very low',
        '1':'Low',
        '2':'Normal',
        '3':'High'
        }
    enum_value = enum.get(value)
    return enum_value  

def start_type_map(value):
    enum = {
        '0':'Aerotow',
        '1':'Winch',
        '2':'Airborne'
        }
    enum_value = enum.get(value)
    return enum_value  