import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import format_number, format_percentage, get_growth_indicator

class Dashboard:
    def __init__(self, data_manager, analytics_manager):
        self.data_manager = data_manager
        self.analytics = analytics_manager
    
    def render_overview_metrics(self):
        """Render overview metrics section"""
        metrics = self.analytics.calculate_growth_metrics()
        
        # Display key metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Streams",
                format_number(metrics['current_month_streams']),
                format_percentage(metrics['stream_growth']),
                delta_color="normal"
            )
        
        with col2:
            st.metric(
                "Save Rate",
                format_percentage(metrics['save_growth']),
                format_percentage(metrics['save_growth'] - metrics['stream_growth']),
                delta_color="normal"
            )
        
        with col3:
            st.metric(
                "Playlist Adds",
                format_number(metrics['current_month_playlists']),
                format_percentage(metrics['playlist_growth']),
                delta_color="normal"
            )
        
        with col4:
            overall_growth = (metrics['stream_growth'] + 
                            metrics['save_growth'] + 
                            metrics['playlist_growth']) / 3
            st.metric(
                "Overall Growth",
                get_growth_indicator(overall_growth),
                format_percentage(overall_growth),
                delta_color="normal"
            )
    
    def render_performance_charts(self):
        """Render performance visualization section"""
        # Stream trend chart
        stream_trend = self.analytics.generate_stream_trend(days=30)
        if stream_trend:
            st.plotly_chart(stream_trend, use_container_width=True)
        
        # Save rate comparison
        col1, col2 = st.columns(2)
        
        with col1:
            save_rate_chart = self.analytics.generate_save_rate_chart()
            if save_rate_chart:
                st.plotly_chart(save_rate_chart, use_container_width=True)
        
        with col2:
            playlist_impact = self.analytics.generate_playlist_impact()
            if playlist_impact:
                st.plotly_chart(playlist_impact, use_container_width=True)
    
    def render_member_performance(self):
        """Render member performance section"""
        member_chart = self.analytics.generate_member_performance()
        if member_chart:
            st.plotly_chart(member_chart, use_container_width=True)
    
    def render_curator_stats(self):
        """Render curator statistics section"""
        curator_summary = self.data_manager.curators_df
        
        if not curator_summary.empty:
            # Create pie chart for submission status
            status_counts = curator_summary['submission_status'].value_counts()
            
            fig = go.Figure(data=[go.Pie(
                labels=status_counts.index,
                values=status_counts.values,
                hole=.3
            )])
            
            fig.update_layout(
                title="Curator Submission Status Distribution",
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display curator reach metrics
            total_followers = curator_summary['followers'].sum()
            accepted_followers = curator_summary[curator_summary['submission_status'] == 'Accepted']['followers'].sum()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Total Curator Reach",
                    format_number(total_followers)
                )
            
            with col2:
                st.metric(
                    "Accepted Playlist Reach",
                    format_number(accepted_followers)
                )
            
            with col3:
                acceptance_rate = (len(curator_summary[curator_summary['submission_status'] == 'Accepted']) / 
                                 len(curator_summary) * 100)
                st.metric(
                    "Acceptance Rate",
                    f"{acceptance_rate:.1f}%"
                )
    
    def render_export_section(self):
        """Render data export section"""
        st.subheader("Export Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Export Track Data"):
                csv = self.data_manager.tracks_df.to_csv(index=False)
                st.download_button(
                    "Download Track Data",
                    csv,
                    "track_data.csv",
                    "text/csv",
                    key='download-track-csv'
                )
        
        with col2:
            if st.button("Export Member Data"):
                csv = self.data_manager.members_df.to_csv(index=False)
                st.download_button(
                    "Download Member Data",
                    csv,
                    "member_data.csv",
                    "text/csv",
                    key='download-member-csv'
                )
        
        with col3:
            if st.button("Export Curator Data"):
                csv = self.data_manager.curators_df.to_csv(index=False)
                st.download_button(
                    "Download Curator Data",
                    csv,
                    "curator_data.csv",
                    "text/csv",
                    key='download-curator-csv'
                )