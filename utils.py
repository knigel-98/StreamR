import uuid
from datetime import datetime
import pandas as pd

def generate_id(prefix=''):
    """Generate a unique ID with optional prefix"""
    return f"{prefix}{str(uuid.uuid4())[:8]}"

def format_number(number):
    """Format large numbers for display"""
    if number >= 1_000_000:
        return f"{number/1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number/1_000:.1f}K"
    return str(number)

def calculate_compliance_score(member_data):
    """Calculate member compliance score based on activity"""
    weights = {
        'streams_given': 0.4,
        'posts_shared': 0.3,
        'playlists_submitted': 0.3
    }
    
    # Get maximum values for normalization
    max_streams = max(member_data['streams_given']) if len(member_data) > 0 else 1
    max_posts = max(member_data['posts_shared']) if len(member_data) > 0 else 1
    max_playlists = max(member_data['playlists_submitted']) if len(member_data) > 0 else 1
    
    # Calculate normalized scores
    normalized_streams = member_data['streams_given'] / max_streams
    normalized_posts = member_data['posts_shared'] / max_posts
    normalized_playlists = member_data['playlists_submitted'] / max_playlists
    
    # Calculate weighted score
    score = (normalized_streams * weights['streams_given'] +
             normalized_posts * weights['posts_shared'] +
             normalized_playlists * weights['playlists_submitted'])
    
    return score * 100

def format_date(date_str):
    """Format date string for display"""
    try:
        date_obj = pd.to_datetime(date_str)
        return date_obj.strftime('%Y-%m-%d')
    except:
        return date_str

def get_growth_indicator(value):
    """Return growth indicator emoji based on value"""
    if value > 0:
        return "📈"
    elif value < 0:
        return "📉"
    return "➡️"

def format_percentage(value):
    """Format percentage value with sign"""
    if value > 0:
        return f"+{value:.1f}%"
    return f"{value:.1f}%"

def validate_email(email):
    """Simple email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_spotify_url(url):
    """Validate Spotify URL format"""
    import re
    pattern = r'^https://open\.spotify\.com/(?:track|playlist|artist)/[a-zA-Z0-9]+'
    return bool(re.match(pattern, url))

def extract_spotify_id(url):
    """Extract Spotify ID from URL"""
    import re
    match = re.search(r'/(?:track|playlist|artist)/([a-zA-Z0-9]+)', url)
    return match.group(1) if match else None

def format_duration_ms(ms):
    """Format milliseconds duration to MM:SS format"""
    seconds = int(ms / 1000)
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:02d}"