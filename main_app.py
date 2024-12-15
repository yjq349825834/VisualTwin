# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 18:11:47 2024

@author: Jiaqi Ye
"""

# import time
import folium
import csv
# import random
import streamlit as st
from streamlit_folium import st_folium
from module_chatbot import ChatbotModule
import base64

# Initialise data path
INPUT_FILE = "data/route_info_vibrations.csv"

HAT_LOGO_PATH = "data/christmas_hat.png" 

TRAIN_LOGO_PATH = "data/christmas_train.png"

MAP_CENTER = [51.853749549356415, -0.10878609932857745]  

STATION_VIDEOS = {
    "Cambridge": "data/cambridge_1.mp4",
    "London Kings Cross": "data/london_kings_cross_1.mp4",
}

IMAGES = [
    "https://github.com/yjq349825834/VisualTwin/blob/144507ad041e3d12429d5f6123f9ff8e5932bb21/data/measure_1.png",
    "data/measure_3.png",
    "data/measure_2.png",
]


# Load route, vibration, and station information
def load_data(input_file):
    route, vibrations, stations = [], [], []
    with open(input_file, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            latitude, longitude = map(float, row[:2])
            station, entries_exits, vibration = row[2], float(row[3]), float(row[4])
            route.append((latitude, longitude))
            vibrations.append(vibration)
            if station != "0":
                stations.append({
                    "lat": latitude,
                    "lon": longitude,
                    "name": station,
                    "value": entries_exits,
                })
    return route, vibrations, stations

# Normalize entries/exits for stations for creating bubbles
def normalize_station_values(stations):
    if not stations:
        return
    max_value = max(station["value"] for station in stations)
    min_value = min(station["value"] for station in stations)
    for station in stations:
        station["radius"] = 6 + 14 * (station["value"] - min_value) / (max_value - min_value)

# Add station bulbbles and feed visual data to the map
def add_station_markers(map_obj, stations, station_videos):
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
            popup=popup,
        ).add_to(map_obj)

# Add route with vibration levels
def add_route(map_obj, route, vibrations, color_toggle=False):
    red_segments = []
    image_index = 0  # Index for red segments' images

    if color_toggle:
        for i in range(len(route) - 1):
            color = (
                "blue" if vibrations[i] < 0.2 else
                "green" if vibrations[i] < 0.3 else
                "yellow" if vibrations[i] < 0.4 else "red"
            )
            folium.PolyLine(
                locations=[route[i], route[i + 1]],
                color=color,
                weight=5,
                opacity=0.8,
            ).add_to(map_obj)
            if vibrations[i] > 0.4:
                if not red_segments or red_segments[-1][-1] != i:
                    red_segments.append([i, i + 1])
                else:
                    red_segments[-1][-1] = i + 1

        for segment in red_segments:
            start_idx, end_idx = segment
            latitudes = [route[idx][0] for idx in range(start_idx, end_idx + 1)]
            longitudes = [route[idx][1] for idx in range(start_idx, end_idx + 1)]
            rect_bounds = [
                (min(latitudes) - 0.001, min(longitudes) - 0.001),
                (max(latitudes) + 0.001, max(longitudes) + 0.001),
            ]
            image_url = IMAGES[image_index % len(IMAGES)]
            image_index += 1
            popup_html = f"""
            <div>
                <h4>High Vibration Area</h4>
                <p>Continuous vibration: > 0.4</p>
                <img src="{image_url}" width="300" alt="Image">
            </div>
            """
            popup = folium.Popup(popup_html, max_width=350)
            folium.Rectangle(
                bounds=rect_bounds,
                color="red",
                fill=True,
                fill_opacity=0.3,
                popup=popup,
            ).add_to(map_obj)
    else:
        folium.PolyLine(locations=route, color="darkgreen", weight=5, opacity=0.8).add_to(map_obj)


# This is a Christams version, so ... ... 
def add_image(img_path, style=""):
    with open(img_path, "rb") as img_file:
        img_data = base64.b64encode(img_file.read()).decode("utf-8")
    return f'<img src="data:image/png;base64,{img_data}" style="{style}" />'


def main():
    st.markdown(
        f"""
        <div style="text-align: left; position: relative;">
            <h1 style="display: inline-block; margin-bottom: 0; padding: 0;">Railway Visual<span style="position: relative;"> Twin</span></h1>
            <div style="position: absolute; top: -20px; left: 3%; transform: translate(-50%, 0);">
                {add_image(HAT_LOGO_PATH, "width: 50px; height: auto;")}
            </div>
            <div style="position: absolute; top: -35px; left: 70%; transform: translate(-50%, 0);">
                {add_image(TRAIN_LOGO_PATH, "width: 200px; height: auto;")}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("""
    Explore a dynamic and interactive representation of the railway network between Cambridge and London Kings Cross. 
    This app visualizes route data, station activity, and vibration metrics in real-time, helping you avoid congestions, identify key insights, and high-risk areas.
    """)

    # Load route and station data
    route, vibrations, stations = load_data(INPUT_FILE)
    normalize_station_values(stations)

    # Create the map
    uk_map = folium.Map(location=MAP_CENTER, zoom_start=7)
    folium.Marker(location=route[0], popup="Cambridge", icon=folium.Icon(color="green")).add_to(uk_map)
    folium.Marker(location=route[-1], popup="London Kings Cross", icon=folium.Icon(color="red")).add_to(uk_map)

    # Congestion and vibration toggles
    if "show_stations" not in st.session_state:
        st.session_state.show_stations = False

    if st.button("Avoiding Congestion"):
        st.session_state.show_stations = not st.session_state.show_stations

    if "color_toggle" not in st.session_state:
        st.session_state.color_toggle = False

    if st.button("Track Assessment"):
        st.session_state.color_toggle = not st.session_state.color_toggle

    # Add markers and routes
    if st.session_state.show_stations:
        add_station_markers(uk_map, stations, STATION_VIDEOS)

    add_route(uk_map, route, vibrations, color_toggle=st.session_state.color_toggle)
    st_folium(uk_map, width=700, height=500)

    # Integrate chatbot module
    #chatbot = ChatbotModule()
    #chatbot.display_chatbot()

# Entry point
if __name__ == "__main__":
    main()
