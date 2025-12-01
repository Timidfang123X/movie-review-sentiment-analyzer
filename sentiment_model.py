"""
Sentiment Analysis Module

This module provides functions to analyze the sentiment of movie reviews.
It uses TextBlob for simple and effective sentiment analysis.
"""

from textblob import TextBlob
from typing import List, Dict, Tuple


def analyze_review_sentiment(text: str) -> float:
    """
    Analyze the sentiment of a single review text.
    
    Args:
        text: The review text to analyze
        
    Returns:
        A sentiment score between -1.0 (very negative) and 1.0 (very positive)
    """
    if not text or len(text.strip()) == 0:
        return 0.0
    
    # Create a TextBlob object and get its polarity
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    return polarity


def analyze_reviews(reviews: List[Dict]) -> Dict:
    """
    Analyze sentiment for a list of reviews and compute statistics.
    
    Args:
        reviews: List of review dictionaries, each containing at least a "content" key
        
    Returns:
        Dictionary containing:
        - sentiments: List of sentiment scores for each review
        - average_sentiment: Average sentiment score
        - positive_count: Number of positive reviews (sentiment > 0.1)
        - negative_count: Number of negative reviews (sentiment < -0.1)
        - neutral_count: Number of neutral reviews
        - positive_percent: Percentage of positive reviews
        - negative_percent: Percentage of negative reviews
        - neutral_percent: Percentage of neutral reviews
    """
    if not reviews or len(reviews) == 0:
        return {
            "sentiments": [],
            "average_sentiment": 0.0,
            "positive_count": 0,
            "negative_count": 0,
            "neutral_count": 0,
            "positive_percent": 0.0,
            "negative_percent": 0.0,
            "neutral_percent": 0.0
        }
    
    sentiments = []
    
    # Analyze each review
    for review in reviews:
        content = review.get("content", "")
        if content:
            sentiment = analyze_review_sentiment(content)
            sentiments.append(sentiment)
    
    if len(sentiments) == 0:
        return {
            "sentiments": [],
            "average_sentiment": 0.0,
            "positive_count": 0,
            "negative_count": 0,
            "neutral_count": 0,
            "positive_percent": 0.0,
            "negative_percent": 0.0,
            "neutral_percent": 0.0
        }
    
    # Calculate statistics
    total_reviews = len(sentiments)
    average_sentiment = sum(sentiments) / total_reviews
    
    # Count positive, negative, and neutral reviews
    # Using thresholds: > 0.1 for positive, < -0.1 for negative
    positive_count = sum(1 for s in sentiments if s > 0.1)
    negative_count = sum(1 for s in sentiments if s < -0.1)
    neutral_count = total_reviews - positive_count - negative_count
    
    positive_percent = (positive_count / total_reviews) * 100
    negative_percent = (negative_count / total_reviews) * 100
    neutral_percent = (neutral_count / total_reviews) * 100
    
    return {
        "sentiments": sentiments,
        "average_sentiment": average_sentiment,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "neutral_count": neutral_count,
        "positive_percent": round(positive_percent, 1),
        "negative_percent": round(negative_percent, 1),
        "neutral_percent": round(neutral_percent, 1)
    }


def get_sample_reviews(reviews: List[Dict], sentiments: List[float], 
                       positive: bool = True, count: int = 2) -> List[Dict]:
    """
    Get sample reviews based on sentiment (most positive or most negative).
    
    Args:
        reviews: List of review dictionaries
        sentiments: List of sentiment scores corresponding to reviews
        positive: If True, return most positive reviews; if False, return most negative
        count: Number of sample reviews to return
        
    Returns:
        List of review dictionaries with highest (or lowest) sentiment scores
    """
    if not reviews or not sentiments or len(reviews) != len(sentiments):
        return []
    
    # Create list of (review, sentiment) tuples
    review_sentiment_pairs = list(zip(reviews, sentiments))
    
    # Sort by sentiment (descending for positive, ascending for negative)
    if positive:
        review_sentiment_pairs.sort(key=lambda x: x[1], reverse=True)
    else:
        review_sentiment_pairs.sort(key=lambda x: x[1])
    
    # Return top N reviews
    sample_reviews = []
    for review, sentiment in review_sentiment_pairs[:count]:
        if review.get("content", "").strip():
            sample_reviews.append({
                "content": review.get("content", ""),
                "author": review.get("author", "Anonymous"),
                "sentiment": sentiment
            })
    
    return sample_reviews

