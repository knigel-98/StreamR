import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SpotifyAuthManager:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI', 'http://127.0.0.1:8502/callback')
        self.scope = [
            'user-read-private',
            'user-read-email',
            'playlist-read-private',
            'playlist-read-collaborative',
            'playlist-modify-public',
            'playlist-modify-private',
            'user-library-read',
            'user-library-modify'
        ]
        
    def get_auth_manager(self):
        return SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            cache_path='.spotify_token_cache'
        )
    
    def get_spotify_client(self):
        auth_manager = self.get_auth_manager()
        return spotipy.Spotify(auth_manager=auth_manager)
    
    def get_user_profile(self, sp_client=None):
        if not sp_client:
            sp_client = self.get_spotify_client()
        return sp_client.current_user()
    
    def get_user_playlists(self, sp_client=None):
        if not sp_client:
            sp_client = self.get_spotify_client()
        return sp_client.current_user_playlists()
    
    def get_track_info(self, track_id, sp_client=None):
        if not sp_client:
            sp_client = self.get_spotify_client()
        return sp_client.track(track_id)
    
    def get_track_audio_features(self, track_id, sp_client=None):
        if not sp_client:
            sp_client = self.get_spotify_client()
        return sp_client.audio_features([track_id])[0]