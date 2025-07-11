import requests
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
key = "9fcd52c4-a3f8-4a10-af66-6d5bb03e7fad"

def geocoding(location, key):
    while location == "":
        location = input("Ingresa la ubicación otra vez: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q":location, "limit": "1", "key":key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) !=0:
        json_data = requests.get(url).json()
        lat = (json_data["hits"][0]["point"]["lat"])
        lng = (json_data["hits"][0]["point"]["lng"])
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country=""
        
        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state=""
        
        if len(state) !=0 and len(country) !=0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) !=0:
            new_loc = name + ", " + country
        else:
            new_loc = name
        
        print("Geocoding API URL for " + new_loc + " (Location Type: " + value + ")\n" + url)
    else:
        lat="null"
        lng="null"
        new_loc=location
        if json_status != 200:
            print("Geocode API status: " + str(json_status) + "\nError message: " + json_data["message"])
    return json_status,lat,lng,new_loc

while True:
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículos disponibles en Graphhopper:")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Auto, Bicicleta, A pie.")
    print("O presiona 's' para salir")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    profile=["Auto", "Bicicleta", "A pie"]
    vehicle = input("Ingresa un perfil de vehículo de la lista anterior:  ")
    if vehicle == "s":
        break
    elif vehicle in profile:
        if vehicle == "Auto":
            vehicle = "car"
        elif vehicle == "Bicicleta":
            vehicle == "Bike"
        elif vehicle == "A pie":
            vehicle == "foot"
    else: 
        vehicle = "car"
        print("No se ha introducido un perfil de vehículo válido. Utilizando el perfil del vehículo: 'auto'.")
    loc1 = input("Ubicación de inicio: ")
    if loc1 == "quit" or loc1 == "q":
        break
    orig = geocoding(loc1, key)
    print(orig)

    loc2 = input("Ubicación de destino: ")
    if loc2 == "quit" or loc2 == "q":
        break
    dest = geocoding(loc2, key)
    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op="&point="+str(orig[1])+"%2C"+str(orig[2])
        dp="&point="+str(dest[1])+"%2C"+str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key":key, "vehicle":vehicle, "locale":"es"}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)
        print("=================================================")
        print("Ruta de direcciones desde " + orig[3] + " hacia " + dest[3] + " en " + vehicle)
        print("=================================================")
        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"])/1000/1.61
            km = (paths_data["paths"][0]["distance"])/1000
            sec = int(paths_data["paths"][0]["time"]/1000%60)
            min = int(paths_data["paths"][0]["time"]/1000/60%60)
            hr = int(paths_data["paths"][0]["time"]/1000/60/60)
            print("Distancia recorrida: {0:.2f} millas / {1:.2f} km".format(miles, km))
            print("Duración del viaje:  {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("=================================================")
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.2f} km / {2:.2f} millas )".format(path, distance/1000, distance/1000/1.61))
            print("=============================================")
        else:
            print("Error message: " + paths_data["message"])
            print("*************************************************")
