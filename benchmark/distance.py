from datetime import datetime
import googlemaps
import json
import os
gmaps = googlemaps.Client(key='AIzaSyCNtIajO-Xwpocu9ARrah2khQF-tG8vWok')

# input list of unique_name of origins separated by comma
origins = input("Enter the unique_name of origins separated by comma: ").split(
    ',')
# Then, convert the unique_name to place_id by searching places directory
# and use the place_id as origin
# In my project folder there is a folder named "places" which contains folder of each place type
# and each place type folder contains files of unique_name of places in the format of "unique_name.json"
# in the json file there is a key named "place_id" which contains the place_id of the place
# So, I can use the place_id as origin
# For example, I have a file named "multiplan_center.json" in the "shopping_mall" folder
# which contains the place_id of Multiplan Center
# So, I can use the place_id as origin
# Now write code to convert unique_name to place_id
# Then, use the place_id as origin

origin_place_ids = []
for i, origin in enumerate(origins):
    if origin == "home":
        with open(f"places/home.json", 'r') as file:
            place = json.load(file)
            # Then, replace the unique_name with place_id
            origin_place_ids.append(f"place_id:{place['place_id']}")
        continue

    flag = False
    # First search in which type the place is. So, go through each folder in the places directory
    for folder in os.listdir("places"):
        # Check if folder is folder or not
        if not os.path.isdir(f"places/{folder}"):
            continue
        elif f"{origin}.json" in os.listdir(f"places/{folder}"):
            # Then, open the json file and get the place_id
            with open(f"places/{folder}/{origin}.json", 'r') as file:
                place = json.load(file)
                # Then, replace the unique_name with place_id
                origin_place_ids.append(f"place_id:{place['place_id']}")
            flag = True
            break
    if not flag:
        print(
            f"Place with unique_name {origin} not found. Please check the unique_name and try again.")
        exit()
# input list of unique_name of destinations separated by comma
destinations = input(
    "Enter the unique_name of destinations separated by comma: ").split(',')
# Then, convert the unique_name to place_id by searching places directory
# and use the place_id as destination

destination_place_ids = []
for i, destination in enumerate(destinations):
    if destination == "home":
        with open(f"places/home.json", 'r') as file:
            place = json.load(file)
            # Then, replace the unique_name with place_id
            destination_place_ids.append(f"place_id:{place['place_id']}")
        continue
    # First search in which type the place is. So, go through each folder in the places directory

    flag = False
    for folder in os.listdir("places"):
        if not os.path.isdir(f"places/{folder}"):
            continue
        # If the unique_name is found in the folder
        if f"{destination}.json" in os.listdir(f"places/{folder}"):
            # Then, open the json file and get the place_id
            with open(f"places/{folder}/{destination}.json", 'r') as file:
                place = json.load(file)
                # Then, replace the unique_name with place_id
                destination_place_ids.append(f"place_id:{place['place_id']}")
            flag = True
            break

    if not flag:
        print(
            f"Place with unique_name {destination} not found. Please check the unique_name and try again.")
        exit()

response = gmaps.distance_matrix(
    origins=origin_place_ids,
    destinations=destination_place_ids,
    mode='walking',
    language='en',
    units='metric'
)
# print json response beautified
# print(json.dumps(response, indent=2))


# {
#   "destination_addresses": [
#     "House 38/1 (1st Floor, Indira Rd, Dhaka 1215, Bangladesh",
#     "Bijoy Sarani, Dhaka 1215, Bangladesh",
#     "DSW office, BUET, Dhaka 1000, Bangladesh",
#     "69, 71 New Elephant Rd, Dhaka 1205, Bangladesh"
#   ],
#   "origin_addresses": [
#     "House 38/1 (1st Floor, Indira Rd, Dhaka 1215, Bangladesh",
#     "Bijoy Sarani, Dhaka 1215, Bangladesh",
#     "DSW office, BUET, Dhaka 1000, Bangladesh",
#     "69, 71 New Elephant Rd, Dhaka 1205, Bangladesh"
#   ],
#   "rows": [
#     {
#       "elements": [
#         {
#           "distance": {
#             "text": "1.8 km",
#             "value": 1835
#           },
#           "duration": {
#             "text": "7 mins",
#             "value": 399
#           },
#           "status": "OK"
#         },
#         {
#           "distance": {
#             "text": "5.3 km",
#             "value": 5255
#           },
#           "duration": {
#             "text": "17 mins",
#             "value": 1039
#           },
#           "status": "OK"
#         },

