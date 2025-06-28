import streamlit as st
import pandas as pd
from datetime import datetime
from utils import generate_id, validate_email, validate_spotify_url, format_number

class CuratorManager:
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def render_curator_form(self):
        """Render form for adding new curator"""
        with st.form("add_curator_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Curator/Playlist Name")
                email = st.text_input("Contact Email")
            
            with col2:
                playlist_url = st.text_input("Playlist URL")
                followers = st.number_input("Follower Count", min_value=0)
            
            notes = st.text_area("Additional Notes")
            
            submitted = st.form_submit_button("Add Curator")
            
            if submitted:
                if not name:
                    st.error("Please enter a curator name")
                    return
                
                if email and not validate_email(email):
                    st.error("Please enter a valid email address")
                    return
                
                if playlist_url and not validate_spotify_url(playlist_url):
                    st.error("Please enter a valid Spotify playlist URL")
                    return
                
                curator_data = {
                    'curator_id': generate_id('curator_'),
                    'name': name,
                    'email': email,
                    'playlist_url': playlist_url,
                    'followers': followers,
                    'submission_status': 'Not Submitted',
                    'last_contacted': None,
                    'notes': notes
                }
                
                self.data_manager.add_curator(curator_data)
                st.success("Curator added successfully!")
    
    def render_curator_list(self):
        """Render list of curators with status"""
        curators = self.data_manager.get_curator_stats()
        
        if curators.empty:
            st.info("No curators added yet. Add your first curator above!")
            return
        
        # Add column filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sort_by = st.selectbox(
                "Sort by",
                ["name", "followers", "submission_status", "last_contacted"],
                index=0
            )
        
        with col2:
            status_filter = st.multiselect(
                "Filter by Status",
                ["Not Submitted", "Submitted", "Accepted", "Rejected", "No Response"],
                default=[]
            )
        
        with col3:
            search = st.text_input("Search curators", "")
        
        # Apply filters
        if search:
            curators = curators[curators['name'].str.contains(search, case=False) |
                               curators['email'].str.contains(search, case=False)]
        
        if status_filter:
            curators = curators[curators['submission_status'].isin(status_filter)]
        
        curators = curators.sort_values(by=sort_by, ascending=False)
        
        # Display curators in an expandable format
        for _, curator in curators.iterrows():
            with st.expander(f"{curator['name']} ({format_number(curator['followers'])} followers)"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Contact:**", curator['email'] if curator['email'] else "N/A")
                    st.write("**Playlist:**", f"[Link]({curator['playlist_url']})" if curator['playlist_url'] else "N/A")
                
                with col2:
                    st.write("**Status:**", curator['submission_status'])
                    st.write("**Last Contacted:**", curator['last_contacted'] if curator['last_contacted'] else "Never")
                
                if curator['notes']:
                    st.write("**Notes:**", curator['notes'])
                
                # Update form
                with st.form(f"update_curator_{curator['curator_id']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_status = st.selectbox(
                            "Update Status",
                            ["Not Submitted", "Submitted", "Accepted", "Rejected", "No Response"],
                            index=["Not Submitted", "Submitted", "Accepted", "Rejected", "No Response"].index(curator['submission_status'])
                        )
                        
                        new_followers = st.number_input(
                            "Update Follower Count",
                            min_value=0,
                            value=int(curator['followers'])
                        )
                    
                    with col2:
                        mark_contacted = st.checkbox("Mark as Contacted Today")
                        new_notes = st.text_area("Update Notes", curator['notes'] if curator['notes'] else "")
                    
                    if st.form_submit_button("Update Curator"):
                        update_data = {
                            'submission_status': new_status,
                            'followers': new_followers,
                            'notes': new_notes
                        }
                        
                        if mark_contacted:
                            update_data['last_contacted'] = datetime.now().strftime('%Y-%m-%d')
                        
                        self.data_manager.update_curator(curator['curator_id'], update_data)
                        st.success("Curator updated successfully!")
                        st.rerun()
    
    def get_curator_summary(self):
        """Get summary of curator outreach"""
        curators = self.data_manager.get_curator_stats()
        
        if curators.empty:
            return {
                'total_curators': 0,
                'total_followers': 0,
                'submission_stats': {
                    'Not Submitted': 0,
                    'Submitted': 0,
                    'Accepted': 0,
                    'Rejected': 0,
                    'No Response': 0
                }
            }
        
        submission_stats = curators['submission_status'].value_counts().to_dict()
        
        return {
            'total_curators': len(curators),
            'total_followers': curators['followers'].sum(),
            'submission_stats': submission_stats
        }