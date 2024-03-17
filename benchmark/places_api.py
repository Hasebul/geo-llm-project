from datetime import datetime
import googlemaps
import json
import os

my_location = (23.7563756, -90.3846132)
# https://developers.google.com/maps/documentation/places/web-service/supported_types
place_types = [
    "accounting", "airport", "amusement_park", "art_gallery", "atm",
    "bakery", "bank", "bar", "beauty_salon", "bicycle_store", "book_store", "bowling_alley", "bus_station",
    "cafe", "campground", "car_dealer", "car_rental", "car_repair", "car_wash", "casino", "cemetery", "church", "city_hall", "clothing_store", "convenience_store", "courthouse",
    "dentist", "department_store", "doctor", "drugstore",
    "electrician", "electronics_store", "embassy",
    "fire_station", "florist", "food", "funeral_home", "furniture_store",
    "gas_station", "gym",
    "hair_care", "hardware_store", "health", "hindu_temple", "home_goods_store", "hospital",
    "insurance_agency",
    "jewelry_store",
    "laundry", "lawyer", "library",
    "light_rail_station", "liquor_store", "local_government_office", "locksmith", "lodging",
    "meal_delivery", "meal_takeaway", "mosque", "movie_rental", "movie_theater", "moving_company", "museum",
    "night_club",
    "painter", "park", "parking", "pet_store", "pharmacy", "physiotherapist", "place_of_worship", "plumber", "point_of_interest", "police", "political", "post_office", "primary_school",
    "real_estate_agency", "restaurant", "roofing_contractor", "rv_park",
    "school", "secondary_school", "shoe_store", "shopping_mall", "spa", "stadium", "storage", "store", "subway_station", "supermarket", "taxi_stand", "tourist_attraction", "train_station", "transit_station", "travel_agency",
    "university",
    "veterinary_care",
    "zoo"
]


def get_opening_hours(periods):
    days = ['Monday', 'Tuesday',
            'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    opening_hours = {}
    for period in periods:
        open_time = datetime.strptime(
            period['open']['time'], "%H%M").strftime("%I:%M %p")
        close_time = datetime.strptime(
            period['close']['time'], "%H%M").strftime("%I:%M %p")
        opening_hours[days[period['open']['day']]] = {
            'open': open_time, 'close': close_time}
    return opening_hours


gmaps = googlemaps.Client(key='AIzaSyCNtIajO-Xwpocu9ARrah2khQF-tG8vWok')

while True:
    print()
    for i, place_type in enumerate(place_types):
        print(f"{i+1:02}. {place_type:<25}", end=" | " if i % 5 != 4 else "\n")

    type_index = int(
        input(f"\n\nchoose type(1-{len(place_types)}): ")) - 1

    if (type_index == -1):
        continue

    name = input(f"\nEnter the name of the {place_types[type_index]}: ")
    places_result = gmaps.places(
        name,
        # location=my_location,
        region="BD",
        type=place_types[type_index])

    print()

    if (len(places_result['results']) == 0):
        print("No results found. Try again.")
        continue

    for i, place in enumerate(places_result['results']):
        print(
            f"{i+1}. Name: {place['name']} | Address: {place['formatted_address']} | Location: {place['geometry']['location']['lat']}, {place['geometry']['location']['lng']}")

    index = int(input(
        f"Enter the index of the {place_types[type_index]}: (1-{len(places_result['results'])}): ")) - 1

    if (index == -1):
        continue

    place_id = places_result['results'][index]['place_id']
    place_result = gmaps.place(place_id)['result']

    if place_types[type_index] == "restaurant":
        details = {
            "place_id": place_result.get('place_id'),
            "name": place_result.get('name'),
            "location": place_result.get('geometry', {}).get('location'),
            "address": place_result.get('formatted_address'),
            "opening_hours": get_opening_hours(place_result.get('opening_hours', {}).get('periods', [])),
            "price_level": place_result.get('price_level'),
            "rating": place_result.get('rating'),
            "user_ratings_total": place_result.get('user_ratings_total'),
            "delivery": place_result.get('delivery'),
            "dine_in": place_result.get('dine_in'),
            "reservable": place_result.get('reservable'),
            "takeout": place_result.get('takeout'),
            "serves_breakfast": place_result.get('serves_breakfast'),
            "serves_lunch": place_result.get('serves_lunch'),
            "serves_dinner": place_result.get('serves_dinner'),
            "serves_brunch": place_result.get('serves_brunch'),
            "wheelchair_accessible_entrance": place_result.get('wheelchair_accessible_entrance'),
        }
    else:
        details = {
            "place_id": place_result.get('place_id'),
            "name": place_result.get('name'),
            "location": place_result.get('geometry', {}).get('location'),
            "address": place_result.get('formatted_address'),
            "opening_hours": get_opening_hours(place_result.get('opening_hours', {}).get('periods', [])),
        }

    directory = f"places/{place_types[type_index]}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    while True:
        unique = input(
            f"Give a unique name to the {place_types[type_index]}: ")
        if not os.path.exists(f"{directory}/{unique}.json"):
            break
        else:
            break
            # print("File already exists. Please give a unique name.")

    with open(f"{directory}/{unique}.json", "w") as f:
        json.dump(details, f, indent=2)

    print(f"\nDetails saved in {directory}/{unique}.json")

'''
https://developers.google.com/maps/documentation/places/web-service/search-text#Place
Format:
address_components -> AddressComponent
adr_address
business_status
curbside_pickup
current_opening_hours -> PlaceEditorialSummary
# delivery
# dine_in
editorial_summary -> PlaceEditorialSummary
# formatted_address
formatted_phone_number
# geometry -> Geometry
icon
icon_background_color
icon_mask_base_uri
international_phone_number
# name
# opening_hours -> PlaceOpeningHours
photos -> PlacePhoto
# place_id
plus_code -> PlusCode
# price_level
    - 0 Free
    - 1 Inexpensive
    - 2 Moderate
    - 3 Expensive
    - 4 Very Expensive
# rating
# reservable
# reviews -> PlaceReview
secondary_opening_hours -> PlaceOpeningHours
# serves_beer
# serves_breakfast
# serves_brunch
# serves_dinner
# serves_lunch
# serves_vegetarian_food
# serves_wine
# takeout
# types
url
# user_ratings_total
utc_offset
vicinity
website
# wheelchair_accessible_entrance
'''
