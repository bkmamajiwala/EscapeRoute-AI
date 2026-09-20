from typing import List, Dict
import pandas as pd
import math

class ShelterFinder:
    def __init__(self):
        """Initialize shelters near Pune with real coordinates"""
        self.shelters = [
            {
                "name": "Government School - Baner",
                "type": "School",
                "lat": 18.5600,
                "lng": 73.8000,
                "capacity": 500,
                "safety": 95,
                "contact": "020-1234-5678"
            },
            {
                "name": "City Hospital - Aundh",
                "type": "Hospital",
                "lat": 18.5400,
                "lng": 73.8300,
                "capacity": 200,
                "safety": 98,
                "contact": "020-9876-5432"
            },
            {
                "name": "Community Center - Viman Nagar",
                "type": "Community Center",
                "lat": 18.5800,
                "lng": 73.9100,
                "capacity": 350,
                "safety": 92,
                "contact": "020-5555-5555"
            },
            {
                "name": "Sports Complex - Hinjawadi",
                "type": "Sports Complex",
                "lat": 18.5900,
                "lng": 73.7700,
                "capacity": 600,
                "safety": 94,
                "contact": "020-3333-3333"
            },
            {
                "name": "University Hall - Katraj",
                "type": "University",
                "lat": 18.4900,
                "lng": 73.8600,
                "capacity": 800,
                "safety": 96,
                "contact": "020-7777-7777"
            },
            {
                "name": "Fire Station - Pashan",
                "type": "Fire Station",
                "lat": 18.5300,
                "lng": 73.7600,
                "capacity": 150,
                "safety": 99,
                "contact": "020-2222-2222"
            },
            {
                "name": "Army Base - Khadakvasla",
                "type": "Military Base",
                "lat": 18.4600,
                "lng": 73.8900,
                "capacity": 1000,
                "safety": 100,
                "contact": "020-4444-4444"
            },
            {
                "name": "Temple Complex - Dagduseth",
                "type": "Religious Site",
                "lat": 18.5200,
                "lng": 73.8700,
                "capacity": 300,
                "safety": 91,
                "contact": "020-6666-6666"
            },
            {
                "name": "Police Station - Shivajinagar",
                "type": "Police Station",
                "lat": 18.5100,
                "lng": 73.8800,
                "capacity": 200,
                "safety": 97,
                "contact": "020-1111-1111"
            },
            {
                "name": "Railway Station Shelter",
                "type": "Railway Station",
                "lat": 18.5400,
                "lng": 73.8400,
                "capacity": 400,
                "safety": 93,
                "contact": "020-8888-8888"
            }
        ]
    
    def calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate distance between two coordinates using Haversine formula"""
        R = 6371000  # Earth radius in meters
        
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lng2 - lng1)
        
        a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        distance = R * c
        return distance
    
    def find_nearby_shelters(self, user_lat: float, user_lng: float, search_radius: float = 5000) -> list:
        """Find shelters within search radius"""
        nearby_shelters = []
        
        for shelter in self.shelters:
            distance = self.calculate_distance(user_lat, user_lng, shelter["lat"], shelter["lng"])
            
            if distance <= search_radius:
                shelter_copy = shelter.copy()
                shelter_copy["distance"] = distance
                nearby_shelters.append(shelter_copy)
        
        # Sort by distance
        nearby_shelters.sort(key=lambda x: x["distance"])
        
        return nearby_shelters
    
    def get_shelter_by_type(self, shelter_type: str) -> list:
        """Get shelters filtered by type"""
        return [s for s in self.shelters if s["type"].lower() == shelter_type.lower()]
    
    def get_safest_shelters(self, limit: int = 5) -> list:
        """Get safest shelters (highest safety score)"""
        return sorted(self.shelters, key=lambda x: x["safety"], reverse=True)[:limit]
    
    def get_largest_capacity(self, limit: int = 5) -> list:
        """Get shelters with largest capacity"""
        return sorted(self.shelters, key=lambda x: x["capacity"], reverse=True)[:limit]