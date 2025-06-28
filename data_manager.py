import pandas as pd
from pathlib import Path
from datetime import datetime

class DataManager:
    def __init__(self, data_dir='data'):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize DataFrames
        self.tracks_df = self._load_or_create_df('tracks.csv', [
            'track_id', 'name', 'artist', 'release_date', 'streams',
            'saves', 'playlist_adds', 'created_at', 'updated_at'
        ])
        
        self.members_df = self._load_or_create_df('members.csv', [
            'member_id', 'name', 'spotify_id', 'streams_given',
            'posts_shared', 'playlists_submitted', 'compliance_score',
            'created_at', 'updated_at'
        ])
        
        self.curators_df = self._load_or_create_df('curators.csv', [
            'curator_id', 'name', 'email', 'followers', 'playlist_url',
            'submission_status', 'last_contacted', 'created_at', 'updated_at'
        ])
        
    def _load_or_create_df(self, filename, columns):
        file_path = self.data_dir / filename
        if file_path.exists():
            return pd.read_csv(file_path)
        return pd.DataFrame(columns=columns)
    
    def save_all(self):
        """Save all DataFrames to CSV files"""
        self.tracks_df.to_csv(self.data_dir / 'tracks.csv', index=False)
        self.members_df.to_csv(self.data_dir / 'members.csv', index=False)
        self.curators_df.to_csv(self.data_dir / 'curators.csv', index=False)
    
    # Track management methods
    def add_track(self, track_data):
        track_data['created_at'] = datetime.now()
        track_data['updated_at'] = datetime.now()
        self.tracks_df = pd.concat([self.tracks_df, pd.DataFrame([track_data])], ignore_index=True)
        self.save_all()
        
    def update_track(self, track_id, update_data):
        update_data['updated_at'] = datetime.now()
        self.tracks_df.loc[self.tracks_df['track_id'] == track_id, update_data.keys()] = update_data.values()
        self.save_all()
    
    # Member management methods
    def add_member(self, member_data):
        member_data['created_at'] = datetime.now()
        member_data['updated_at'] = datetime.now()
        self.members_df = pd.concat([self.members_df, pd.DataFrame([member_data])], ignore_index=True)
        self.save_all()
        
    def update_member(self, member_id, update_data):
        update_data['updated_at'] = datetime.now()
        self.members_df.loc[self.members_df['member_id'] == member_id, update_data.keys()] = update_data.values()
        self.save_all()
    
    # Curator management methods
    def add_curator(self, curator_data):
        curator_data['created_at'] = datetime.now()
        curator_data['updated_at'] = datetime.now()
        self.curators_df = pd.concat([self.curators_df, pd.DataFrame([curator_data])], ignore_index=True)
        self.save_all()
        
    def update_curator(self, curator_id, update_data):
        update_data['updated_at'] = datetime.now()
        self.curators_df.loc[self.curators_df['curator_id'] == curator_id, update_data.keys()] = update_data.values()
        self.save_all()
    
    # Analytics methods
    def get_track_stats(self, track_id=None):
        if track_id:
            return self.tracks_df[self.tracks_df['track_id'] == track_id]
        return self.tracks_df
    
    def get_member_stats(self, member_id=None):
        if member_id:
            return self.members_df[self.members_df['member_id'] == member_id]
        return self.members_df
    
    def get_curator_stats(self, curator_id=None):
        if curator_id:
            return self.curators_df[self.curators_df['curator_id'] == curator_id]
        return self.curators_df
    
    def get_performance_metrics(self):
        metrics = {
            'total_streams': self.tracks_df['streams'].sum(),
            'total_saves': self.tracks_df['saves'].sum(),
            'total_playlist_adds': self.tracks_df['playlist_adds'].sum(),
            'save_rate': (self.tracks_df['saves'].sum() / self.tracks_df['streams'].sum() * 100) if self.tracks_df['streams'].sum() > 0 else 0
        }
        return metrics