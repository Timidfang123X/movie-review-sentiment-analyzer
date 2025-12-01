"""
Command-Line Interface for Movie Sentiment Analyzer

This is the main entry point for the application. Users can input a movie title
and receive a sentiment analysis report.
"""

from analyzer import analyze_movie
import sys


def truncate_text(text: str, max_length: int = 200) -> str:
    """
    Truncate text to a maximum length, adding ellipsis if needed.
    
    Args:
        text: The text to truncate
        max_length: Maximum length before truncation
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_report(result: dict) -> str:
    """
    Format the analysis result into a readable report.
    
    Args:
        result: Dictionary containing analysis results
        
    Returns:
        Formatted string report
    """
    # Check for errors
    if "error" in result:
        report = f"""
Movie: {result.get('title', 'Unknown')} ({result.get('year', 'Unknown')})
TMDb rating: {result.get('tmdb_rating', 0.0)} / 10

{result['error']}
"""
        return report
    
    # Build the main report
    report = f"""
{'=' * 60}
MOVIE SENTIMENT ANALYSIS REPORT
{'=' * 60}

Movie: {result.get('title', 'Unknown')} ({result.get('year', 'Unknown')})
TMDb rating: {result.get('tmdb_rating', 0.0)} / 10
Reviews analyzed: {result.get('reviews_analyzed', 0)}

Sentiment Breakdown:
  • Positive reviews: {result.get('positive_percent', 0.0)}%
  • Negative reviews: {result.get('negative_percent', 0.0)}%
  • Neutral reviews: {result.get('neutral_percent', 0.0)}%
  • Average sentiment score: {result.get('average_sentiment', 0.0)} (range: -1.0 to 1.0)

VERDICT: {result.get('verdict', 'Unknown').upper()} – {result.get('verdict_explanation', '')}
"""
    
    # Add sample positive reviews
    positive_reviews = result.get('sample_positive_reviews', [])
    if positive_reviews:
        report += "\n" + "-" * 60 + "\n"
        report += "Example Positive Reviews:\n"
        report += "-" * 60 + "\n"
        for i, review in enumerate(positive_reviews, 1):
            content = truncate_text(review.get('content', ''), 300)
            author = review.get('author', 'Anonymous')
            report += f"\n[{i}] By {author}:\n"
            report += f'"{content}"\n'
    
    # Add sample negative reviews
    negative_reviews = result.get('sample_negative_reviews', [])
    if negative_reviews:
        report += "\n" + "-" * 60 + "\n"
        report += "Example Negative Reviews:\n"
        report += "-" * 60 + "\n"
        for i, review in enumerate(negative_reviews, 1):
            content = truncate_text(review.get('content', ''), 300)
            author = review.get('author', 'Anonymous')
            report += f"\n[{i}] By {author}:\n"
            report += f'"{content}"\n'
    
    # Add movie overview
    overview = result.get('overview', '')
    if overview:
        report += "\n" + "-" * 60 + "\n"
        report += "Movie Overview:\n"
        report += "-" * 60 + "\n"
        report += f"{overview}\n"
    
    report += "\n" + "=" * 60 + "\n"
    
    return report


def main():
    """
    Main function to run the CLI interface.
    """
    print("\n" + "=" * 60)
    print("MOVIE SENTIMENT ANALYZER")
    print("=" * 60)
    print("\nThis tool analyzes movie reviews to determine if a movie is 'good'.")
    print("It uses TMDb ratings and sentiment analysis of user reviews.\n")
    
    # Get movie title from user
    while True:
        try:
            title = input("Enter a movie title (or 'quit' to exit): ").strip()
            
            if title.lower() in ['quit', 'exit', 'q']:
                print("\nThank you for using Movie Sentiment Analyzer!")
                sys.exit(0)
            
            if not title:
                print("Please enter a valid movie title.\n")
                continue
            
            print(f"\nAnalyzing '{title}'... Please wait.\n")
            
            # Analyze the movie
            result = analyze_movie(title)
            
            if not result:
                print(f"❌ Movie '{title}' not found. Please try a different title.\n")
                continue
            
            # Display the report
            report = format_report(result)
            print(report)
            
            # Ask if user wants to analyze another movie
            while True:
                another = input("Would you like to analyze another movie? (y/n): ").strip().lower()
                if another in ['y', 'yes']:
                    print()
                    break
                elif another in ['n', 'no']:
                    print("\nThank you for using Movie Sentiment Analyzer!")
                    sys.exit(0)
                else:
                    print("Please enter 'y' or 'n'.")
        
        except KeyboardInterrupt:
            print("\n\nThank you for using Movie Sentiment Analyzer!")
            sys.exit(0)
        
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please try again or check your API key in the .env file.\n")


if __name__ == "__main__":
    main()

