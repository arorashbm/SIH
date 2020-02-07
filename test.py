from maps import hospital, reverseGeocode, route, policeStation, makeUrl

lat = 34.0563442
lon = -118.3076779
rad = 3000

name_hosp, phone_hosp, pos_hosp = hospital(lat, lon, rad)

name_pol, pos_pol = policeStation(lat, lon, rad)

accident_pos, route_num = reverseGeocode(lat, lon)

address_hosp, route_num = reverseGeocode(pos_hosp[0], pos_hosp[1])

address_pol, route_num = reverseGeocode(pos_pol[0], pos_pol[1])

dist_hosp_acc = route(lat, lon, pos_hosp[0], pos_hosp[1])

dist_pol_acc = route(lat, lon, pos_pol[0], pos_pol[1])

route_url = makeUrl(address_hosp, address_pol, accident_pos)

if route_num != 0:
    accident_pos += " on "+route_num

if route_num != 0:
    address_hosp += " on "+route_num

if route_num != 0:
    address_pol += " on "+route_num

print()
print("Name of Hospital                                   :      ", name_hosp)
print("Phone number of Hospital                           :      ", phone_hosp)
print("Location of Hospital                               :      ", address_hosp)
print()
print("Name of Police Station                             :      ", name_pol)
print("Location of Police station                         :      ", address_pol)
print()
print("Accident Location                                  :      ", accident_pos)
print()
print("Distance between Hospital and Accident site        :       {}km".format(dist_hosp_acc/1000))
print("Distance between Police station and Accident site  :       {}km".format(dist_pol_acc/1000))
print()
print(route_url[0])
print()
print(route_url[1])
print()

with open("result.txt", "w") as res:
    res.write("Name of Hospital                                   :      "+name_hosp+"\n")
    res.write("Phone number of Hospital                           :      "+phone_hosp+"\n")
    res.write("Location of Hospital                               :      "+address_hosp+"\n")
    res.write("Name of Police Station                             :      "+name_pol+"\n")
    res.write("Location of Police station                         :      "+address_pol+"\n")
    res.write("Accident Location                                  :      "+accident_pos+"\n")
    res.write("Distance between Hospital and Accident site        :      {}km".format(dist_hosp_acc/1000)+"\n")
    res.write("Distance between Police station and Accident site  :      {}km".format(dist_pol_acc/1000)+"\n")
    res.write(route_url[0]+"\n")
    res.write(route_url[1]+"\n")

