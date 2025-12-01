"""
Movie Analyzer Module

This module combines movie data, reviews, and sentiment analysis to generate
a final verdict on whether a movie is "good", "mixed/okay", or "bad".
"""

from typing import Dict, List, Optional
from movie_api import get_movie_data
from sentiment_model import analyze_reviews, get_sample_reviews


def generate_verdict(movie_data: Dict, reviews: List[Dict]) -> Dict:
    """
    Analyze a movie's reviews and generate a verdict.
    
    Args:
        movie_data: Dictionary containing movie details (title, year, vote_average, etc.)
        reviews: List of review dictionaries from TMDb
        
    Returns:
        Dictionary containing:
        - title: Movie title
        - year: Release year
        - tmdb_rating: TMDb average rating (0-10)
        - reviews_analyzed: Number of reviews analyzed
        - positive_percent: Percentage of positive reviews
        - negative_percent: Percentage of negative reviews
        - verdict: "Good", "Mixed/Okay", or "Mostly Negative"
        - verdict_explanation: Brief explanation of the verdict
        - sample_positive_reviews: List of sample positive review snippets
        - sample_negative_reviews: List of sample negative review snippets
    """
    # Analyze sentiment of all reviews
    sentiment_results = analyze_reviews(reviews)
    
    # Get movie rating (TMDb uses 0-10 scale)
    tmdb_rating = movie_data.get("vote_average", 0.0)
    positive_percent = sentiment_results["positive_percent"]
    
    # Determine verdict based on rating and sentiment
    # Rules:
    # - Good: rating >= 7.5 AND positive reviews >= 70%
    # - Mixed/Okay: rating between 5.5-7.5 OR positive between 40%-70%
    # - Mostly Negative: otherwise
    
    if tmdb_rating >= 7.5 and positive_percent >= 70:
        verdict = "Good"
        verdict_explanation = "Most viewers like this movie."
    elif (5.5 <= tmdb_rating < 7.5) or (40 <= positive_percent < 70):
        verdict = "Mixed/Okay"
        verdict_explanation = "Viewers have mixed opinions about this movie."
    else:
        verdict = "Mostly Negative"
        verdict_explanation = "Most viewers did not enjoy this movie."
    
    # Get sample reviews
    sentiments = sentiment_results["sentiments"]
    sample_positive = get_sample_reviews(reviews, sentiments, positive=True, count=2)
    sample_negative = get_sample_reviews(reviews, sentiments, positive=False, count=2)
    
    return {
        "title": movie_data.get("title", "Unknown"),
        "year": movie_data.get("year", "Unknown"),
        "tmdb_rating": round(tmdb_rating, 1),
        "reviews_analyzed": len(reviews),
        "positive_percent": sentiment_results["positive_percent"],
        "negative_percent": sentiment_results["negative_percent"],
        "neutral_percent": sentiment_results["neutral_percent"],
        "average_sentiment": round(sentiment_results["average_sentiment"], 2),
        "verdict": verdict,
        "verdict_explanation": verdict_explanation,
        "sample_positive_reviews": sample_positive,
        "sample_negative_reviews": sample_negative,
        "overview": movie_data.get("overview", "No overview available.")
    }


def analyze_movie(title: str) -> Optional[Dict]:
    """
    Main function to analyze a movie by title.
    
    Args:
        title: The movie title to analyze
        
    Returns:
        Dictionary with analysis results, or None if movie not found
        
    Raises:
        Exception: If there's an error fetching movie data
    """
    try:
        # Fetch movie data and reviews
        movie_data, reviews = get_movie_data(title)
        
        if not movie_data:
            return None
        
        if not reviews or len(reviews) == 0:
            # Return basic info even if no reviews
            return {
                "title": movie_data.get("title", "Unknown"),
                "year": movie_data.get("year", "Unknown"),
                "tmdb_rating": round(movie_data.get("vote_average", 0.0), 1),
                "reviews_analyzed": 0,
                "error": "No reviews found for this movie."
            }
        
        # Generate verdict
        result = generate_verdict(movie_data, reviews)
        return result
        
    except Exception as e:
        raise Exception(f"Error analyzing movie: {e}")

