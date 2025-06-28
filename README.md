# StreamR 🎵

StreamR is a Streamlit-based web application designed for Spotify artists and their networks to collaborate and grow streaming numbers in a data-driven way.

## Features

- **Track Drop Manager**: Monitor release performance with streams, saves, and playlist metrics
- **Member Hub**: Track network participation and support statistics
- **Curator Push**: Manage playlist curator outreach efforts
- **Performance Dashboard**: Visualize growth and engagement metrics
- **Spotify Integration**: Direct access to Spotify data via OAuth

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd streamr
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
```
Edit `.env` with your Spotify API credentials:
- Get credentials from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- Set `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`
- Configure `SPOTIFY_REDIRECT_URI` (default: http://localhost:8501/callback)

5. Run the application:
```bash
streamlit run app.py
```

## Project Structure

```
streamr/
├── app.py              # Main Streamlit application
├── spotify_auth.py     # Spotify OAuth and API handling
├── data_manager.py     # Data storage and retrieval
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── data/              # Data storage directory
    ├── tracks.csv
    ├── members.csv
    └── curators.csv
```

## Usage

1. Start the application and navigate to http://localhost:8501
2. Log in with your Spotify account
3. Use the sidebar navigation to access different features:
   - Track releases and performance
   - View member statistics
   - Manage curator outreach
   - Monitor overall performance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.