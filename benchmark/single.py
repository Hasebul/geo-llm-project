from datetime import datetime
import googlemaps
import json
import os

my_location = (23.7563756, -90.3846132)


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


places_result = gmaps.place(
    "ChIJNwjmp8q4VTcRxVCb9Pb8fvQ"
)


print(places_result)
