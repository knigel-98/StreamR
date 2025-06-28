import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

# Import custom modules
from spotify_auth import SpotifyAuthManager
from data_manager import DataManager
from track_manager import TrackManager
from member_manager import MemberManager
from curator_manager import CuratorManager
from analytics import AnalyticsManager
from dashboard import Dashboard

# Configure Streamlit page settings
st.set_page_config(
    page_title="StreamR",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize managers
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = DataManager()

if 'spotify_auth' not in st.session_state:
    st.session_state.spotify_auth = SpotifyAuthManager()

if 'track_manager' not in st.session_state:
    st.session_state.track_manager = TrackManager(
        st.session_state.data_manager,
        st.session_state.spotify_auth
    )

if 'member_manager' not in st.session_state:
    st.session_state.member_manager = MemberManager(
        st.session_state.data_manager,
        st.session_state.spotify_auth
    )

if 'curator_manager' not in st.session_state:
    st.session_state.curator_manager = CuratorManager(
        st.session_state.data_manager
    )

if 'analytics_manager' not in st.session_state:
    st.session_state.analytics_manager = AnalyticsManager(
        st.session_state.data_manager
    )

if 'dashboard' not in st.session_state:
    st.session_state.dashboard = Dashboard(
        st.session_state.data_manager,
        st.session_state.analytics_manager
    )

# Sidebar navigation
st.sidebar.title("StreamR 🎵")

# Spotify Authentication Status
if 'spotify_token' not in st.session_state:
    st.session_state.spotify_token = None

if not st.session_state.spotify_token:
    st.sidebar.warning("⚠️ Not connected to Spotify")
    if st.sidebar.button("Connect Spotify"):
        try:
            spotify_client = st.session_state.spotify_auth.get_spotify_client()
            user_profile = st.session_state.spotify_auth.get_user_profile(spotify_client)
            st.session_state.spotify_token = True
            st.sidebar.success(f"✅ Connected as {user_profile['display_name']}")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Failed to connect: {str(e)}")
else:
    st.sidebar.success("✅ Connected to Spotify")

# Navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["Track Drop Manager", "Member Hub", "Curator Push", "Performance Dashboard"]
)

# Main content area
st.title(page)

if page == "Track Drop Manager":
    st.header("Track Management")
    
    # Add new track section
    with st.expander("Add New Track", expanded=True):
        st.session_state.track_manager.render_track_form()
    
    # Track list
    st.subheader("Your Tracks")
    st.session_state.track_manager.render_track_list()
    
elif page == "Member Hub":
    st.header("Member Management")
    
    # Add new member section
    with st.expander("Add New Member", expanded=True):
        st.session_state.member_manager.render_member_form()
    
    # Member list
    st.subheader("Network Members")
    st.session_state.member_manager.render_member_list()
    
elif page == "Curator Push":
    st.header("Playlist Curator Management")
    
    # Add new curator section
    with st.expander("Add New Curator", expanded=True):
        st.session_state.curator_manager.render_curator_form()
    
    # Curator list
    st.subheader("Curator Database")
    st.session_state.curator_manager.render_curator_list()
    
elif page == "Performance Dashboard":
    # Overview metrics
    st.session_state.dashboard.render_overview_metrics()
    
    # Performance charts
    st.subheader("Performance Analytics")
    st.session_state.dashboard.render_performance_charts()
    
    # Member performance
    st.subheader("Member Performance")
    st.session_state.dashboard.render_member_performance()
    
    # Curator statistics
    st.subheader("Curator Outreach Analytics")
    st.session_state.dashboard.render_curator_stats()
    
    # Export section
    st.session_state.dashboard.render_export_section()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center'>
    Made with ❤️ by StreamForge<br>
    <small>v1.0.0</small>
</div>
""", unsafe_allow_html=True)