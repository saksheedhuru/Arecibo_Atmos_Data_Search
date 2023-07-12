from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector

password_path = "../password/password.txt"
# Read in the first line
with open(password_path, "r") as file_handler:
    
    password = file_handler.readline()


mydb = mysql.connector.connect(
host="localhost",
user="atmos",
password=password,
database="atmos_data_search"
)
base_dir = "/media/FPIBAK/"
# import HttpResponse
# Create your views here.
def index(request): 
    
# if request.method == "POST":
    

    cursor = mydb.cursor(dictionary=True)
    # Define query
    distinct_years_query = "SELECT DISTINCT(Year) FROM Sky_Imager;"
    cursor.execute(distinct_years_query)

    distinct_years_results = cursor.fetchall()

    distinct_locations_query = "SELECT DISTINCT(Location) FROM Sky_Imager;"
    cursor.execute(distinct_locations_query)

    distinct_locations_results = cursor.fetchall()

    distinct_wavelengths_query = "SELECT DISTINCT(Wavelength) FROM Sky_Imager;"
    cursor.execute(distinct_wavelengths_query)

    distinct_wavelengths_results = cursor.fetchall()
    
    years = []
    for year in distinct_years_results:
        years.append(year["Year"])
    years.sort(reverse=True)


    locations = []
    for location in distinct_locations_results:
        locations.append(location["Location"])

    wavelengths = []
    for wavelength in distinct_wavelengths_results:
        wavelengths.append(wavelength["Wavelength"])
    wavelengths.sort()

    # Detect if its a post
    if request.method == "POST":
        
        set_year = request.POST['Year']
        set_year = int(set_year)
        set_location = request.POST['Location']
        set_wavelength = request.POST['Wavelength']
        set_wavelength = int(set_wavelength)
        
    # If its not a post set to default values
    else:
        # sets the first year of the list as default since its the first one the user will see in the dropdown
        set_year = years[0]

        # sets the first location of the list as default since its the first one the user will see in the dropdown
        set_location = locations[0]

        # sets empty wavelength of the list as default since its the first one the user will see in the dropdown
        set_wavelength = wavelengths[0]


    # change years variable to be a list of two elements:
    
    # [year_number, True/False]
    # Only one year can have a True value, which indicated the selected one
    # The year that should have the True value is the one that equals set_year
    years_TF = []
    
    for year in years:
        
        selected = False
        # Check if the current year being looked at is the same as set year
        if year == set_year:
            selected = True
        years_TF.append([year, selected])
    
    years = years_TF
    # Also propagate changes to the html, use the years to fill in dropdown, use True or False to add selected element


    # Basically the same for location
    locations_TF = []
    
    for location in locations:
        
        selected = False
        # Check if the current location being looked at is the same as set location
        if location == set_location:
            selected = True
        locations_TF.append([location, selected])
    
    locations = locations_TF

    # And for wavelength
    wavelengths_TF = []
    
    for wavelength in wavelengths:
        
        selected = False
        # Check if the current wavelength being looked at is the same as set wavelength
        if wavelength == set_wavelength:
            selected = True
        wavelengths_TF.append([wavelength, selected])
    
    wavelengths = wavelengths_TF

    
