from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector

# import HttpResponse
# Create your views here.
def index(request): 

    mydb = mysql.connector.connect(
    host="localhost",
    user="atmos",
    password="password",
    database="atmos_data_search"
    )

    cursor = mydb.cursor(dictionary=True)
    # Define query
    query = "SELECT * FROM data_archive;"
    cursor.execute(query)

    results = cursor.fetchall()

    breakpoint()
    print(mydb)

    context = {
		"Years" : [2019, 2020, 2021, 2022, 2023],
        "Months" : ["January", "February", "March", "April", "May", "June",
                   "July","August", "September", "October", "November", "December"],
        "Days" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
        "Locations" : ["Arecibo Observatory", "Culebra"]
        	}
    # return HttpResponse("test")

    return render(request, "index.html", context)

# # create a function
# def geeks_view(request):
# 	# create a dictionary

# 	# return response
# 	return render(request, "index.html", context)