# Open the file in read mode
with open('distance_matrix.json', 'r') as file:
    distance_matrix = json.load(file)

if not distance_matrix:
    distance_matrix = {}
else:
    # Continue with your processing
    pass
# # Read distance_matrix.json file and write the response to it
# distance_matrix_file = open("distance_matrix.json", "r+")
# # read the json object from the file to a variable
# distance_matrix = json.load(distance_matrix_file)

# Convert the response to a matrix format
# Declare a matrix variable

matrix = []
for row in response["rows"]:
    for element in row["elements"]:
        duration = element["duration"]["value"]
        minutes = duration // 60
        seconds = duration % 60
        new_element = {"distance": f'{element["distance"]["value"]} meters',
                       "duration":  f'{minutes} mins{" " + str(seconds) + " secs" if seconds != 0 else ""}'}
        matrix.append(new_element)
        # now add the matrix to the file
        # distance_matrix is a list of dictionaries
        # each dictionary contains the distance and duration of a place from the origin
        # for example, if the origin is "home" and the destination is "sonali_bank_buet"
        # then the dictionary will be {"distance": "4389 m", "duration": "14 mins 52 secs"}

        # If the origin already exists in the distance_matrix, then append only those destinations which are not in the distance_matrix
        # If the origin does not exist in the distance_matrix, then append the origin and all the destinations

        # distance_matrix[origin] = {
        #     **distance_matrix.get(origin, {}), destination: new_element}

# print(distance_matrix)
# From the response, create distance and duration matrix in this format:
#   "home": {
#     "home": {
#       "distance": "0 m",
#       "duration": "0 mins"
#     },
#     "bangabandhu_military_museum": {
#       "distance": "3298 m",
#       "duration": "10 mins 25 secs"
#     },
#     "sonali_bank_buet": {
#       "distance": "4389 m",
#       "duration": "14 mins 52 secs"
#     }
#     "sonali_bank_buet": {
#       "distance": "4389 m",
#       "duration": "14 mins 52 secs"
#     }
#   },


for i, origin in enumerate(origins):
    # print(f'"{origin}": {{')
    for j, destination in enumerate(destinations):
        # print(f'  "{destination}": {{')
        # print(
        #     f'    "distance": "{response["rows"][i]["elements"][j]["distance"]["text"]}",')
        # instead of printing distance in text format, convert the value to meters and print
        # print(
        #     f'    "distance": "{response["rows"][i]["elements"][j]["distance"]["value"]} meters",')
        # print(
        #     f'    "duration": "{response["rows"][i]["elements"][j]["duration"]["text"]}"')
        # print the duration value in minutes and seconds. Don't print 0 seconds
        # duration = response["rows"][i]["elements"][j]["duration"]["value"]
        # minutes = duration // 60
        # seconds = duration % 60
        # print(
        #     f'    "duration": "{minutes} mins{" " + str(seconds) + " secs" if seconds != 0 else ""}"')
        # print("  },")

        element = response["rows"][i]["elements"][j]
        duration = element["duration"]["value"]
        minutes = duration // 60
        seconds = duration % 60
        new_element = {"distance": f'{element["distance"]["value"]} meters',
                       "duration":  f'{minutes} mins{" " + str(seconds) + " secs" if seconds != 0 else ""}'}
        distance_matrix[origin] = {
            **distance_matrix.get(origin, {}), destination: new_element}

    # print("},")
print(json.dumps(distance_matrix, indent=2))
# save the distance_matrix to the file
with open('distance_matrix.json', 'w') as file:
    json.dump(distance_matrix, file, indent=2)
