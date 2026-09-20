# Intelligent Emergency Escape & Smart Route Finder System

## Overview
The Intelligent Emergency Escape & Smart Route Finder System is designed to assist users during emergencies such as fires, medical situations, or other hazards. The system provides real-time guidance to the safest and fastest exits, identifies nearby shelters, and offers AI-driven assistance through a chatbot. It dynamically adapts to environmental risks, ensuring user safety and efficient navigation.

## Project Goals
- Guide users to the safest and fastest exit routes.
- Locate nearby shelters and safe zones.
- Provide real-time assistance via an AI chatbot.
- Adapt to changing environmental conditions and hazards.

## Core AI Concepts
The system incorporates several core AI concepts:
- **Pathfinding Intelligence**: Utilizes A* and Dijkstra’s algorithms for route optimization based on a weighted graph representation that accounts for hazards.
- **NLP Chatbot**: Implements intent classification and keyword extraction to assist users effectively during emergencies.
- **Decision-Making System**: A rule-based expert system that evaluates distance, safety, and congestion risk.
- **KNN / Geospatial AI**: Employs K-Nearest Neighbors to find the closest shelters based on user coordinates.

## System Modules
1. **Smart Navigation Engine**: Converts the map into a graph/grid, calculates dynamic weights based on hazards, and outputs the safest path and alternative routes.
2. **AI Smart Chatbot**: Provides a conversational interface to collect user information and deliver instructions and navigation guidance.
3. **Shelter Finder**: Identifies the nearest safe zones based on GPS input, ranking them by safety and distance.
4. **Visualization System**: Displays the map, user position, path to exit, and hazards using visualization libraries.

## Advanced Features
- **Dynamic Obstacle Detection**: Uses OpenCV for real-time detection of hazards like fire and smoke.
- **Predictive Crowd Flow**: Implements simple machine learning to predict congestion areas and dynamically reroute users.
- **Offline Mesh Networking**: Conceptual design for device-to-device communication in case of network failure.
- **AR Navigation**: Concept for overlaying visual navigation aids using augmented reality.
- **Health Monitoring**: Concept for integrating smartwatch data to detect user stress levels and provide calming guidance.

## Tech Stack
- **Python**: Core programming language for the application.
- **NetworkX**: Library for graph representation and pathfinding algorithms.
- **Streamlit**: Framework for building the user interface.
- **OpenCV**: Library for computer vision tasks.
- **Scikit-learn**: Library for implementing K-Nearest Neighbors.
- **Google Maps API / Folium**: For mapping and geospatial functionalities.
- **MongoDB / Firebase**: For data storage and management.

## Installation Instructions
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/emergency-escape-ai.git
   ```
2. Navigate to the project directory:
   ```
   cd emergency-escape-ai
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## How to Run the System
To start the application, run the following command:
```
python src/main.py
```
This will launch the Streamlit interface where users can interact with the system.

## Future Improvements
- Enhance the chatbot's NLP capabilities for better user interaction.
- Integrate more advanced machine learning models for predictive crowd flow analysis.
- Expand the dynamic obstacle detection feature to include more types of hazards.
- Develop the AR navigation feature for a more immersive user experience.

## Conclusion
The Intelligent Emergency Escape & Smart Route Finder System is a comprehensive solution aimed at improving user safety during emergencies through advanced AI techniques and real-time assistance.