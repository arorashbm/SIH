import requests
import json

#get nearest hospital
def hospital(latitude, longnitude, radius):
    lat = latitude
    lon = longnitude
    rad = radius
    url = "https://api.tomtom.com/search/2/search/hospital.json?key=NzxUQicH4gU0siE7sSEsJnLyPJlOFjv5&lat="+str(lat)+"&lon="+str(lon)+"&radius="+str(rad)
    response = requests.get(url)
    response_dict = response.json()
    num_results = response_dict["summary"]["numResults"]
    if num_results == 0:
        name, phone, position = hospital(latitude, longnitude, radius+1000)
        return name, phone, position
    with open("json_hospital.txt", "w") as jh:
        jh.write(str(response_dict))
    score_dist = []
    results = response_dict["results"]
    for num in range(num_results):
        poi = results[num]["poi"]
        category = poi["categories"]
        if "hospital/polyclinic" in category or "health care service" in category or "public health technologies" in category:
                if "phone" in poi: 
                    result_dict = {
                        "score": results[num]["score"],
                        "dist": results[num]["dist"],
                        "num": num
                    }
                    score_dist.append(result_dict)
    min_dist = rad+1000
    if len(score_dist) > 0:
        for num in range(len(score_dist)):
            if score_dist[num]["dist"] < min_dist:
                min_dist = score_dist[num]["dist"]
                min_res = num
        min_num = score_dist[min_res]["num"]
        min_result = results[min_num]
        poi_hosp = min_result["poi"]
        name = poi_hosp["name"]
        if "phone" in poi_hosp:
            phone = poi_hosp["phone"]
        else:
            phone = "NA"
        position_dict = min_result["position"]
        position = tuple([position_dict["lat"], position_dict["lon"]])
        return name, phone, position            #return name, phone number of hospital along with a tuple containing co-ordinates of hospital
    else:
        print("No in 1000")
    
#get address from co-ordinates
def reverseGeocode(latitude, longnitude):
    lat = latitude
    lon = longnitude
    url = "https://api.tomtom.com/search/2/reverseGeocode/"+str(lat)+"%2C"+str(lon)+".json?key=NzxUQicH4gU0siE7sSEsJnLyPJlOFjv5"
    response = requests.get(url)
    response_dict = response.json()
    with open("json_reverse_geocode.txt", "w") as jh:
        jh.write(str(response_dict))
    complete_address = response_dict["addresses"][0]["address"]
    address = complete_address["freeformAddress"]
    if len(complete_address["routeNumbers"]) != 0:
        route_number = complete_address["routeNumbers"][0]
    else:
        route_number = 0
    return address, route_number        #return address of hospital

#get path length between two points
def route(latitude, longnitude, latitude_hosp, longnitude_hosp):
    lat = latitude
    lon = longnitude
    lat_hosp = latitude_hosp
    lon_hosp = longnitude_hosp
    dist = []
    url = "https://api.tomtom.com/routing/1/calculateRoute/"+str(lat_hosp)+"%2C"+str(lon_hosp)+"%3A"+str(lat)+"%2C"+str(lon)+"/json?avoid=unpavedRoads&key=NzxUQicH4gU0siE7sSEsJnLyPJlOFjv5"
    response = requests.get(url)
    response_dict = response.json()
    with open("json_route.txt", "w") as jh:
        jh.write(str(response_dict))
    route = response_dict["routes"]
    num_routes = len(route)
    for num in range(num_routes):
        length = route[num]["summary"]["lengthInMeters"]
        dist.append(length)
    return min(dist)        #return minimum distance between hospital and accident site

#get nearest police station
def policeStation(latitude, longnitude, radius):
    lat = latitude
    lon = longnitude
    rad = radius
    url = "https://api.tomtom.com/search/2/search/police.json?key=NzxUQicH4gU0siE7sSEsJnLyPJlOFjv5&lat="+str(lat)+"&lon="+str(lon)+"&radius="+str(rad)
    response = requests.get(url)
    response_dict = response.json()
    num_results = response_dict["summary"]["numResults"]
    if num_results == 0:
        name, position = policeStation(latitude, longnitude, radius+1000)
        return name, position
    with open("json_police.txt", "w") as jh:
        jh.write(str(response_dict))
    score_dist = []
    results = response_dict["results"]
    for num in range(num_results):
        category = results[num]["poi"]["categories"]
        if "police station" in category:
            result_dict = {
                "score": results[num]["score"],
                "dist": results[num]["dist"],
                "num": num
            }
            score_dist.append(result_dict)
    min_dist = rad+1000
    for num in range(len(score_dist)):
        if score_dist[num]["dist"] < min_dist:
            min_dist = score_dist[num]["dist"]
            min_res = num
    min_num = score_dist[min_res]["num"]
    min_result = results[min_num]
    poi_hosp = min_result["poi"]
    name = poi_hosp["name"]
    position_dict = min_result["position"]
    position = tuple([position_dict["lat"], position_dict["lon"]])
    return name, position                  #return name of police station along with a tuple containing its co-ordinates

#make google maps url
def makeUrl(location_hosp, location_pol, location_acc):
    location_hosp_plus = "+".join(location_hosp.split())
    location_pol_plus = "+".join(location_pol.split())
    location_acc_plus = "+".join(location_acc.split())
    
    hosp_acc = "https://www.google.com/maps/dir/?api=1&origin="+location_hosp_plus+"&destination="+location_acc_plus+"&travelmode=car"
    pol_acc = "https://www.google.com/maps/dir/?api=1&origin="+location_pol_plus+"&destination="+location_acc_plus+"&travelmode=car"
    return hosp_acc, pol_acc