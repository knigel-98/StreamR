import streamlit as st
import pandas as pd
from datetime import datetime
from utils import generate_id, calculate_compliance_score, format_number

class MemberManager:
    def __init__(self, data_manager, spotify_auth):
        self.data_manager = data_manager
        self.spotify_auth = spotify_auth
    
    def render_member_form(self):
        """Render form for adding new member"""
        with st.form("add_member_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Member Name")
                spotify_id = st.text_input("Spotify Profile ID (optional)")
            
            with col2:
                streams_given = st.number_input("Initial Streams Given", min_value=0)
                posts_shared = st.number_input("Initial Posts Shared", min_value=0)
            
            submitted = st.form_submit_button("Add Member")
            
            if submitted:
                if not name:
                    st.error("Please enter a member name")
                    return
                
                member_data = {
                    'member_id': generate_id('member_'),
                    'name': name,
                    'spotify_id': spotify_id,
                    'streams_given': streams_given,
                    'posts_shared': posts_shared,
                    'playlists_submitted': 0,
                    'compliance_score': 100  # Initial score
                }
                
                self.data_manager.add_member(member_data)
                st.success("Member added successfully!")
    
    def render_member_list(self):
        """Render list of members with stats"""
        members = self.data_manager.get_member_stats()
        
        if members.empty:
            st.info("No members added yet. Add your first member above!")
            return
        
        # Add column filters
        col1, col2 = st.columns(2)
        
        with col1:
            sort_by = st.selectbox(
                "Sort by",
                ["name", "streams_given", "posts_shared", "compliance_score"],
                index=0
            )
        
        with col2:
            search = st.text_input("Search members", "")
        
        # Apply filters and sorting
        if search:
            members = members[members['name'].str.contains(search, case=False)]
        
        members = members.sort_values(by=sort_by, ascending=False)
        
        # Display members in an expandable format
        for _, member in members.iterrows():
            with st.expander(f"{member['name']}"):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Streams Given", format_number(member['streams_given']))
                
                with col2:
                    st.metric("Posts Shared", format_number(member['posts_shared']))
                
                with col3:
                    st.metric("Playlists Submitted", format_number(member['playlists_submitted']))
                
                with col4:
                    st.metric("Compliance Score", f"{member['compliance_score']:.1f}%")
                
                # Update form
                with st.form(f"update_member_{member['member_id']}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        new_streams = st.number_input(
                            "Update Streams Given",
                            min_value=0,
                            value=int(member['streams_given'])
                        )
                    
                    with col2:
                        new_posts = st.number_input(
                            "Update Posts Shared",
                            min_value=0,
                            value=int(member['posts_shared'])
                        )
                    
                    with col3:
                        new_playlists = st.number_input(
                            "Update Playlists Submitted",
                            min_value=0,
                            value=int(member['playlists_submitted'])
                        )
                    
                    if st.form_submit_button("Update Stats"):
                        # Calculate new compliance score
                        temp_df = members.copy()
                        temp_df.loc[temp_df['member_id'] == member['member_id'], 'streams_given'] = new_streams
                        temp_df.loc[temp_df['member_id'] == member['member_id'], 'posts_shared'] = new_posts
                        temp_df.loc[temp_df['member_id'] == member['member_id'], 'playlists_submitted'] = new_playlists
                        
                        new_score = calculate_compliance_score(temp_df.loc[temp_df['member_id'] == member['member_id']])
                        
                        update_data = {
                            'streams_given': new_streams,
                            'posts_shared': new_posts,
                            'playlists_submitted': new_playlists,
                            'compliance_score': new_score
                        }
                        
                        self.data_manager.update_member(member['member_id'], update_data)
                        st.success("Member stats updated successfully!")
                        st.rerun()
    
    def get_member_performance_summary(self):
        """Get summary of member performance"""
        members = self.data_manager.get_member_stats()
        
        if members.empty:
            return {
                'total_members': 0,
                'total_streams_given': 0,
                'total_posts_shared': 0,
                'total_playlists_submitted': 0,
                'avg_compliance_score': 0
            }
        
        return {
            'total_members': len(members),
            'total_streams_given': members['streams_given'].sum(),
            'total_posts_shared': members['posts_shared'].sum(),
            'total_playlists_submitted': members['playlists_submitted'].sum(),
            'avg_compliance_score': members['compliance_score'].mean()
        }