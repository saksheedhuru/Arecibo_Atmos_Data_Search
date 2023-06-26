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

# import HttpResponse
# Create your views here.
def index(request): 
    
# if request.method == "POST":
    

    cursor = mydb.cursor(dictionary=True)
    # Define query
    distinct_years_query = "SELECT DISTINCT(Year) FROM data_archive;"
    cursor.execute(distinct_years_query)

    distinct_years_results = cursor.fetchall()

    distinct_locations_query = "SELECT DISTINCT(Location) FROM data_archive;"
    cursor.execute(distinct_locations_query)

    distinct_locations_results = cursor.fetchall()

    

    
    years = []
    for year in distinct_years_results:
        years.append(year["Year"])
    years.sort(reverse=True)


    locations = []
    for location in distinct_locations_results:
        locations.append(location["Location"])
    # Detect if its a post
    if request.method == "POST":
        
        set_year = request.POST['Year']
        set_year = int(set_year)
        set_location = request.POST['Location']
        set_wavelength = request.POST['Wavelength']

        
    # If its not a post set to default values
    else:
        # sets the first year of the list as default since its the first one the user will see in the dropdown
        set_year = years[0]

        # sets the first location of the list as default since its the first one the user will see in the dropdown
        set_location = locations[0]

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
        "Locations" : locations
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
        distinct_days = distinctDayOfMonth(set_year, month_num, set_location)
        new_days = []
        # Iterates through each day of the month
        for day in context[key]:
            # Make a list of two elements:
            # First element is the int, representing the day
            # Second element is going to be True or False, representing if its got data

            # Assigning True or False as to whether it has data or not
            if day in distinct_days:
                new_element = [day, True]
            else:
                new_element = [day, False]

            new_days.append(new_element)
        month_num = month_num + 1
        context[key] = new_days

    # return HttpResponse("test")

    return render(request, "index.html", context)

# # create a function
# def geeks_view(request):
# 	# create a dictionary

# 	# return response
# 	return render(request, "index.html", context)

# Make a function That will return a list of distinct days for a given month and year.
def distinctDayOfMonth(year, month, location):

    
    cursor = mydb.cursor(dictionary=True)
    available_data_query = f"SELECT distinct Day FROM data_archive WHERE Year = '{year}' AND Month = '{month}' AND Location = '{location}';"
    cursor.execute(available_data_query)

    available_data = cursor.fetchall()
    
    dates = []
    for date in available_data:
        dates.append(date["Day"])
    dates.sort()
    return dates
