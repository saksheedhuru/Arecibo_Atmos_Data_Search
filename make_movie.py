import os
import glob
import mysql.connector
import imageio
import pandas as pd

framerate = 5
delete_existing_bool = True

photos_dir = "photos"
base_dir = "/media/FPIBAK/"
password_path = "password/password.txt"
csv_file_path = "Movies.csv"
limit = 10
# Read in the first line
with open(password_path, "r") as file_handler:
    
    password = file_handler.readline()

mydb = mysql.connector.connect(
host="localhost",
user="atmos",
password=password,
database="atmos_data_search"
)

def main():

    cursor = mydb.cursor(dictionary=True)
    # Define query
    distinct_combinations_query = "SELECT DISTINCT Year, Month, Day, Location, Wavelength FROM atmos_data_search.Sky_Imager ORDER BY Year DESC, Month ASC, Day ASC, Location ASC, Wavelength ASC;"
    cursor.execute(distinct_combinations_query)

    distinct_combinations_results = cursor.fetchall()

    # Iterate over results, using these combinations, get all the photo paths where all 4 equal the current iteration in sql

    # Assuming you have established a connection to the MySQL database and obtained the cursor

    data_list = []
    args_list = []

    # Iterate over the distinct combinations
    for combination in distinct_combinations_results:
        result = create_movie(combination)

        if type(result) != type(""):
            # result will have either the filepath of the video (string) or a -1 integer or -2 integer
            if result < 0:
                # Add log variables when erro is found
                # Open error.log as append
                with open("errors.log", "a") as f:
                    f.write("Negative Wavelength found\n")
                    f.write("Combination:")
                    f.write(f"{combination}")
                    f.write("query:")
                    year = combination['Year']
                    month = combination['Month']
                    day = combination['Day']
                    location = combination['Location']
                    wavelength = combination['Wavelength']
                    photo_paths_query = f"SELECT FilePath FROM atmos_data_search.Sky_Imager WHERE Year = {year} AND Month = {month} AND Day = {day} AND Location = '{location}' AND Wavelength = '{wavelength}';"
                    f.write(photo_paths_query)

                continue

        new_row = {'Year': combination['Year'], 'Month': combination['Month'], 'Day': combination['Day'], 'Location': combination['Location'], 'FilePath': result, 'Wavelength': combination['Wavelength']}

        # Append row to data_list
        data_list.append(new_row)

    df = pd.DataFrame(data_list)

    # Use the to_csv() function to save the DataFrame as a CSV file
    df.to_csv(csv_file_path, index=True)



    # Close the cursor and database connection when done
    cursor.close()
    mydb.close()

# Make a function, that receives a filepath and returns the series number as an int
# Example: 
# Input: /media/FPIBAK/AOimager_2020-present/2023_Archive/jan_2023/230101/Browse/Images/ao230101sk_96.jpg
# Output: 96
def filepathNum(filepath):
    # take filename out of filepath
    filename = os.path.basename(filepath)
    # take the value, between the _ and the .
    number = filename.split("_")[-1]
    number = number.split(".")[0]
    # Turn it into integer
    number = int(number)
    # Return result
    return number


def create_movie(combination):
    cursor = mydb.cursor(dictionary=True)
    year = combination['Year']
    month = combination['Month']
    day = combination['Day']
    location = combination['Location']
    wavelength = combination['Wavelength']

    if wavelength < 0:
        return -1

    # Define the query to retrieve photo paths matching the current combination
    photo_paths_query = f"SELECT FilePath FROM atmos_data_search.Sky_Imager WHERE Year = {year} AND Month = {month} AND Day = {day} AND Location = '{location}' AND Wavelength = '{wavelength}';"

    # Execute the query
    cursor.execute(photo_paths_query)

    # Fetch all the photo paths
    photo_paths = cursor.fetchall()
    photo_paths_list = []
    rel_filelist = []
    
    # Process the photo paths
    for photo_path in photo_paths:
        photo_paths_list.append(photo_path['FilePath'].replace(base_dir,""))
    photo_paths_list.sort(key=filepathNum)

    # Then add the photos directory path to the left of the path
    # Last path turns into:
    # photos/CUimager_2015-present/2023_Archive/jun_2023/230619/Browse/Images/cu230619sk_85.jpg
    for i, rel_path in enumerate(photo_paths_list):
        rel_path = os.path.join(photos_dir, rel_path)
        photo_paths_list[i] = rel_path

    # Check if there's more than one distinct directory in listing.

    # Get a list of directories from the photos
    dir_listing = []
    for rel_path in photo_paths_list:
        # For each one, get base directory and add to list
        rel_base_dir = os.path.dirname(rel_path)
        dir_listing.append(rel_base_dir)
    distinct_dirs = set(dir_listing)
    distinct_dirs = list(distinct_dirs)

    if len(distinct_dirs) != 1:
        print("ERROR: the year, month, day, location, and wavelength images are found in more than one directory.")
        print(combination)
        return -2
    video_output_dir = distinct_dirs[0]

    # Make video output filename
    # Encode query information as a part of the filename
    filename = f"{year}_{month}_{day}_{location}_{wavelength}.mp4"
    
    # Make video output filepath
    filepath = os.path.join(video_output_dir,filename)

    # Create a list to store the image frames
    frames = []

    # Read each photo and append it to the frames list
    for photo_path in photo_paths_list:
        try:
            frames.append(imageio.imread(photo_path))
        except:
            breakpoint()
    
    # Create the video using imageio
    imageio.mimsave(filepath, frames, fps=24)  # Adjust the FPS as needed

    return filepath


main()



