# YouTube API Configuration
# Get your API key from https://console.developers.google.com/
# Make sure to enable YouTube Data API v3 for your project

import os

# Replace with your actual API key or set as environment variable
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "YOUR_YOUTUBE_API_KEY_HERE")

# YouTube API settings
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Data collection settings
MAX_RESULTS_PER_REQUEST = int(
    os.getenv("MAX_RESULTS_PER_REQUEST", "50")
)  # YouTube API limit
DEFAULT_DAYS_THRESHOLD = int(
    os.getenv("DEFAULT_DAYS_THRESHOLD", "1")
)  # Minimum days since upload to calculate growth
