import pandas as pd
import multiprocessing as mp
import os
import subprocess
import time
from astropy.io import fits

abbr_months =["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
years = ["2020", "2021", "2022", "2023"]
locations = {"ao": 'Arecibo Observatory', "cu": 'Culebra'}

listing_path = "Interferometer_listing.txt"
full_archive_path = "Interferometer_full_archive.txt"
csv_file_path = "Interferometer.csv"
run_find = True
def main():
    # Example find command: 
    # find /media/FPIBAK/AOimager_2020-present/2020_Archive -type f -name "*sk*.jpg" -not -name "*thumb*" > /share/s3453g1/keysha/Development/FACT/Sakshee/listing.txt
    # find {directory} -type f -name "*sk*.jpg" -not -name "*thumb*" > {output_file_path}

    # The directory of the find command should be a list of strings that denote the path
    # output filepath should be defined as a global variable
    # directories = ['/media/FPIBAK/AOimager_2020-present/2020_Archive', '/media/FPIBAK/AOimager_2020-present/2021_Archive',
    #              '/media/FPIBAK/AOimager_2020-present/2022_Archive', '/media/FPIBAK/AOimager_2020-present/2023_Archive'] 

    # Open folders file as read
    with open(full_archive_path, 'r') as file:
        lines = file.readlines()
    
    directories = []
    for line in lines:
        line = line[0:-1]
        directories.append(line)
    
    total_dict_list = []
    for directory in directories:
        
        command = f"find {directory} -type f -name '*sk *.fit' -not -name '*thumb*' > {listing_path}"
        print("Running find command ...")
        if run_find == True:
            subprocess.run(command, shell=True)
        print("Finished find command")


        # Open the file
        with open(listing_path, 'r') as file:
            i = 0
            start_time = time.time()
            args_list = []
            pool = mp.Pool(processes=mp.cpu_count()*2)
            
            # Read and print each line
            for line in file:
                line = line[0:-1]
                args_list.append(line)
                

                # df = df.append(row, ignore_index=True)
                i = i + 1

                if i % 1000 == 0:
                    # submit whatever is in args_list
                    results = pool.map(makeRow, args_list)
                    # results = []
                    # for arg in args_list:
                    #     results.append(makeRow(arg))
                    # Add the results to df
                    total_dict_list.extend(results)
                    # reset args_list
                    args_list = []
                    

                    end_time = time.time()
                    print(i)
                    print(end_time - start_time)
                    start_time = time.time()
            # Check if args list is not an empty list
            if args_list != []:
                # If it is not an empty list, submit through multiprocessing, submit whatever is in args_list
                results = pool.map(makeRow, args_list)
                # results = []
                # for arg in args_list:
                #     results.append(makeRow(arg))
                # Add the results to df
                total_dict_list.extend(results)
                # reset args_list
                args_list = []
        df = pd.DataFrame(total_dict_list)
        # Use the to_csv() function to save the DataFrame as a CSV file
        df.to_csv(csv_file_path, index=True)

def makeRow(filepath):

    # Take infomration, assuming the folder stucture is the same
    # split filepath by "/"
    split_filepath_list = filepath.split("/")

    # turn year into int
    year_month_day = split_filepath_list[6]
    year = year_month_day[0:2]
    year = int(year)
    year = 2000 + year

    # turn month into int
    month = year_month_day[2:4]
    month = int(month)

    # turn day into int
    day = year_month_day[4:6]
    day = int(day)

    # create location    
    name_imager = split_filepath_list[-1]
    name = name_imager[0:2]
    location = locations[name]

    # Get FW_POS in fit file from hdul header in astropy
    hdul = fits.open(filepath)
    wavelength = hdul[0].header["FW_POS"]

    # Create a new row
    new_row = {'Year': year, 'Month': month, 'Day': day, 'Location': location, 'FilePath': filepath, 'Wavelength': wavelength}

    return new_row

main()