import csv
import os
import glob
from fplHelper import *

"""
summary_dict = {}


# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Relative path to the folder
folder_path = os.path.join(script_dir, "fplFiles")

# Find all files in the folder with the .igc extension
fpl_files = glob.glob(os.path.join(folder_path, "*.fpl"))


# Print the number of .igc files found
print(f"Number of .fpl files in {folder_path}: {len(fpl_files)}")

file_name = fpl_files[0]

# Read the file and store each line as an element in a list
with open(file_name, 'r') as file:
    fpl_data = [line.strip() for line in file.readlines()]

"""


def read_fpl_and_return(file_name):
    # Read the file and store each line as an element in a list
    with open(file_name, 'r') as file:
        fpl_data = [line.strip() for line in file.readlines()]    
    
    print(f'Analyzing {file_name}')
    #set up dicts
    summary_dict = {}
    summary_dict['Task'] = {}
    summary_dict['Wind'] = {}
    summary_dict['Thermals'] = {}
    summary_dict['Waves'] = {}
    summary_dict['High clouds'] = {}
    summary_dict['Notam'] = {}
    summary_dict['Task legs'] = {}


    ##########################  Task Related
    filename_with_extension = os.path.basename(file_name)
    filename, extension = os.path.splitext(filename_with_extension)
    summary_dict['Task'][' '] = ' '
    summary_dict['Task']['Name'] = filename
    summary_dict['Task']['Landscape'] = get_line(fpl_data, 'Landscape=')
    summary_dict['Task']['Timing'] = get_line(fpl_data, 'TaskDate=')
    summary_dict['Task']['Timing'] = excel_date_to_mmddyyyy(summary_dict['Task']['Timing'])
    summary_dict['Task']['Plane class'] = get_line(fpl_data, 'Class=')
    summary_dict['Task']['Race in'] = get_line(fpl_data, 'RaceStartDelay=')
    summary_dict['Task']['Race in'] = hours_to_minutes(summary_dict['Task']['Race in'])
    summary_dict['Task']['Time window'] = get_line(fpl_data, 'StartTimeWindow=')
    summary_dict['Task']['Time window'] = hours_to_minutes(summary_dict['Task']['Time window'])
    summary_dict['Task']['Start time [hours]'] = get_line(fpl_data, 'StartTime=')
    summary_dict['Task']['Legs'] = str(int(get_line(fpl_data, 'Count=')) - 2)
    summary_dict['Task']['Takeoff'] = get_line(fpl_data, 'TPName0=')
    summary_dict['Task']['Start height'] = get_line(fpl_data, 'TPAltitude1=')
    summary_dict['Task']['Start height'] = meters_to_feet(summary_dict['Task']['Start height'])

    ##todo add legs and add finish


    ##########################  Wind Related
    
    summary_dict['Wind'][' '] = ' '
    summary_dict['Wind']['Direction'] = get_line(fpl_data, 'WindDir=')
    summary_dict['Wind']['Direction'] = str(int(float(summary_dict['Wind']['Direction'])))
    summary_dict['Wind']['Direction variation'] = get_line(fpl_data, 'WindDirVariation=')
    summary_dict['Wind']['Direction variation'] = wind_variation_map(summary_dict['Wind']['Direction variation'])
    summary_dict['Wind']['Speed'] = get_line(fpl_data, 'WindSpeed=')
    summary_dict['Wind']['Speed'] = mps_to_kts(summary_dict['Wind']['Speed'])
    summary_dict['Wind']['Variation'] = get_line(fpl_data, 'WindSpeedVariation=')
    summary_dict['Wind']['Variation']  = wind_variation_map(summary_dict['Wind']['Variation'] )
    summary_dict['Wind']['Turbulence'] = get_line(fpl_data, 'WindTurbulence=')
    summary_dict['Wind']['Turbulence'] = turbulence_map(summary_dict['Wind']['Turbulence'])



    ##########################  Thermals Related

    #base =
    #print(base)
    #summary_dict['Thermals']['Temperature'] = get_line(fpl_data, 'ThermalsTemp=')
    summary_dict['Thermals'][' '] = ' '
    Thermals_Temperature = get_line(fpl_data, 'ThermalsTemp=')
    #summary_dict['Thermals']['Dew point'] = get_line(fpl_data, 'ThermalsDew=')
    Thermals_Dewpoint = get_line(fpl_data, 'ThermalsDew=')
    summary_dict['Thermals']['Cloud base'] = get_cloud_base_height(Thermals_Temperature, Thermals_Dewpoint)
    summary_dict['Thermals']['Cloud base variation'] = get_line(fpl_data, 'ThermalsTempVariation=')
    summary_dict['Thermals']['Cloud base variation'] = wind_variation_map(summary_dict['Thermals']['Cloud base variation'])
    summary_dict['Thermals']['Inversion height'] = get_line(fpl_data, 'ThermalsInversionheight=')
    summary_dict['Thermals']['Inversion height'] = meters_to_feet(summary_dict['Thermals']['Inversion height'])
    summary_dict['Thermals']['Cloud depth'] = calculate_inversion_depth(summary_dict['Thermals']['Inversion height'], summary_dict['Thermals']['Cloud base'])
    summary_dict['Thermals']['Strength'] = get_line(fpl_data, 'ThermalsStrength=')
    summary_dict['Thermals']['Strength'] = thermals_strength_map(summary_dict['Thermals']['Strength'])
    summary_dict['Thermals']['Strength variation'] = get_line(fpl_data, 'ThermalsStrengthVariation=')
    summary_dict['Thermals']['Strength variation'] = thermals_variation_map(summary_dict['Thermals']['Strength variation'])
    summary_dict['Thermals']['Width'] = get_line(fpl_data, 'ThermalsWidth=')
    summary_dict['Thermals']['Width'] = thermals_width_map(summary_dict['Thermals']['Width'])
    summary_dict['Thermals']['Width variation'] = get_line(fpl_data, 'ThermalsWidthVariation=')
    summary_dict['Thermals']['Width variation'] = wind_variation_map(summary_dict['Thermals']['Width variation'])
    summary_dict['Thermals']['Activity'] = get_line(fpl_data, 'ThermalsActivity=')
    summary_dict['Thermals']['Activity'] = thermals_activity_map(summary_dict['Thermals']['Activity'])
    summary_dict['Thermals']['Turbulence'] = get_line(fpl_data, 'ThermalsTurbulence=')
    summary_dict['Thermals']['Turbulence'] = turbulence_map(summary_dict['Thermals']['Turbulence'])
    summary_dict['Thermals']['Flats activity'] = get_line(fpl_data, 'ThermalsFlatsActivity=')
    summary_dict['Thermals']['Flats activity'] = thermals_flats_activity_map(summary_dict['Thermals']['Flats activity'])
    summary_dict['Thermals']['Streeting'] = get_line(fpl_data, 'ThermalsStreeting=')
    summary_dict['Thermals']['Streeting'] = wind_variation_map(summary_dict['Thermals']['Streeting'])
    summary_dict['Thermals']['Randomize?'] = get_line(fpl_data, 'RandomizeWeatherOnEachFlight=')
    summary_dict['Thermals']['Randomize?'] = checked_not_checked_map(summary_dict['Thermals']['Randomize?'])

    ##########################  Waves Related
    
    summary_dict['Waves'][' '] = ' '
    summary_dict['Waves']['Speed'] = get_line(fpl_data, 'WindUpperSpeed=')
    summary_dict['Waves']['Speed'] = mps_to_kts(summary_dict['Waves']['Speed'])
    summary_dict['Waves']['Stability'] = "'"+get_line(fpl_data, 'WavesStability=') + '/10'
    summary_dict['Waves']['Moisture'] = get_line(fpl_data, 'WavesMoisture=') + '0%'


    ##########################  High Clouds Related

    summary_dict['High clouds'][' '] = ' '
    summary_dict['High clouds']['Coverage'] = "'"+get_line(fpl_data, 'HighCloudsCoverage=') + '/8'


    ##########################  Notam Related
    
    summary_dict['Notam'][' '] = ' '
    #Start options
    summary_dict['Notam']['Start type'] = get_line(fpl_data, 'StartType=')
    summary_dict['Notam']['Start type'] = start_type_map(summary_dict['Notam']['Start type'])
    summary_dict['Notam']['Start height'] = get_line(fpl_data, 'StartHeight=')
    summary_dict['Notam']['Start height'] = meters_to_feet(summary_dict['Notam']['Start height'])   
    # Realism
    summary_dict['Notam']['Plane icons range'] = get_line(fpl_data, 'IconsVisibleRange=')
    summary_dict['Notam']['Plane icons range'] = km_to_nmi(summary_dict['Notam']['Plane icons range'])
    summary_dict['Notam']['Thermal helpers range'] = get_line(fpl_data, 'ThermalHelpersRange=')
    summary_dict['Notam']['Thermal helpers range'] = km_to_nmi(summary_dict['Notam']['Thermal helpers range'])
    summary_dict['Notam']['Turnpoint helpers range'] = get_line(fpl_data, 'TurnpointHelpersRange=')
    summary_dict['Notam']['Turnpoint helpers range'] = km_to_nmi(summary_dict['Notam']['Turnpoint helpers range'])
    summary_dict['Notam']['Allow PDA'] = get_line(fpl_data, 'AllowPDA=')
    summary_dict['Notam']['Allow PDA'] = checked_not_checked_map(summary_dict['Notam']['Allow PDA'])
    summary_dict['Notam']['Allow realtime scoring'] = get_line(fpl_data, 'AllowRealtimeScoring=')
    summary_dict['Notam']['Allow realtime scoring'] = checked_not_checked_map(summary_dict['Notam']['Allow realtime scoring'])
    summary_dict['Notam']['Allow External View'] = get_line(fpl_data, 'AllowExternalView')
    summary_dict['Notam']['Allow External View'] = checked_not_checked_map(summary_dict['Notam']['Allow External View'])
    summary_dict['Notam']['Allow Padlock View'] = get_line(fpl_data, 'AllowPadlockView')
    summary_dict['Notam']['Allow Padlock View'] = checked_not_checked_map(summary_dict['Notam']['Allow Padlock View'])
    summary_dict['Notam']['Allow Smoke'] = get_line(fpl_data, 'AllowSmoke')
    summary_dict['Notam']['Allow Smoke'] = checked_not_checked_map(summary_dict['Notam']['Allow Smoke'])
    summary_dict['Notam']['Allow Plane Recovery'] = get_line(fpl_data, 'AllowPlaneRecovery')
    summary_dict['Notam']['Allow Plane Recovery'] = checked_not_checked_map(summary_dict['Notam']['Allow Plane Recovery'])
    summary_dict['Notam']['Allow Height Recovery'] = get_line(fpl_data, 'AllowHeightRecovery')
    summary_dict['Notam']['Allow Height Recovery'] = checked_not_checked_map(summary_dict['Notam']['Allow Height Recovery'])
    summary_dict['Notam']['Allow Midair Collision Recovery'] = get_line(fpl_data, 'AllowMidairCollisionRecovery')
    summary_dict['Notam']['Allow Midair Collision Recovery'] = checked_not_checked_map(summary_dict['Notam']['Allow Midair Collision Recovery'])
    #penalties
    summary_dict['Notam']['Cloud flying'] = "'"+get_line(fpl_data, 'PenaltyCloudFlying') + ' p'
    summary_dict['Notam']['Plane Recovery'] = "'"+get_line(fpl_data, 'PenaltyPlaneRecovery') + ' p'
    summary_dict['Notam']['Height Recovery'] = "'"+get_line(fpl_data, 'PenaltyHeightRecovery') + ' p'
    summary_dict['Notam']['Wrong Window Entrance'] = "'"+get_line(fpl_data, 'PenaltyWrongWindowEnterance') + ' p'
    summary_dict['Notam']['Window Collision'] = "'"+get_line(fpl_data, 'PenaltyWindowCollision') + ' p'
    summary_dict['Notam']['Penalty Zone Entrance'] = "'"+get_line(fpl_data, 'PenaltyPenaltyZoneEnterance') + ' p'
    summary_dict['Notam']['Thermal Helpers'] = "'"+get_line(fpl_data, 'PenaltyThermalHelpers') + ' p'


    ##########################  Task legs Related

    start_elevation_m = get_line(fpl_data, 'TPPosZ0')
    start_elevation_ft = meters_to_feet(start_elevation_m)
    summary_dict['Task']['Cloud base above start height'] = calculate_cloud_base_above_start(start_elevation_ft.split()[0],summary_dict['Thermals']['Cloud base'].split()[0],summary_dict['Task']['Start height'].split()[0])
    summary_dict['Task']['Task distance'] = calculate_total_distance(fpl_data)
    summary_dict['Task']['Task legs'] = str(int(get_line(fpl_data, 'Count=')) - 2)


    # Extract just the filename without path and extension
    base_filename = os.path.splitext(os.path.basename(file_name))[0]

    """
    # Flatten the dictionary
    flat_data = flatten_dict(summary_dict)

    # Write to CSV
    csv_file_path = 'output.csv'
    fieldnames = ['Variable', base_filename]

    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write data
        for key, value in flat_data.items():
            if key.lower() != 'key':
                writer.writerow({'Variable': key, base_filename: value})


    """
    print('')
    print('Task',summary_dict['Task'])
    print('')
    print('Wind',summary_dict['Wind'])
    print('')
    print('Thermals',summary_dict['Thermals'])
    print('')
    print('Waves',summary_dict['Waves'])
    print('')
    print('High clouds',summary_dict['High clouds'])
    print('')
    print('Notam',summary_dict['Notam'])
    print('')
    print('Task legs',summary_dict['Task legs'])

    return summary_dict
