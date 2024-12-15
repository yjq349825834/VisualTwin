# Visual Twin: Enhanced Railway Asset Mangment

This repository hosts the Visual Twin Open Data project proposal, a visual data-driven railway monitoring platform. It integrates a Streamlit app, interactive visualisation, object detection, and chatbot interaction for enhanced railway condition monitoring and asset management.

![App Screenshot](data/app_1.0.png)

## Features
- **Visual Railway Monitoring**: Interactive visualization of UK railway usage and routes.
- **Chatbot Interaction**: Integrated chatbot for inquiries.
- **Object Detection Module**: Detects specific conditions in railway assets.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yjq349825834/VisualTwin.git
   cd VisualTwin

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Run the Streamlit app:
   ```bash
   streamlit run app/visual_twin_app.py

## Suggested Sources of Open Data
- [Open Sensor Data for Rail 2023](https://data.fid-move.de/dataset/osdar23) 
- [The Office of Rail and Road Data Portal](http://dataportal.orr.gov.uk/)
- [Network Rail Data Feeds](https://datafeeds.networkrail.co.uk/)


## Project Structure
```plaintext
VisualTwin/
│
├── main_app.py                    # The main application file
├── module_chatbot.py              # The chatbot module
├── Dockerfile                     # Dockerfile for containerizing the app
├── requirements.txt               # Python dependencies for the app
├── README.md                      # Project description and instructions
├── data/                          # Folder for datasets or statics
│   ├── route_info_vibrations.csv  # Route info between London Kings Cross and Cambridge for demo
│   └── videos.mp4                 # Demo videos
│   └── images.png                 # Demo sensor data
    └── data.ods                   # Example dataset from ORR (Train Station Usuage)
├── notebooks/                     # Jupyter notebooks for instructions or experiments
│   └── object_detection.ipynb     # Instruction notebook for object detection module