# <a href="?location=arecibo&amp;year=2023&amp;filt=5577&amp;month=Mar&amp;day=17">17</a>
    context = {
		"Years" : years,
        "Months" : ["January", "February", "March", "April", "May", "June", "July","August", "September", "October", "November", "December"],
        "January_Days" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
        "February_Days" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
        "March_Days" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
        "April_Days" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
        "May_Days" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
        "June_Days" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
        "July_Days" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
        "August_Days" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
        "September_Days" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
        "October_Days" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
        "November_Days" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
        "December_Days" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
        "Locations" : locations,
        "Wavelengths" : wavelengths
        	}
    
    # Iterate through each key in January_Days
    # Take the months out of context
    months_dict = {
        "January_Days": context["January_Days"],
        "February_Days": context["February_Days"],
        "March_Days": context["March_Days"],
        "April_Days": context["April_Days"],
        "May_Days": context["May_Days"],
        "June_Days": context["June_Days"],
        "July_Days": context["July_Days"],
        "August_Days": context["August_Days"],
        "September_Days": context["September_Days"],
        "October_Days": context["October_Days"],
        "November_Days": context["November_Days"],
        "December_Days": context["December_Days"]
    }
    
    
    month_num = 1
    # iterate through each month
    for key in months_dict.keys():
        # get all days in current year and month that have data
        # Save as a list of days
        distinct_day_location_wavelength = distinctDayOfMonth(set_year, month_num, set_location, set_wavelength)
        new_days = []
        # Iterates through each day of the month
        for day in context[key]:
            # Make a list of two elements:
            # First element is the int, representing the day
            # Second element is going to be True or False, representing if its got data
            # <a href="{% url 'next_page' %}?param1=value1&param2=value2">Go to Next Page</

            # The href woulkd be: gallery?year={year_value}&month={month_value}&day={day_value}&location={location_value}
            # Start by just changing it to gallery

            # Assigning True or False as to whether it has data or not
            if day in distinct_day_location_wavelength:
                new_element = [day, True, f"gallery?year={set_year}&month={month_num}&day={day}&location={set_location}&wavelength={set_wavelength}"]
            else:
                new_element = [day, False, "https://www.google.com/"]

            new_days.append(new_element)
        month_num = month_num + 1
        context[key] = new_days

    # return HttpResponse("test")

    return render(request, "index.html", context)

def gallery(request):
    # Extract year, month, day and location and save to variables
    set_year = request.GET['year']
    set_year = int(set_year)
    set_month = request.GET['month']
    set_month = int(set_month)
    set_day = request.GET['day']
    set_day = int(set_day)
    set_location = request.GET['location']
    set_wavelength = request.GET['wavelength']
    
    cursor = mydb.cursor(dictionary=True)
    filepath_query = f"SELECT File_Path FROM Sky_Imager WHERE Year = {set_year} AND Month = {set_month} AND Day = {set_day} AND Location = '{set_location}';"
    cursor.execute(filepath_query)

    filelist = []
    filepath_results = cursor.fetchall()
    
    for var in filepath_results:
        filelist.append(var['File_Path'])
    
    # Sort list using for loop
    filelist.sort(key=getNum)
    
    rel_filelist = []

    for filepath in filelist:
        rel_path = filepath.replace(base_dir,"photos/")
        rel_filelist.append(rel_path)
    
    grouped_rel_filelist = transform_to_groups_of_four(rel_filelist)
    context = {
        "name": "Sakshee",
        "filepaths": grouped_rel_filelist
    }
    
    
    print("Something")
    return render(request, "gallery.html", context)

def transform_to_groups_of_four(rel_filelist):
    sorted_rel_filelist = []
    group = []
    for value in rel_filelist:
        group.append(value)
        if len(group) == 4:
            sorted_rel_filelist.append(group)
            group = []
    if group:  # Append the remaining values if the length is not divisible by 4
        sorted_rel_filelist.append(group)
    return sorted_rel_filelist


def getNum(filepath):
    int_num = filepath.split("_")[-1]
    int_num = int_num.split(".")[0]
    int_num = int(int_num)
    return int_num



# # create a function
# def geeks_view(request):
# 	# create a dictionary

# 	# return response
# 	return render(request, "index.html", context)

# Make a function That will return a list of distinct days for a given month and year.
def distinctDayOfMonth(year, month, location, wavelength):

    
    cursor = mydb.cursor(dictionary=True)
    available_data_query = f"SELECT distinct Day FROM Sky_Imager WHERE Year = '{year}' AND Month = '{month}' AND Location = '{location}' AND Wavelength  = '{wavelength}';"
    cursor.execute(available_data_query)

    available_data = cursor.fetchall()
    
    dates = []
    for date in available_data:
        dates.append(date["Day"])
    dates.sort()
    return dates
