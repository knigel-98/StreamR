import streamlit as st
import pandas as pd
from datetime import datetime
from utils import generate_id, format_number, format_date, validate_spotify_url, extract_spotify_id

class TrackManager:
    def __init__(self, data_manager, spotify_auth):
        self.data_manager = data_manager
        self.spotify_auth = spotify_auth
        
    def render_track_form(self):
        """Render form for adding new track"""
        with st.form("add_track_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                track_url = st.text_input("Spotify Track URL")
                artist_name = st.text_input("Artist Name")
            
            with col2:
                release_date = st.date_input("Release Date")
                initial_streams = st.number_input("Initial Stream Count", min_value=0)
            
            submitted = st.form_submit_button("Add Track")
            
            if submitted:
                if not validate_spotify_url(track_url):
                    st.error("Please enter a valid Spotify track URL")
                    return
                
                track_id = extract_spotify_id(track_url)
                
                try:
                    # Get track details from Spotify
                    sp_client = self.spotify_auth.get_spotify_client()
                    track_info = self.spotify_auth.get_track_info(track_id, sp_client)
                    
                    track_data = {
                        'track_id': generate_id('track_'),
                        'spotify_id': track_id,
                        'name': track_info['name'],
                        'artist': artist_name or track_info['artists'][0]['name'],
                        'release_date': release_date.strftime('%Y-%m-%d'),
                        'streams': initial_streams,
                        'saves': 0,
                        'playlist_adds': 0
                    }
                    
                    self.data_manager.add_track(track_data)
                    st.success("Track added successfully!")
                    
                except Exception as e:
                    st.error(f"Error adding track: {str(e)}")
    
    def render_track_list(self):
        """Render list of tracks with stats"""
        tracks = self.data_manager.get_track_stats()
        
        if tracks.empty:
            st.info("No tracks added yet. Add your first track above!")
            return
        
        # Add column filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sort_by = st.selectbox(
                "Sort by",
                ["release_date", "streams", "saves", "playlist_adds"],
                index=0
            )
        
        with col2:
            sort_order = st.selectbox(
                "Order",
                ["Descending", "Ascending"],
                index=0
            )
        
        with col3:
            search = st.text_input("Search tracks", "")
        
        # Apply filters and sorting
        if search:
            tracks = tracks[tracks['name'].str.contains(search, case=False) |
                           tracks['artist'].str.contains(search, case=False)]
        
        tracks = tracks.sort_values(
            by=sort_by,
            ascending=(sort_order == "Ascending")
        )
        
        # Display tracks in an expandable format
        for _, track in tracks.iterrows():
            with st.expander(f"{track['name']} - {track['artist']}"):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Streams", format_number(track['streams']))
                
                with col2:
                    st.metric("Saves", format_number(track['saves']))
                
                with col3:
                    st.metric("Playlist Adds", format_number(track['playlist_adds']))
                
                with col4:
                    save_rate = (track['saves'] / track['streams'] * 100) if track['streams'] > 0 else 0
                    st.metric("Save Rate", f"{save_rate:.1f}%")
                
                # Update form
                with st.form(f"update_track_{track['track_id']}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        new_streams = st.number_input(
                            "Update Streams",
                            min_value=0,
                            value=int(track['streams'])
                        )
                    
                    with col2:
                        new_saves = st.number_input(
                            "Update Saves",
                            min_value=0,
                            value=int(track['saves'])
                        )
                    
                    with col3:
                        new_playlist_adds = st.number_input(
                            "Update Playlist Adds",
                            min_value=0,
                            value=int(track['playlist_adds'])
                        )
                    
                    if st.form_submit_button("Update Stats"):
                        update_data = {
                            'streams': new_streams,
                            'saves': new_saves,
                            'playlist_adds': new_playlist_adds
                        }
                        
                        self.data_manager.update_track(track['track_id'], update_data)
                        st.success("Track stats updated successfully!")
                        st.rerun()
    
    def get_track_performance_summary(self):
        """Get summary of track performance"""
        tracks = self.data_manager.get_track_stats()
        
        if tracks.empty:
            return {
                'total_tracks': 0,
                'total_streams': 0,
                'total_saves': 0,
                'total_playlists': 0,
                'avg_save_rate': 0
            }
        
        total_streams = tracks['streams'].sum()
        total_saves = tracks['saves'].sum()
        
        return {
            'total_tracks': len(tracks),
            'total_streams': total_streams,
            'total_saves': total_saves,
            'total_playlists': tracks['playlist_adds'].sum(),
            'avg_save_rate': (total_saves / total_streams * 100) if total_streams > 0 else 0
        }