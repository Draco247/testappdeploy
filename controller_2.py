from datetime import time
import re
import time
import requests

from flask import Flask, request, flash, redirect, render_template, url_for

app = Flask(__name__)

app.secret_key = 'the random string'

@app.route("/", methods=['GET', 'POST']) # When the controller receives a request
def getServer(): 
    server = request.args.get('server') # It will first check what server the request is coming from by checking the query
    widget_location = request.args.get('widget') # this will check what side the widget should appear
    name = request.args.get('name') # The name of the hotel
    address = request.args.get('address') # The address of the hotel
    debug = request.args.get('debug') # The address of the hotel
    #print("Server: ", server, "was chosen") # TESTING PURPOSES

    if len(name) != 0 and len(address) != 0 and len(server) != 0: # If the EU server was in the query then it will do the following
        time_start = time.time() # FOR TESTING PURPOSES
        
        price = pick_server()
        #print(price)
        split_price = price.split("-") # This will split up the return value from the web scraper server and will divide them into separate elements in a list
        print(split_price) # FOR TESTING PURPOSES
        price_booking = split_price[0] # We know that price_booking is for booking.com because that is how it was configured in the web scraper. This is same for the other 2 hotels below
        price_hotels = split_price[1].replace(".", ",") # Hotels.com for some reason uses "." instead of "," for their prices
        price_expedia = split_price[2]
        """
        flash(price_hotels, 'hotels') # This will assign the price_hotels value to hotels. So when hotels is called in the html code, the price for hotels will appear. This is same for the other 2 hotels below
        flash(price_booking, 'booking')
        flash(price_expedia, 'expedia')
        """
        just_price_booking = ""
        just_price_hotels = ""
        just_price_expedia = ""
        # Testing
        if server == "EU":
            just_price_booking = price_booking.split(" ")[1] # FOR TESTING PURPOSES - As the EU at least returns out the name, price and time taken
            just_price_hotels = price_hotels.split(" ")[1] + " " + price_hotels.split(" ")[2] # FOR TESTING PURPOSES
            just_price_expedia = price_expedia.split(" ")[1] + " "+ price_expedia.split(" ")[2] # FOR TESTING PURPOSES
        elif server == "UK":
            just_price_booking = price_booking.split(" ")[1] # FOR TESTING PURPOSES - As the EU at least returns out the name, price and time taken
            just_price_hotels = price_hotels.split(" ")[1]
            just_price_expedia = price_expedia.split(" ")[1]
        elif server == "US":
            just_price_booking = price_booking.split(" ")[1] # FOR TESTING PURPOSES - As the EU at least returns out the name, price and time taken
            just_price_booking = just_price_booking.replace("US", "")
            just_price_hotels = price_hotels.split(" ")[1]
            just_price_expedia = price_expedia.split(" ")[1]

        if "N/A" in just_price_expedia:
            just_price_expedia = "N/A"
        if "N/A" in just_price_hotels or just_price_hotels == "":
            just_price_hotels = "N/A"
        if "N/A" in just_price_booking:
            just_price_booking = "N/A"
        flash(just_price_hotels, 'hotels') # This will assign the price_hotels value to hotels. So when hotels is called in the html code, the price for hotels will appear. This is same for the other 2 hotels below
        flash(just_price_booking, 'booking')
        flash(just_price_expedia, 'expedia')
        
        time_end = time.time() # FOR TESTING PURPOSES
        print("Time elapsed: ", time_end - time_start, "Server: ", server) # FOR TESTING PURPOSES

        if debug == "true":
            return price
        elif debug != "true":
            if widget_location == "left": # IF the widget_location was left then the widget will appear left,
                return redirect(url_for('widget_template2'))
            elif widget_location != "left": # otherwise it will appear right by default
                return redirect(url_for('widget_template'))
    else:
        return "Enter hotel details and server details correctly"
        
def pick_server(): # picking server
    server = request.args.get('server') # It will first check what server the request is coming from by checking the query

    # Setting the IP addresses
    #eu_server = "http://20.56.90.161:5678/" # IP address for the EU web scraper server (Currently in the Netherlands) OLD
    eu_server = "http://52.236.132.185:5678/" # IP address for the EU web scraper server 
    uk_server = "http://20.68.20.177:5678/" # IP address for the UK web scraper server
    us_server = "http://40.85.164.118:5678/" # IP address for the US web scraper server

    # The details will get sent to the web scraper server
    name = request.args.get('name') # The name of the hotel
    address = request.args.get('address') # The address of the hotel
    check_in = request.args.get('check_in') # The check in date of the hotel
    check_out = request.args.get('check_out') # The check out date of the hotel
    rooms = request.args.get('rooms') # The number of rooms required 
    adults = request.args.get('adults') # The number of adults 
    children = request.args.get('children') # The number of chidlren 
    ages = request.args.get('ages')

    # Setting default values if none are added
    if len(rooms) == 0 or len(rooms) is None:
        rooms = 1   
    if len(adults) == 0:
        adults = 1
    if len(children) == 0:
        children = 0

    # Creating a new query that will get sent to the web scraper
    if server == "EU":
        url_req = eu_server + "?name=" + name + "&address=" + address + "&check_in=" + check_in + "&check_out=" + check_out + "&rooms=" + rooms + "&adults=" + adults + "&children=" + children + "&ages=" +ages
    elif server == "UK":
        url_req = uk_server + "?name=" + name + "&address=" + address + "&check_in=" + check_in + "&check_out=" + check_out + "&rooms=" + rooms + "&adults=" + adults + "&children=" + children + "&ages=" +ages
    elif server == "US":
        url_req = us_server + "?name=" + name + "&address=" + address + "&check_in=" + check_in + "&check_out=" + check_out + "&rooms=" + rooms + "&adults=" + adults + "&children=" + children + "&ages=" +ages
    hotel_results = requests.get(url_req)
    
    return hotel_results.text # This will return the result from the web scraper back to the getServer function

@app.route("/widget_template", methods=['GET', 'POST']) # This function is to output the widget at the bottom right side
def widget_template():
    return render_template('main2.html')

@app.route("/widget_template2", methods=['GET', 'POST']) # This function is to output the widget at the bottom left side
def widget_template2():
    return render_template('main2_left.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5678) # host 0.0.0.0 allows the program to run on all ip addresses, debug=True allows the script return errors on the console if there are any

