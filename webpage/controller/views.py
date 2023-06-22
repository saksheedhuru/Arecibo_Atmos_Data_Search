from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector

# import HttpResponse
# Create your views here.
def index(request): 

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

    locations = []
    for location in distinct_locations_results:
        locations.append(location["Location"])

    context = {
		"Years" : years,
        "Months" : ["January", "February", "March", "April", "May", "June",
                   "July","August", "September", "October", "November", "December"],
        "January_Days" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
        "Locations" : locations
        	}
    # return HttpResponse("test")

    return render(request, "index.html", context)

# # create a function
# def geeks_view(request):
# 	# create a dictionary

# 	# return response
# 	return render(request, "index.html", context)
