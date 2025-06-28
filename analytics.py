import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

class AnalyticsManager:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        
    def generate_stream_trend(self, days=30):
        """Generate streaming trend chart for the last N days"""
        tracks_df = self.data_manager.tracks_df.copy()
        tracks_df['release_date'] = pd.to_datetime(tracks_df['release_date'])
        
        # Filter for recent tracks
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_tracks = tracks_df[tracks_df['release_date'] >= cutoff_date]
        
        if recent_tracks.empty:
            return None
            
        fig = px.line(recent_tracks, 
                      x='release_date', 
                      y='streams',
                      title=f'Streaming Trend (Last {days} Days)',
                      labels={'release_date': 'Date', 'streams': 'Total Streams'})
        return fig
    
    def generate_save_rate_chart(self):
        """Generate save rate comparison chart"""
        tracks_df = self.data_manager.tracks_df.copy()
        
        if tracks_df.empty:
            return None
            
        tracks_df['save_rate'] = (tracks_df['saves'] / tracks_df['streams'] * 100).fillna(0)
        
        fig = px.bar(tracks_df,
                     x='name',
                     y='save_rate',
                     title='Save Rate by Track',
                     labels={'name': 'Track Name', 'save_rate': 'Save Rate (%)'})
        return fig
    
    def generate_playlist_impact(self):
        """Generate playlist impact visualization"""
        tracks_df = self.data_manager.tracks_df.copy()
        
        if tracks_df.empty:
            return None
            
        fig = px.scatter(tracks_df,
                        x='playlist_adds',
                        y='streams',
                        size='saves',
                        hover_data=['name'],
                        title='Playlist Impact Analysis',
                        labels={'playlist_adds': 'Playlist Adds',
                               'streams': 'Total Streams',
                               'saves': 'Total Saves'})
        return fig
    
    def generate_member_performance(self):
        """Generate member performance comparison"""
        members_df = self.data_manager.members_df.copy()
        
        if members_df.empty:
            return None
            
        fig = go.Figure()
        
        # Add traces for different metrics
        fig.add_trace(go.Bar(name='Streams Given',
                            x=members_df['name'],
                            y=members_df['streams_given']))
        
        fig.add_trace(go.Bar(name='Posts Shared',
                            x=members_df['name'],
                            y=members_df['posts_shared']))
        
        fig.add_trace(go.Bar(name='Playlists Submitted',
                            x=members_df['name'],
                            y=members_df['playlists_submitted']))
        
        fig.update_layout(title='Member Performance Comparison',
                         barmode='group',
                         xaxis_title='Member Name',
                         yaxis_title='Count')
        return fig
    
    def calculate_growth_metrics(self):
        """Calculate key growth metrics"""
        tracks_df = self.data_manager.tracks_df.copy()
        tracks_df['release_date'] = pd.to_datetime(tracks_df['release_date'])
        
        current_month = datetime.now().replace(day=1)
        last_month = (current_month - timedelta(days=1)).replace(day=1)
        
        current_month_data = tracks_df[tracks_df['release_date'] >= current_month]
        last_month_data = tracks_df[(tracks_df['release_date'] >= last_month) & 
                                   (tracks_df['release_date'] < current_month)]
        
        metrics = {
            'current_month_streams': current_month_data['streams'].sum(),
            'last_month_streams': last_month_data['streams'].sum(),
            'current_month_saves': current_month_data['saves'].sum(),
            'last_month_saves': last_month_data['saves'].sum(),
            'current_month_playlists': current_month_data['playlist_adds'].sum(),
            'last_month_playlists': last_month_data['playlist_adds'].sum()
        }
        
        # Calculate growth percentages
        metrics['stream_growth'] = self._calculate_growth_percentage(
            metrics['current_month_streams'],
            metrics['last_month_streams']
        )
        
        metrics['save_growth'] = self._calculate_growth_percentage(
            metrics['current_month_saves'],
            metrics['last_month_saves']
        )
        
        metrics['playlist_growth'] = self._calculate_growth_percentage(
            metrics['current_month_playlists'],
            metrics['last_month_playlists']
        )
        
        return metrics
    
    def _calculate_growth_percentage(self, current, previous):
        """Calculate growth percentage between two values"""
        if previous == 0:
            return 100 if current > 0 else 0
        return ((current - previous) / previous) * 100