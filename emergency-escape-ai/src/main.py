import streamlit as st
from ai_engine import Pathfinding
from chatbot import Chatbot
from shelter import ShelterFinder
from vision import ObstacleDetector
import json

def load_map_data():
    with open('data/sample_map.json') as f:
        return json.load(f)

def main():
    st.title("Intelligent Emergency Escape & Smart Route Finder System")
    
    # Load map data
    map_data = load_map_data()
    
    # Initialize modules
    pathfinding = Pathfinding(map_data)
    chatbot = Chatbot()
    shelter_finder = ShelterFinder()
    obstacle_detector = ObstacleDetector()
    
    # User input section
    st.header("Emergency Assistance")
    user_location = st.text_input("Enter your current location (latitude, longitude):")
    emergency_type = st.selectbox("Select emergency type:", ["Fire", "Medical", "Hazard"])
    
    if st.button("Get Assistance"):
        if user_location:
            # Process user input
            lat, lon = map(float, user_location.split(","))
            safest_path = pathfinding.find_safest_route(lat, lon, emergency_type)
            nearest_shelters = shelter_finder.find_nearest_shelters(lat, lon)
            chatbot_response = chatbot.get_response(emergency_type)
            
            # Display results
            st.subheader("Safest Path:")
            st.write(safest_path)
            st.subheader("Nearest Shelters:")
            st.write(nearest_shelters)
            st.subheader("Chatbot Response:")
            st.write(chatbot_response)
        else:
            st.error("Please enter a valid location.")

if __name__ == "__main__":
    main()