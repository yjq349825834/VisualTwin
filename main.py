# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 18:11:47 2024

@author: Jiaqi Ye
"""

import time
import folium
import csv
import random
import streamlit as st
from streamlit_folium import st_folium
from chatbot import ChatbotModule

# Load data
input_file = "updated_resampled_route_coordinates2.csv"
route = []
vibrations = []
stations = []

# Read the CSV file
with open(input_file, mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        latitude = float(row[0])
        longitude = float(row[1])
        station = row[2]  # Station name (or 0 if not a station)
        entries_exits = float(row[3])  # Entries and exits value
        vibration = float(row[4])  # Vibration value
        route.append((latitude, longitude))
        vibrations.append(vibration)
        if station != "0":
            stations.append({"lat": latitude, "lon": longitude, "name": station, "value": entries_exits})

# Normalize the values for dot size
if stations:
    max_value = max(station["value"] for station in stations)
    min_value = min(station["value"] for station in stations)
    for station in stations:
        station["radius"] = 6 + 14 * (station["value"] - min_value) / (max_value - min_value)

# Map setup
map_center = [51.853749549356415, -0.10878609932857745]  # Roughly midway
uk_map = folium.Map(location=map_center, zoom_start=7)

# Add start and end markers
folium.Marker(location=route[0], popup="Cambridge", icon=folium.Icon(color='green')).add_to(uk_map)
folium.Marker(location=route[-1], popup="London Kings Cross", icon=folium.Icon(color='red')).add_to(uk_map)

# Streamlit UI
st.title("Railway 'Visual Twin'")

st.markdown("""
Explore a dynamic and interactive representation of the railway network between Cambridge and London Kings Cross. 
This app visualizes route data, station activity, and vibration metrics in real-time, helping you avoid jams, identify key insights, and high-risk areas.
""")

# Example mapping of station names to video URLs
station_videos = {
    "Cambridge": "http://localhost:8000/cambridge_1.mp4",  # Replace with actual video URL
    "London Kings Cross": "http://localhost:8000/london_kings_cross_1.mp4",
    # Add more stations with corresponding video URLs
}


def add_station_markers(map_obj, stations, station_videos):
    """Add station markers to the map."""
    for station in stations:
        station_name = station["name"]
        video_url = station_videos.get(station_name, "")
        popup_html = f"""
        <div>
            <h4>{station_name}</h4>
            <p>Entries/Exits: {int(station['value'])}</p>
            {"<video controls width='300'><source src='" + video_url + "' type='video/mp4'></video>" if video_url else "<p>Video unavailable</p>"}
        </div>
        """
        popup = folium.Popup(popup_html, max_width=350)

        folium.CircleMarker(
            location=(station["lat"], station["lon"]),
            radius=station["radius"],
            color=None,
            fill=True,
            fill_color="red",
            fill_opacity=0.5,
            tooltip=f"{station_name}: {int(station['value'])} entries/exits",
            popup=popup
        ).add_to(map_obj)
        

# Function to add route lines
def add_route(map_obj, route, vibrations, color_toggle=False):
    red_segments = []  # To store the start and end points of red segments
    
    images = [
    "http://localhost:8000/red1.png",
    "http://localhost:8000/red3.png",
    "http://localhost:8000/red2.png",
    ]  # List of unique image URLs (replace with actual URLs)
    image_index = 0
    if color_toggle:
        for i in range(len(route) - 1):
            color = "blue" if vibrations[i] < 0.2 else \
                    "green" if vibrations[i] < 0.3 else \
                    "yellow" if vibrations[i] < 0.4 else "red"
            folium.PolyLine(
                locations=[route[i], route[i + 1]],
                color=color,
                weight=5,
                opacity=0.8
            ).add_to(map_obj)
            
            # Collect red segments
            if vibrations[i] > 0.4:
                if not red_segments or red_segments[-1][-1] != i:  # Start new segment
                    red_segments.append([i, i + 1])
                else:  # Extend the current segment
                    red_segments[-1][-1] = i + 1

        # Add rectangles for each continuous red segment
        for segment in red_segments:
            start_idx, end_idx = segment
            latitudes = [route[idx][0] for idx in range(start_idx, end_idx + 1)]
            longitudes = [route[idx][1] for idx in range(start_idx, end_idx + 1)]
    
            # Bounding box for the segment
            rect_bounds = [
                (min(latitudes) - 0.001, min(longitudes) - 0.001),
                (max(latitudes) + 0.001, max(longitudes) + 0.001),
            ]
    
            # Assign a unique image (loop through the list if there are more regions than images)
            image_url = images[image_index % len(images)]
            image_index += 1
    
            # Popup for high vibration region
            popup_html = f"""
            <div>
                <h4>High Vibration Area</h4>
                <p>Continuous vibration: > 0.4</p>
                <img src="{image_url}" width="300" alt="Image">
            </div>
            """
            popup = folium.Popup(popup_html, max_width=350)
    
            # Add the rectangle to the map
            folium.Rectangle(
                bounds=rect_bounds,
                color="red",
                fill=True,
                fill_opacity=0.3,
                popup=popup
            ).add_to(map_obj)
    else:
        folium.PolyLine(locations=route, color="darkgreen", weight=5, opacity=0.8).add_to(map_obj)
        

# Toggle station markers
if "show_stations" not in st.session_state:
    st.session_state.show_stations = False

if st.button("Avoiding Congestion"):
    st.session_state.show_stations = not st.session_state.show_stations


# Toggle vibration-based route coloring
if "color_toggle" not in st.session_state:
    st.session_state.color_toggle = False

if st.button("Track Assessment"):
    st.session_state.color_toggle = not st.session_state.color_toggle
    

if st.session_state.show_stations:
    add_station_markers(uk_map, stations, station_videos)    

# Add route based on toggle
add_route(uk_map, route, vibrations, color_toggle=st.session_state.color_toggle)


# Display the map
st_folium(uk_map, width=700, height=500)

# Initialize and display the chatbot
chatbot = ChatbotModule()
chatbot.display_chatbot()