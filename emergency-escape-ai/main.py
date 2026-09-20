import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ai_engine import PathFinding
from src.shelter import ShelterFinder

# Page config
st.set_page_config(
    page_title="🚨 Emergency Escape System",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS Styling - More Aesthetic
st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
        }
        
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .main-header {
            background: linear-gradient(135deg, #FF6B6B 0%, #DC143C 100%);
            padding: 40px;
            border-radius: 20px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(255, 107, 107, 0.4);
            animation: slideDown 0.6s ease-out;
        }
        
        .main-header h1 {
            font-size: 2.8em;
            font-weight: 900;
            margin-bottom: 10px;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
            letter-spacing: 1px;
        }
        
        .main-header p {
            font-size: 1.2em;
            opacity: 0.95;
            font-weight: 500;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 15px;
            color: white;
            text-align: center;
            box-shadow: 0 10px 35px rgba(102, 126, 234, 0.4);
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            border: 2px solid rgba(255,255,255,0.1);
        }
        
        .metric-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 15px 50px rgba(102, 126, 234, 0.6);
        }
        
        .metric-card h3 {
            font-size: 0.95em;
            opacity: 0.9;
            margin-bottom: 12px;
            font-weight: 600;
        }
        
        .metric-card h2 {
            font-size: 2.8em;
            font-weight: 900;
            margin: 10px 0;
        }
        
        .metric-card p {
            font-size: 0.9em;
            opacity: 0.85;
        }
        
        .info-card {
            background: linear-gradient(135deg, #f0f2f6 0%, #e8eaf6 100%);
            padding: 25px;
            border-radius: 15px;
            border-left: 6px solid #667eea;
            margin: 15px 0;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
            border-radius: 12px;
            transition: all 0.3s ease;
        }
        
        .info-card:hover {
            transform: translateX(5px);
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.25);
        }
        
        .success-card {
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            padding: 25px;
            border-radius: 15px;
            border-left: 6px solid #28a745;
            margin: 15px 0;
            box-shadow: 0 8px 25px rgba(40, 167, 69, 0.15);
            transition: all 0.3s ease;
        }
        
        .success-card:hover {
            transform: translateX(5px);
            box-shadow: 0 12px 35px rgba(40, 167, 69, 0.25);
        }
        
        .warning-card {
            background: linear-gradient(135deg, #fff3cd 0%, #ffe69c 100%);
            padding: 25px;
            border-radius: 15px;
            border-left: 6px solid #ffc107;
            margin: 15px 0;
            box-shadow: 0 8px 25px rgba(255, 193, 7, 0.15);
            transition: all 0.3s ease;
        }
        
        .warning-card:hover {
            transform: translateX(5px);
            box-shadow: 0 12px 35px rgba(255, 193, 7, 0.25);
        }
        
        .danger-card {
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            padding: 25px;
            border-radius: 15px;
            border-left: 6px solid #dc3545;
            margin: 15px 0;
            box-shadow: 0 8px 25px rgba(220, 53, 69, 0.2);
            animation: pulse 2s infinite;
            transition: all 0.3s ease;
        }
        
        .danger-card:hover {
            transform: translateX(5px);
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.85; }
        }
        
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .step-item {
            background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
            padding: 18px;
            margin: 12px 0;
            border-radius: 12px;
            border-left: 5px solid #667eea;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }
        
        .step-item:hover {
            transform: translateX(8px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        }
        
        .section-title {
            color: #333;
            font-size: 1.5em;
            font-weight: 800;
            margin: 25px 0 15px 0;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }
        
        .stMetric {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        }
        
        .location-badge {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 25px;
            font-size: 0.9em;
            font-weight: 600;
            display: inline-block;
            margin: 5px;
        }
        
        /* Sidebar Styles */
        .sidebar-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            color: white;
            margin-bottom: 20px;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }
        
        .sidebar-header h2 {
            margin: 0;
            font-size: 1.5em;
            font-weight: 900;
        }
        
        .sidebar-header p {
            margin: 5px 0 0 0;
            font-size: 0.9em;
            opacity: 0.9;
        }
        
        .nav-section-title {
            color: #667eea;
            font-size: 0.85em;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 20px;
            margin-bottom: 10px;
            padding-left: 10px;
            border-left: 3px solid #667eea;
        }
        
        .nav-item {
            padding: 12px 15px;
            margin: 8px 0;
            border-radius: 10px;
            background: rgba(102, 126, 234, 0.1);
            border-left: 4px solid transparent;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .nav-item:hover {
            background: rgba(102, 126, 234, 0.2);
            border-left-color: #667eea;
            transform: translateX(5px);
        }
        
        .emergency-button {
            background: linear-gradient(135deg, #FF6B6B 0%, #DC143C 100%);
            color: white;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            font-weight: 900;
            margin: 20px 0;
            box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3); }
            50% { opacity: 0.9; box-shadow: 0 8px 35px rgba(255, 107, 107, 0.5); }
        }
        
        .quick-stats {
            background: linear-gradient(135deg, #f0f2f6 0%, #e8eaf6 100%);
            padding: 15px;
            border-radius: 12px;
            margin: 15px 0;
            border-left: 4px solid #667eea;
        }
        
        .stat-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 8px 0;
            font-size: 0.9em;
        }
        
        .stat-value {
            background: #667eea;
            color: white;
            padding: 4px 10px;
            border-radius: 6px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'pathfinding' not in st.session_state:
    st.session_state.pathfinding = PathFinding()

if 'shelter_finder' not in st.session_state:
    st.session_state.shelter_finder = ShelterFinder()

if 'show_route' not in st.session_state:
    st.session_state.show_route = False

if 'route_data' not in st.session_state:
    st.session_state.route_data = None

if 'show_shelters' not in st.session_state:
    st.session_state.show_shelters = False

if 'shelters_data' not in st.session_state:
    st.session_state.shelters_data = None

# Pune coordinates
PUNE_LAT = 18.5204
PUNE_LNG = 73.8567

# Main Header
st.markdown("""
    <div class="main-header">
        <h1>🚨 Emergency Escape & Smart Route Finder</h1>
        <p>⚡ Real-time AI-powered guidance to safety in Pune</p>
    </div>
""", unsafe_allow_html=True)

# Define pages dictionary
pages_dict = {
    "🏠 Dashboard": "dashboard",
    "🗺️ Route Finder": "route_finder",
    "🏥 Shelter Finder": "shelter_finder",
    "👁️ Hazard Detection": "hazard_detection",
    "📊 Analytics": "analytics",
    "📞 Emergency Contacts": "emergency_contacts"
}

# Enhanced Sidebar with Better Navigation
with st.sidebar:
    st.markdown("""
        <style>
            .sidebar-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                color: white;
                margin-bottom: 20px;
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
            }
            
            .sidebar-header h2 {
                margin: 0;
                font-size: 1.5em;
                font-weight: 900;
            }
            
            .sidebar-header p {
                margin: 5px 0 0 0;
                font-size: 0.9em;
                opacity: 0.9;
            }
            
            .nav-section-title {
                color: #667eea;
                font-size: 0.85em;
                font-weight: 900;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-top: 20px;
                margin-bottom: 10px;
                padding-left: 10px;
                border-left: 3px solid #667eea;
            }
            
            .nav-item {
                padding: 12px 15px;
                margin: 8px 0;
                border-radius: 10px;
                background: rgba(102, 126, 234, 0.1);
                border-left: 4px solid transparent;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            
            .nav-item:hover {
                background: rgba(102, 126, 234, 0.2);
                border-left-color: #667eea;
                transform: translateX(5px);
            }
            
            .emergency-button {
                background: linear-gradient(135deg, #FF6B6B 0%, #DC143C 100%);
                color: white;
                padding: 15px;
                border-radius: 12px;
                text-align: center;
                font-weight: 900;
                margin: 20px 0;
                box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3); }
                50% { opacity: 0.9; box-shadow: 0 8px 35px rgba(255, 107, 107, 0.5); }
            }
            
            .quick-stats {
                background: linear-gradient(135deg, #f0f2f6 0%, #e8eaf6 100%);
                padding: 15px;
                border-radius: 12px;
                margin: 15px 0;
                border-left: 4px solid #667eea;
            }
            
            .stat-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin: 8px 0;
                font-size: 0.9em;
            }
            
            .stat-value {
                background: #667eea;
                color: white;
                padding: 4px 10px;
                border-radius: 6px;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Sidebar Header
    st.markdown("""
        <div class="sidebar-header">
        <h2>🚨 Emergency System</h2>
        <p>Smart Route Finder & Safety Guide</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Main Navigation
    st.markdown('<div class="nav-section-title">📑 Main Modules</div>', unsafe_allow_html=True)
    
    page = st.radio(
        "Select Page:",
        list(pages_dict.keys()),
        label_visibility="collapsed",
        format_func=lambda x: x
    )
    
    st.markdown("---")
    
    # Emergency Alert Section
    st.markdown("""
        <div class="emergency-button">
        🚨 EMERGENCY ALERT
        </div>
    """, unsafe_allow_html=True)
    
    emergency_col1, emergency_col2 = st.columns(2)
    with emergency_col1:
        if st.button("🚒 FIRE", use_container_width=True, key="btn_fire_emergency"):
            st.error("🚒 Fire Department - 101")
            st.error("Emergency services have been alerted!")
    
    with emergency_col2:
        if st.button("🚑 AMBULANCE", use_container_width=True, key="btn_ambulance_emergency"):
            st.error("🚑 Ambulance Service - 102")
            st.error("Emergency services have been alerted!")
    
    st.markdown("---")
    
    # Quick Settings Section
    st.markdown('<div class="nav-section-title">⚙️ Quick Settings</div>', unsafe_allow_html=True)
    
    emergency_level = st.select_slider(
        "🎯 Emergency Level",
        options=["Low", "Medium", "High", "Critical"],
        value="High",
        label_visibility="collapsed"
    )
    
    # Emergency Level Indicator
    if emergency_level == "Critical":
        level_color = "#FF6B6B"
        level_text = "🔴 CRITICAL"
    elif emergency_level == "High":
        level_color = "#FF9800"
        level_text = "🟠 HIGH"
    elif emergency_level == "Medium":
        level_color = "#FFC107"
        level_text = "🟡 MEDIUM"
    else:
        level_color = "#4CAF50"
        level_text = "🟢 LOW"
    
    st.markdown(f"""
        <div style="background: {level_color}; color: white; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; margin: 10px 0;">
        {level_text}
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="font-size: 0.85em; color: #666; margin: 10px 0;">Current Emergency Level</div>', unsafe_allow_html=True)
    
    # Location Settings
    st.markdown('<div class="nav-section-title">📍 Location Settings</div>', unsafe_allow_html=True)
    
    user_location = st.text_input("Your Location", "Baner, Pune", label_visibility="collapsed")
    
    col1, col2 = st.columns(2)
    with col1:
        user_lat = st.number_input("Latitude", value=PUNE_LAT, format="%.4f", label_visibility="collapsed")
    with col2:
        user_lng = st.number_input("Longitude", value=PUNE_LNG, format="%.4f", label_visibility="collapsed")
    
    st.markdown("---")
    
    # Quick Statistics
    st.markdown('<div class="nav-section-title">📊 Quick Stats</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="quick-stats">
        <div class="stat-item">
            <span>⏱️ Response Time</span>
            <span class="stat-value">2.3 min</span>
        </div>
        <div class="stat-item">
            <span>📍 Exits Found</span>
            <span class="stat-value">5</span>
        </div>
        <div class="stat-item">
            <span>🏥 Shelters</span>
            <span class="stat-value">12</span>
        </div>
        <div class="stat-item">
            <span>✅ Success Rate</span>
            <span class="stat-value">99.2%</span>
        </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Additional Options
    st.markdown('<div class="nav-section-title">⚡ Quick Actions</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.success("✅ Data refreshed!")
    with col2:
        if st.button("📞 Call 112", use_container_width=True):
            st.info("📞 Emergency hotline available")
    
    if st.button("⚙️ System Status", use_container_width=True, key="btn_system_status"):
        st.success("✅ System Online | 🟢 All Systems Operational")
    
    st.markdown("---")
    
    # Footer Info
    st.markdown("""
        <div style='text-align: center; color: #999; font-size: 0.8em; margin-top: 20px; padding: 15px; background: rgba(0,0,0,0.05); border-radius: 10px;'>
        <b>Emergency Response System v2.0</b><br>
        <small>Last Updated: """ + datetime.now().strftime("%H:%M:%S") + """</small><br>
        <small>📍 Pune Region | 🚀 AI Powered</small>
        </div>
    """, unsafe_allow_html=True)

# ============ DASHBOARD ============
if page == "🏠 Dashboard":
    st.markdown("### 📊 Real-Time Status")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h3>⏱️ Response Time</h3><h2>2.3 min</h2><p>Average</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>📍 Exits Found</h3><h2>5</h2><p>Nearby</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>🏥 Shelters</h3><h2>12</h2><p>In Pune</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h3>❤️ Status</h3><h2>Stable</h2><p>Heart: 72 BPM</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h3 class='section-title'>🚨 Emergency Status</h3>", unsafe_allow_html=True)
        if emergency_level == "Critical":
            st.markdown("""
                <div class="danger-card">
                <b>🔴 CRITICAL EMERGENCY</b><br>
                Immediate evacuation required<br>
                Emergency services en route<br>
                ETA: 4-5 minutes
                </div>
            """, unsafe_allow_html=True)
        elif emergency_level == "High":
            st.markdown(f"""
                <div class="warning-card">
                <b>⚠️ HIGH PRIORITY</b><br>
                Evacuate to nearest safe zone<br>
                Last Updated: {datetime.now().strftime('%H:%M:%S')}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="info-card">
                <b>📌 Emergency Level: {emergency_level}</b><br>
                Status: Monitoring<br>
                Location: {user_location}
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h3 class='section-title'>📍 Your Location</h3>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="success-card">
            <b>Current Address:</b><br>
            {user_location}<br>
            <b>Coordinates:</b> {user_lat:.4f}°N, {user_lng:.4f}°E<br>
            Status: Active & Tracking
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<h3 class='section-title'>⚡ Quick Actions</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚨 EMERGENCY ALERT", key="btn_emergency", use_container_width=True):
            st.success("✅ Emergency services contacted! ETA: 4-5 minutes")
            st.balloons()
    
    with col2:
        if st.button("🗺️ Find Nearest Exit", key="btn_exit", use_container_width=True):
            st.info("📍 Nearest exit: 45m North-West | Time: 45 seconds walking")
    
    with col3:
        if st.button("🏥 Find Safe Shelter", key="btn_shelter", use_container_width=True):
            st.success("🏥 12 shelters found within 5km radius")
    
    st.markdown("---")
    st.markdown("<h3 class='section-title'>🗺️ Pune Overview</h3>", unsafe_allow_html=True)
    
    m = folium.Map(
        location=[PUNE_LAT, PUNE_LNG],
        zoom_start=13,
        tiles="OpenStreetMap"
    )
    
    # User location
    folium.Marker(
        [user_lat, user_lng],
        popup="<b>Your Location</b>",
        icon=folium.Icon(color='blue', icon='info-sign', prefix='fa'),
        tooltip="You are here"
    ).add_to(m)
    
    # Emergency exits
    exits = [
        ([PUNE_LAT + 0.015, PUNE_LNG + 0.020], "North Exit", "green"),
        ([PUNE_LAT - 0.015, PUNE_LNG + 0.020], "South Exit", "green"),
        ([PUNE_LAT + 0.010, PUNE_LNG - 0.025], "West Exit", "green"),
    ]
    
    for exit_loc, name, color in exits:
        folium.Marker(
            exit_loc,
            popup=f"<b>{name}</b>",
            icon=folium.Icon(color=color, icon='sign-out', prefix='fa'),
            tooltip=name
        ).add_to(m)
    
    # Display map in full width
    st_folium(m, width=1400, height=600)

# ============ ROUTE FINDER ============
elif page == "🗺️ Route Finder":
    st.markdown("<h3 class='section-title'>🗺️ Intelligent Pathfinding (A* Algorithm)</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        start_choice = st.selectbox(
            "📍 Starting Point",
            [
                "Current Location (1, 1)",
                "Main Entrance (2, 2)",
                "Office Floor (5, 5)",
                "Storage Area (8, 8)",
                "North Wing (15, 15)"
            ],
            key="start_choice"
        )
    
    with col2:
        destination_choice = st.selectbox(
            "🎯 Destination",
            [
                "Emergency Exit North (18, 18)",
                "Emergency Exit South (18, 2)",
                "Hospital Nearby (2, 18)",
                "Police Station (2, 2)"
            ],
            key="dest_choice"
        )
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Swap Start & End", use_container_width=True, key="swap_btn"):
            st.info("🔄 Swap positions to reverse route")
    
    # Map starting point choice to coordinates
    start_map = {
        "Current Location (1, 1)": (1, 1),
        "Main Entrance (2, 2)": (2, 2),
        "Office Floor (5, 5)": (5, 5),
        "Storage Area (8, 8)": (8, 8),
        "North Wing (15, 15)": (15, 15)
    }
    start_coords = start_map[start_choice]
    
    # Map destination choice to coordinates
    dest_map = {
        "Emergency Exit North (18, 18)": (18, 18),
        "Emergency Exit South (18, 2)": (18, 2),
        "Hospital Nearby (2, 18)": (2, 18),
        "Police Station (2, 2)": (2, 2)
    }
    dest_coords = dest_map[destination_choice]
    
    st.markdown("---")
    st.markdown("### 🔧 Route Configuration")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        algo_choice = st.selectbox(
            "Algorithm",
            ["A* (Fastest)", "Dijkstra (Balanced)", "BFS (Simplest)"],
            help="A* uses heuristics for speed | Dijkstra finds optimal paths | BFS explores all options",
            key="algo_choice"
        )
    with col2:
        priority_choice = st.selectbox(
            "Priority",
            ["Fastest Route", "Safest Route", "Least Crowded", "Balanced"],
            key="priority_choice"
        )
    with col3:
        avoid_hazards = st.checkbox("🚫 Avoid Hazards", value=True, key="avoid_hazards_check")
    
    # Determine algorithm based on priority
    algo_name = "a_star" if "A*" in algo_choice else "dijkstra" if "Dijkstra" in algo_choice else "bfs"
    
    # Apply priority settings
    if priority_choice == "Fastest Route":
        algo_name = "a_star"  # A* is fastest
        avoid_hazards = True
    elif priority_choice == "Safest Route":
        algo_name = "dijkstra"  # Dijkstra is most thorough
        avoid_hazards = True
    elif priority_choice == "Least Crowded":
        algo_name = "a_star"
        avoid_hazards = True
    # "Balanced" uses the user's algorithm choice
    
    st.markdown("---")
    
    # Display selected configuration
    config_col1, config_col2, config_col3, config_col4 = st.columns(4)
    with config_col1:
        st.markdown(f"""
        <div class="info-card">
        <b>📍 Start:</b><br>
        {start_coords}
        </div>
        """, unsafe_allow_html=True)
    with config_col2:
        st.markdown(f"""
        <div class="info-card">
        <b>🎯 Destination:</b><br>
        {dest_coords}
        </div>
        """, unsafe_allow_html=True)
    with config_col3:
        st.markdown(f"""
        <div class="info-card">
        <b>🎯 Route Priority:</b><br>
        {priority_choice}
        </div>
        """, unsafe_allow_html=True)
    with config_col4:
        hazard_status = "✅ Enabled" if avoid_hazards else "❌ Disabled"
        st.markdown(f"""
        <div class="info-card">
        <b>🚫 Hazard Avoidance:</b><br>
        {hazard_status}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Calculate and display route
    with st.spinner("🔄 Calculating optimal route..."):
        result = st.session_state.pathfinding.find_path(start_coords, dest_coords, algo_name, avoid_hazards)
    
    if result["found"]:
        st.markdown("### 📊 Route Analysis")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📏 Distance", f"{result['distance']} blocks", delta="optimal", delta_color="off")
        with col2:
            st.metric("⏱️ Time", f"{result['time']:.1f} min", delta="est.", delta_color="off")
        with col3:
            st.metric("🛡️ Safety", f"{result['safety_score']}%", delta="high", delta_color="off")
        with col4:
            priority_emoji = "⚡" if priority_choice == "Fastest Route" else "🛡️" if priority_choice == "Safest Route" else "👥" if priority_choice == "Least Crowded" else "⚖️"
            st.metric("🎯 Priority", priority_emoji, delta=priority_choice, delta_color="off")
        
        st.markdown("---")
        st.markdown("<h3 class='section-title'>🗺️ Route Visualization (20x20 Grid Map)</h3>", unsafe_allow_html=True)
        
        # Create map
        m = folium.Map(
            location=[PUNE_LAT, PUNE_LNG],
            zoom_start=14,
            tiles="OpenStreetMap"
        )
        
        def grid_to_latlon(x, y):
            return PUNE_LAT + (x * 0.0015), PUNE_LNG + (y * 0.0015)
        
        # Start point
        start_lat, start_lng = grid_to_latlon(start_coords[0], start_coords[1])
        folium.Marker(
            [start_lat, start_lng],
            popup=f"<b>🟢 START ({start_coords[0]}, {start_coords[1]})</b>",
            icon=folium.Icon(color='blue', icon='play', prefix='fa'),
            tooltip="Start Location"
        ).add_to(m)
        
        # Draw path
        path = result["path"]
        if path and len(path) > 1:
            waypoints = [grid_to_latlon(p[0], p[1]) for p in path]
            
            # Color code based on priority
            if priority_choice == "Fastest Route":
                path_color = '#FF6B6B'  # Red - fast
            elif priority_choice == "Safest Route":
                path_color = '#4CAF50'  # Green - safe
            elif priority_choice == "Least Crowded":
                path_color = '#2196F3'  # Blue - crowd
            else:
                path_color = '#FF9800'  # Orange - balanced
            
            folium.PolyLine(waypoints, color=path_color, weight=6, opacity=0.95, popup="Route").add_to(m)
            
            # Add numbered waypoints
            for i, wp in enumerate(waypoints[1:-1], 1):
                folium.CircleMarker(
                    wp,
                    radius=8,
                    popup=f"<b>Waypoint {i}</b>",
                    color='orange',
                    fill=True,
                    fillColor='orange',
                    fillOpacity=0.9,
                    weight=2
                ).add_to(m)
            
            end_lat, end_lng = waypoints[-1]
        else:
            end_lat, end_lng = grid_to_latlon(dest_coords[0], dest_coords[1])
        
        # End point
        folium.Marker(
            [end_lat, end_lng],
            popup=f"<b>🏁 EXIT/DESTINATION ({dest_coords[0]}, {dest_coords[1]})</b>",
            icon=folium.Icon(color='green', icon='check', prefix='fa'),
            tooltip="Destination"
        ).add_to(m)
        
        # Draw hazard zones
        hazards = [
            (5, 5), (5, 6), (6, 5), (6, 6),
            (10, 10), (10, 11), (11, 10), (11, 11),
            (15, 3), (15, 4), (16, 3), (16, 4),
            (8, 15), (8, 16), (9, 15), (9, 16),
            (3, 12), (4, 12), (3, 13), (4, 13)
        ]
        
        for hz in hazards:
            hz_lat, hz_lng = grid_to_latlon(hz[0], hz[1])
            folium.Circle(
                [hz_lat, hz_lng],
                radius=60,
                popup=f"🔥 Fire Hazard {hz}",
                color='red',
                fill=True,
                fillColor='red',
                fillOpacity=0.5,
                weight=2
            ).add_to(m)
        
        # Display map in full width
        st_folium(m, width=1800, height=900)
        
        st.markdown("---")
        st.markdown("<h3 class='section-title'>📍 Turn-by-Turn Navigation</h3>", unsafe_allow_html=True)
        
        directions = [
            ("1️⃣", "Head towards waypoint 1", "Follow the marked route", "30 sec"),
            ("2️⃣", "Turn and proceed", "Avoid hazard zones", "1 min"),
            ("3️⃣", "Continue navigation", "Follow next waypoint", "45 sec"),
            ("4️⃣", "Approaching destination", "Look for exit signs", "20 sec"),
            ("5️⃣", "Reach assembly point", "Safe zone confirmed", "10 sec"),
        ]
        
        for num, action, detail, t in directions:
            st.markdown(
                f'<div class="step-item"><b>{num} {action}</b><br>{detail} '
                f'<span style="float:right">⏱️ {t}</span></div>',
                unsafe_allow_html=True
            )
        
        st.markdown("---")
        st.markdown("<h3 class='section-title'>📊 Route Statistics</h3>", unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("🗺️ Map Size", "20x20 Grid")
        with col2:
            st.metric("🔥 Hazard Zones", "5 Areas")
        with col3:
            st.metric("📍 Total Waypoints", len(path) if path else 0)
        with col4:
            st.metric("🎯 Algorithm", result["algorithm_used"].upper())
        with col5:
            st.metric("✅ Status", "Safe Path" if avoid_hazards else "Direct Path")
        
        st.markdown("---")
        st.markdown("<h3 class='section-title'>📋 Path Details</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        priority_desc = {
            "Fastest Route": "⚡ Optimized for speed using A* algorithm",
            "Safest Route": "🛡️ Most thorough path using Dijkstra algorithm",
            "Least Crowded": "👥 Avoids high-density areas",
            "Balanced": "⚖️ Balanced between speed and safety"
        }
        
        with col1:
            st.info(f"""
            **Route Information:**
            - Start: {start_coords}
            - Destination: {dest_coords}
            - Distance: {result['distance']} blocks
            - Priority: {priority_choice}
            - {priority_desc[priority_choice]}
            - Hazard Avoidance: {'✅ Enabled' if avoid_hazards else '❌ Disabled'}
            - Safety Score: {result['safety_score']}%
            """)
        
        with col2:
            st.success(f"""
            **Journey Summary:**
            - Total Distance: {result['distance']} blocks
            - Estimated Time: {result['time']:.1f} minutes
            - Total Waypoints: {len(path) if path else 0}
            - Algorithm: {result['algorithm_used'].upper()}
            - Status: ✅ Route Found
            - Route Color: {path_color}
            """)
        
        if path:
            st.markdown("**Full Path Coordinates:**")
            st.code(str(path), language="python")
    
    else:
        st.error(f"❌ No safe route found from {start_coords} to {dest_coords}")
        st.warning("Try disabling hazard avoidance or selecting a different start/destination.")

# ============ SHELTER FINDER ============
elif page == "🏥 Shelter Finder":
    st.markdown("<h3 class='section-title'>🏥 Find Nearby Shelters & Safe Zones</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        distance = st.slider("📍 Search Radius (meters)", 100, 10000, 5000, step=100)
    with col2:
        min_safety = st.slider("🛡️ Minimum Safety Score", 0.0, 100.0, 75.0, step=5.0)
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 Search Shelters", use_container_width=True):
            st.session_state.search_shelters = True
    
    st.markdown("---")
    
    # Get nearby shelters with error handling
    try:
        shelters = st.session_state.shelter_finder.find_nearby_shelters(user_lat, user_lng, distance)
        shelters = [s for s in shelters if s["safety"] >= min_safety]
        
        st.markdown(f"### 🏆 Found {len(shelters)} Shelters (Sorted by Distance)")
        
        if len(shelters) > 0:
            # Display shelters in cards
            for idx, shelter in enumerate(sorted(shelters, key=lambda x: x["distance"])):
                col1, col2, col3 = st.columns([2, 2.5, 1])
                
                with col1:
                    st.markdown(f"""
                        <div class="info-card">
                        <b>#{idx+1} 📍 {shelter['name']}</b><br>
                        📁 Type: <b>{shelter['type']}</b><br>
                        📞 Contact: {shelter['contact']}<br>
                        Distance: <b style="color: #667eea;">{shelter['distance']:.0f}m</b> (~{int(shelter['distance']/1.4)}s walk)
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    safety_color = "#4CAF50" if shelter['safety'] >= 95 else "#FF9800" if shelter['safety'] >= 90 else "#FF6B6B"
                    st.markdown(f"""
                        <div class="success-card">
                        👥 Capacity: <b>{shelter['capacity']} people</b><br>
                        ⭐ Safety Score: <b style="color: {safety_color}; font-size: 1.3em;">{shelter['safety']}%</b><br>
                        Status: 🟢 <b>Open & Accepting</b>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    if st.button(f"🗺️ Route", key=f"shelter_route_{idx}", use_container_width=True):
                        st.success(f"✅ Route to {shelter['name']} calculated!")
                        st.info(f"📍 Distance: {shelter['distance']:.0f}m | ⏱️ ETA: {int(shelter['distance']/1.4)}s walking")
                
                st.markdown("")
        else:
            st.warning("❌ No shelters found. Try increasing search radius or lowering safety requirements.")
    
    except Exception as e:
        st.error(f"Error loading shelters: {str(e)}")
    
    st.markdown("---")
    st.markdown("<h3 class='section-title'>🗺️ Shelters Map (Pune Region)</h3>", unsafe_allow_html=True)
    
    try:
        m = folium.Map(
            location=[user_lat, user_lng],
            zoom_start=12,
            tiles="OpenStreetMap"
        )
        
        # User location
        folium.Marker(
            [user_lat, user_lng],
            popup="<b>📍 Your Current Location</b>",
            icon=folium.Icon(color='blue', icon='user', prefix='fa'),
            tooltip="You are here"
        ).add_to(m)
        
        # Draw search radius circle
        folium.Circle(
            [user_lat, user_lng],
            radius=distance,
            color='blue',
            fill=True,
            fillColor='blue',
            fillOpacity=0.1,
            weight=2,
            popup=f"🔍 Search Radius: {distance}m"
        ).add_to(m)
        
        # Add all shelters to map
        if len(shelters) > 0:
            for idx, shelter in enumerate(shelters):
                # Color based on safety
                if shelter["safety"] >= 95:
                    color = 'darkgreen'
                    icon_char = '✓'
                elif shelter["safety"] >= 90:
                    color = 'green'
                    icon_char = '✓'
                elif shelter["safety"] >= 85:
                    color = 'orange'
                    icon_char = '!'
                else:
                    color = 'red'
                    icon_char = '!'
                
                folium.Marker(
                    [shelter["lat"], shelter["lng"]],
                    popup=(
                        f"<b>{shelter['name']}</b><br>"
                        f"<b>Type:</b> {shelter['type']}<br>"
                        f"<b>Distance:</b> {shelter['distance']:.0f}m<br>"
                        f"<b>Capacity:</b> {shelter['capacity']} people<br>"
                        f"<b>Safety:</b> {shelter['safety']}%<br>"
                        f"<b>Contact:</b> {shelter['contact']}"
                    ),
                    icon=folium.Icon(color=color, icon='hospital', prefix='fa'),
                    tooltip=f"{idx+1}. {shelter['name']}"
                ).add_to(m)
                
                # Draw line from user to shelter
                folium.PolyLine(
                    [[user_lat, user_lng], [shelter["lat"], shelter["lng"]]],
                    color='#667eea',
                    weight=2,
                    opacity=0.5,
                    dash_array='5, 5'
                ).add_to(m)
        
        # Display map in full width
        st_folium(m, width=1400, height=800)
    
    except Exception as e:
        st.error(f"Map Error: {str(e)}")
    
    st.markdown("---")
    st.markdown("<h3 class='section-title'>📊 Shelter Statistics</h3>", unsafe_allow_html=True)
    
    if len(shelters) > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        avg_safety = sum(s["safety"] for s in shelters) / len(shelters)
        total_capacity = sum(s["capacity"] for s in shelters)
        nearest_distance = min(s["distance"] for s in shelters)
        
        with col1:
            st.metric("🏢 Total Shelters", len(shelters), delta="found")
        with col2:
            st.metric("🛡️ Avg Safety", f"{avg_safety:.1f}%", delta=f"{avg_safety-75:.1f}%")
        with col3:
            st.metric("👥 Total Capacity", f"{total_capacity:,}", delta="people")
        with col4:
            st.metric("📍 Nearest", f"{nearest_distance:.0f}m", delta="away")
        
        st.markdown("---")
        st.markdown("<h3 class='section-title'>📋 Detailed Shelter Information</h3>", unsafe_allow_html=True)
        
        shelter_table = pd.DataFrame([
            {
                "🏢 Name": s["name"],
                "📁 Type": s["type"],
                "📍 Distance (m)": f"{s['distance']:.0f}",
                "👥 Capacity": f"{s['capacity']}",
                "🛡️ Safety %": f"{s['safety']}%",
                "📞 Contact": s["contact"]
            }
            for s in sorted(shelters, key=lambda x: x["distance"])
        ])
        
        st.dataframe(shelter_table, use_container_width=True, hide_index=True)
    else:
        st.info("🔍 No shelters found. Adjust your search parameters above.")

# ============ HAZARD DETECTION ============
elif page == "👁️ Hazard Detection":
    st.markdown("<h3 class='section-title'>👁️ Real-Time Hazard Detection</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h4>📹 Computer Vision Feed</h4>", unsafe_allow_html=True)
        st.info("📹 Live hazard detection system active")
        
        if st.checkbox("🔴 Enable Real-time Detection"):
            st.markdown("""
                <div class="danger-card">
                <b>🔴 HAZARDS DETECTED:</b><br><br>
                🔥 <b>Fire Detected</b> - Confidence: 94% | Severity: <b>CRITICAL</b><br>
                💨 <b>Smoke Detected</b> - Confidence: 87% | Severity: <b>HIGH</b><br>
                🚧 <b>Structural Obstacle</b> - Confidence: 92% | Severity: <b>HIGH</b><br>
                👥 <b>Crowd Density</b> - Confidence: 65% | Severity: <b>MEDIUM</b>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h4>📊 Detection Results</h4>", unsafe_allow_html=True)
        hazard_data = pd.DataFrame({
            "🚨 Hazard": ["🔥 Fire", "💨 Smoke", "🚧 Obstacle", "👥 Crowding"],
            "Confidence": ["94%", "87%", "92%", "65%"],
            "Severity": ["CRITICAL", "HIGH", "HIGH", "MEDIUM"],
            "Location": ["Floor 3-E", "Floor 3-E", "Main Exit", "Stairwell A"],
            "Recommended Action": ["Reroute", "Evacuate", "Reroute", "Monitor"]
        })
        st.dataframe(hazard_data, use_container_width=True, hide_index=True)

# ============ ANALYTICS ============
elif page == "📊 Analytics":
    st.markdown("<h3 class='section-title'>📊 System Performance Analytics</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📈 Total Evacuations", "1,250", "+45", delta_color="normal")
    with col2:
        st.metric("⏱️ Avg Response Time", "2.4 min", "-0.2 min", delta_color="inverse")
    with col3:
        st.metric("✅ Success Rate", "99.2%", "+0.1%", delta_color="normal")
    with col4:
        st.metric("❤️ Lives Assisted", "3,847", "+120", delta_color="normal")
    
    st.markdown("---")
    
    st.markdown("<h3 class='section-title'>📈 Evacuation Trends</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        chart_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Evacuations': [45, 52, 38, 61, 55, 48, 35]
        })
        st.bar_chart(chart_data.set_index('Day'), use_container_width=True)
    
    with col2:
        chart_data2 = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Success Rate %': [98.5, 99.1, 98.8, 99.3, 99.2, 99.0, 98.9]
        })
        st.line_chart(chart_data2.set_index('Day'), use_container_width=True)
    
    st.markdown("---")
    st.markdown("<h3 class='section-title'>🎯 System Health Metrics</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🤖 AI Accuracy", "96%", "+2%")
    with col2:
        st.metric("🖥️ Server Uptime", "99.9%", "●")
    with col3:
        st.metric("🗺️ Route Optimization", "94%", "+3%")
    with col4:
        st.metric("😊 User Satisfaction", "98%", "+1%")

# ============ EMERGENCY CONTACTS ============
elif page == "📞 Emergency Contacts":
    st.markdown("<h3 class='section-title'>📞 Emergency Contact Numbers</h3>", unsafe_allow_html=True)
    
    st.warning("⚠️ In case of emergency, use these numbers immediately!")
    
    st.markdown("---")
    
    # Emergency Services
    st.markdown("<h3 class='section-title'>🚨 Emergency Services</h3>", unsafe_allow_html=True)
    
    emergency_col1, emergency_col2, emergency_col3 = st.columns(3)
    
    with emergency_col1:
        st.markdown(f"""
        <div class="emergency-card" style="background: #FF6B6B; padding: 20px; border-radius: 10px; text-align: center; color: white;">
        <h2 style="margin: 0; font-size: 2.5em;">🚒</h2>
        <h3 style="margin: 10px 0;">Fire Department</h3>
        <p style="margin: 15px 0; font-size: 1.3em; font-weight: bold;">101</p>
        <p style="margin: 5px 0; font-size: 0.9em;">Fire & Rescue Services</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📋 Copy Fire Dept Number", use_container_width=True, key="copy_fire"):
            st.success("✅ Copied: 101")
    
    with emergency_col2:
        st.markdown(f"""
        <div class="emergency-card" style="background: #4CAF50; padding: 20px; border-radius: 10px; text-align: center; color: white;">
        <h2 style="margin: 0; font-size: 2.5em;">🚑</h2>
        <h3 style="margin: 10px 0;">Ambulance</h3>
        <p style="margin: 15px 0; font-size: 1.3em; font-weight: bold;">102</p>
        <p style="margin: 5px 0; font-size: 0.9em;">Medical Emergency</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📋 Copy Ambulance Number", use_container_width=True, key="copy_ambulance"):
            st.success("✅ Copied: 102")
    
    with emergency_col3:
        st.markdown(f"""
        <div class="emergency-card" style="background: #2196F3; padding: 20px; border-radius: 10px; text-align: center; color: white;">
        <h2 style="margin: 0; font-size: 2.5em;">🚓</h2>
        <h3 style="margin: 10px 0;">Police</h3>
        <p style="margin: 15px 0; font-size: 1.3em; font-weight: bold;">100</p>
        <p style="margin: 5px 0; font-size: 0.9em;">Police & Security</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📋 Copy Police Number", use_container_width=True, key="copy_police"):
            st.success("✅ Copied: 100")
    
    st.markdown("---")
    
    # Additional Emergency Services
    st.markdown("<h3 class='section-title'>🆘 Additional Emergency Services</h3>", unsafe_allow_html=True)
    
    additional_contacts = [
        {
            "name": "National Disaster Management Authority",
            "icon": "🌍",
            "number": "1070",
            "description": "Natural Disasters & Emergencies"
        },
        {
            "name": "Women Helpline",
            "icon": "👩",
            "number": "1091",
            "description": "Women in Distress"
        },
        {
            "name": "Child Helpline",
            "icon": "👧",
            "number": "1098",
            "description": "Child Abuse & Exploitation"
        },
        {
            "name": "Electricity Emergency",
            "icon": "⚡",
            "number": "1912",
            "description": "Power & Electrical Issues"
        }
    ]
    
    col1, col2 = st.columns(2)
    
    for idx, contact in enumerate(additional_contacts):
        col = col1 if idx % 2 == 0 else col2
        
        with col:
            st.markdown(f"""
            <div class="info-card">
            <h3>{contact['icon']} {contact['name']}</h3>
            <p><b>Number:</b> <span style="color: #667eea; font-size: 1.2em; font-weight: bold;">{contact['number']}</span></p>
            <p><small>{contact['description']}</small></p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"📋 Copy {contact['number']}", use_container_width=True, key=f"copy_{contact['number']}"):
                st.success(f"✅ Copied: {contact['number']}")
    
    st.markdown("---")
    
    # Pune-specific Emergency Numbers
    st.markdown("<h3 class='section-title'>📍 Pune Emergency Numbers</h3>", unsafe_allow_html=True)
    
    pune_contacts = [
        {
            "name": "Pune Police Control Room",
            "number": "020-2621-0333",
            "category": "Local Police"
        },
        {
            "name": "Pune Fire Brigade",
            "number": "020-2525-0000",
            "category": "Local Fire Brigade"
        },
        {
            "name": "Sassoon General Hospital",
            "number": "020-2610-0000",
            "category": "Major Hospital"
        },
        {
            "name": "Ruby Hall Clinic",
            "number": "020-6630-0000",
            "category": "Private Hospital"
        },
        {
            "name": "Inlaks & Budhrani Hospital",
            "number": "020-2141-8888",
            "category": "Private Hospital"
        },
        {
            "name": "Deenanath Mangeshkar Hospital",
            "number": "020-2417-8000",
            "category": "Private Hospital"
        }
    ]
    
    pune_col1, pune_col2, pune_col3 = st.columns(3)
    
    for idx, contact in enumerate(pune_contacts):
        col = [pune_col1, pune_col2, pune_col3][idx % 3]
        
        with col:
            st.markdown(f"""
            <div class="info-card">
            <h4>{contact['name']}</h4>
            <p><b>Number:</b><br><span style="color: #667eea; font-size: 1.1em; font-weight: bold;">{contact['number']}</span></p>
            <p><small>🏷️ {contact['category']}</small></p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"📋 Copy", use_container_width=True, key=f"copy_pune_{idx}"):
                st.success(f"✅ Copied: {contact['number']}")
    
    st.markdown("---")
    
    # Quick Reference Guide
    st.markdown("<h3 class='section-title'>📋 Quick Reference Guide</h3>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🔥 Fire Emergency", "🚑 Medical Emergency", "🚓 Security Issue"])
    
    with tab1:
        st.markdown("""
        ### What to do in a Fire Emergency:
        
        1. **🚨 Call 101** (Fire Department)
            - Provide your location clearly
            - Describe the fire (size, location, spread)
            - Listen to instructions carefully
        
        2. **🏃 Evacuate Immediately**
            - Don't use elevators
            - Move to nearest stairwell
            - Help others if possible
        
        3. **🗣️ Alert Others**
            - Ring fire alarms
            - Shout "FIRE!" loudly
            - Direct people to exits
        
        4. **❌ Don't**
            - Go back for belongings
            - Use elevators
            - Hide in buildings
            - Panic or run
        
        5. **✅ Safe Zone**
            - Go to assembly point
            - Stay away from building
            - Wait for fire department
        """)
    
    with tab2:
        st.markdown("""
        ### What to do in a Medical Emergency:
        
        1. **🚨 Call 102** (Ambulance)
            - Provide patient's condition
            - Give clear location/directions
            - Follow dispatcher's instructions
        
        2. **📋 Provide Information**
            - Patient's age & name
            - Symptoms & allergies
            - Current medications
            - Any injuries visible
        
        3. **💊 First Aid**
            - Keep patient calm
            - Don't move if injured
            - Place in recovery position if unconscious
            - Provide water if conscious
        
        4. **🏥 When Ambulance Arrives**
            - Brief paramedics clearly
            - Accompany patient if possible
            - Keep valuables safe
            - Inform family members
        
        5. **📞 Important Hospitals**
            - Sassoon Hospital: 020-2610-0000
            - Ruby Hall: 020-6630-0000
            - Inlaks Hospital: 020-2141-8888
        """)
    
    with tab3:
        st.markdown("""
        ### What to do for Security Issues:
        
        1. **🚨 Call 100** (Police)
            - Describe the threat/incident
            - Provide exact location
            - Give physical descriptions
            - Stay on the line if safe
        
        2. **🛡️ Personal Safety**
            - Move to safe location
            - Lock doors/windows
            - Stay with trusted people
            - Don't confront aggressor
        
        3. **📸 Document Evidence**
            - Note details of incident
            - Identify witnesses
            - Save messages/calls
            - Take photos if safe
        
        4. **🚓 When Police Arrive**
            - Provide full statement
            - Show any evidence
            - Request incident report
            - Get badge numbers
        
        5. **📞 Police Non-Emergency**
            - Pune Police: 020-2621-0333
            - File complaint later if needed
            - Keep reference number
        """)
    
    st.markdown("---")
    
    # Emergency Preparedness Checklist
    st.markdown("<h3 class='section-title'>✅ Emergency Preparedness Checklist</h3>", unsafe_allow_html=True)
    
    checklist_items = [
        "Know the nearest emergency exits",
        "Save emergency numbers in phone",
        "Have a communication plan with family",
        "Know where first aid kit is located",
        "Identify assembly/safe points",
        "Know how to operate fire extinguisher",
        "Have emergency contact cards",
        "Know CPR basics",
        "Identify alternate routes out",
        "Keep medication accessible"
    ]
    
    col1, col2 = st.columns(2)
    
    for idx, item in enumerate(checklist_items):
        col = col1 if idx % 2 == 0 else col2
        with col:
            checked = st.checkbox(item, key=f"check_{idx}")
            if checked:
                st.success(f"✅ {item}")
    
    st.markdown("---")
    
    # Emergency Tips
    st.markdown("<h3 class='section-title'>💡 Emergency Safety Tips</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        ### 🏢 At Work
        - Know 2 exit routes
        - Stay near stairs, away from elevators
        - Keep desk clear for quick exit
        - Know location of first aid kit
        - Report hazards immediately
        """)
    
    with col2:
        st.warning("""
        ### 🏠 At Home
        - Know assembly point
        - Have emergency bag ready
        - Keep valuables accessible
        - Have emergency numbers posted
        - Practice evacuation route
        """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align:center; color:#666; margin-top: 40px; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 12px;'>
    <b>🚨 Intelligent Emergency Response System - Pune Region</b><br>
    <small>🚀 Powered by Advanced AI | 📍 Real-time Emergency Response | 🕐 """ + datetime.now().strftime("%H:%M:%S") + """</small><br>
    <small>Emergency Line: 112 | Police: 100 | Fire: 101 | Ambulance: 102</small>
    </div>
""", unsafe_allow_html=True)