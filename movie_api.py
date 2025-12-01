"""
Movie API Module

This module handles all interactions with The Movie Database (TMDb) API.
It provides functions to search for movies and fetch their details and reviews.
"""

import requests
import os
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# TMDb API base URL
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_API_KEY = os.getenv("TMDB_API_KEY")


def search_movie(title: str) -> Optional[Dict]:
    """
    Search for a movie by title using TMDb API.
    
    Args:
        title: The movie title to search for
        
    Returns:
        Dictionary with movie ID, title, and release year if found, None otherwise
        
    Raises:
        ValueError: If API key is missing or invalid
        requests.RequestException: If API request fails
    """
    if not TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY not found in environment variables. Please check your .env file.")
    
    # TMDb search endpoint
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "language": "en-US"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Return the first (best match) result
        if data.get("results") and len(data["results"]) > 0:
            movie = data["results"][0]
            return {
                "id": movie["id"],
                "title": movie["title"],
                "year": movie.get("release_date", "").split("-")[0] if movie.get("release_date") else "Unknown",
                "overview": movie.get("overview", "No overview available.")
            }
        else:
            return None
            
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            raise ValueError("Invalid TMDb API key. Please check your .env file.")
        raise requests.RequestException(f"API request failed: {e}")
    except requests.exceptions.RequestException as e:
        raise requests.RequestException(f"Failed to connect to TMDb API: {e}")


def get_movie_details(movie_id: int) -> Dict:
    """
    Fetch detailed information about a movie including its rating.
    
    Args:
        movie_id: The TMDb movie ID
        
    Returns:
        Dictionary with movie details including vote_average
        
    Raises:
        requests.RequestException: If API request fails
    """
    if not TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY not found in environment variables.")
    
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return {
            "vote_average": data.get("vote_average", 0.0),
            "vote_count": data.get("vote_count", 0),
            "title": data.get("title", ""),
            "release_date": data.get("release_date", ""),
            "overview": data.get("overview", "No overview available.")
        }
        
    except requests.exceptions.RequestException as e:
        raise requests.RequestException(f"Failed to fetch movie details: {e}")


def get_movie_reviews(movie_id: int, max_reviews: int = 50) -> List[Dict]:
    """
    Fetch user reviews for a movie from TMDb.
    
    Args:
        movie_id: The TMDb movie ID
        max_reviews: Maximum number of reviews to fetch (default: 50)
        
    Returns:
        List of dictionaries, each containing:
        - author: Review author name
        - content: Review text
        - created_at: Review creation date
        - rating: Author's rating (if available)
        
    Raises:
        requests.RequestException: If API request fails
    """
    if not TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY not found in environment variables.")
    
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/reviews"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "page": 1
    }
    
    reviews = []
    
    try:
        # Fetch first page of reviews
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract reviews from the response
        for review in data.get("results", [])[:max_reviews]:
            reviews.append({
                "author": review.get("author", "Anonymous"),
                "content": review.get("content", ""),
                "created_at": review.get("created_at", ""),
                "rating": review.get("author_details", {}).get("rating")
            })
        
        return reviews
        
    except requests.exceptions.RequestException as e:
        raise requests.RequestException(f"Failed to fetch movie reviews: {e}")


def get_movie_data(title: str) -> Tuple[Optional[Dict], Optional[List[Dict]]]:
    """
    Convenience function to get both movie details and reviews in one call.
    
    Args:
        title: The movie title to search for
        
    Returns:
        Tuple of (movie_details_dict, reviews_list)
        Returns (None, None) if movie not found
    """
    # Search for the movie
    movie_search = search_movie(title)
    
    if not movie_search:
        return None, None
    
    movie_id = movie_search["id"]
    
    # Fetch details and reviews
    try:
        details = get_movie_details(movie_id)
        reviews = get_movie_reviews(movie_id)
        
        # Merge search result with details
        movie_data = {
            **movie_search,
            **details
        }
        
        return movie_data, reviews
        
    except Exception as e:
        raise Exception(f"Error fetching movie data: {e}")

