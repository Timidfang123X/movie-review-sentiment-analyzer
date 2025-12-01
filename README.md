# Movie Sentiment Analyzer

A Python project that answers the question: **"Is this movie good?"** by combining official movie ratings from The Movie Database (TMDb) with sentiment analysis of user reviews.

## What It Does

This project uses a two-pronged approach to evaluate movies:

1. **Official Ratings**: Fetches the average rating from TMDb (a popular movie database) on a scale of 0-10.
2. **Sentiment Analysis**: Analyzes the text of user reviews using natural language processing to determine if reviews are positive, negative, or neutral.

By combining these two signals, the program generates a verdict: "Good", "Mixed/Okay", or "Mostly Negative". It also provides sample positive and negative reviews so you can see what viewers are actually saying.

## How It Works

The project is structured into several modules:

- **`movie_api.py`**: Handles all interactions with the TMDb API (searching for movies, fetching ratings and reviews)
- **`sentiment_model.py`**: Uses TextBlob to analyze the sentiment of review text
- **`analyzer.py`**: Combines the data and applies logic to generate a final verdict
- **`cli.py`**: Provides a simple command-line interface for users

## Setup Instructions

### 1. Get a TMDb API Key

1. Go to [https://www.themoviedb.org/](https://www.themoviedb.org/)
2. Create a free account (it's completely free)
3. Navigate to **Settings** → **API**
4. Click **Request an API Key**
5. Select "Developer" as the type
6. Fill out the simple form (you can say it's for personal/educational use)
7. Copy your API key (it looks like: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)

### 2. Install Dependencies

Make sure you have Python 3.7 or higher installed. Then install the required packages:

```bash
pip install -r requirements.txt
```

This will install:
- `requests` - for making API calls to TMDb
- `python-dotenv` - for loading your API key from a `.env` file
- `textblob` - for sentiment analysis (this will also download the necessary language data)

### 3. Configure Your API Key

1. Copy `config_example.env` to `.env`:
   ```bash
   cp config_example.env .env
   ```
   (On Windows, you can use: `copy config_example.env .env`)

2. Open `.env` in a text editor and replace `your_api_key_here` with your actual TMDb API key:
   ```
   TMDB_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
   ```

### 4. Run the Program

```bash
python cli.py
```

You'll be prompted to enter a movie title. Try some examples:
- "The Dark Knight"
- "Inception"
- "Inside Out 2"
- "The Matrix"

## Example Output

```
============================================================
MOVIE SENTIMENT ANALYSIS REPORT
============================================================

Movie: The Dark Knight (2008)
TMDb rating: 9.0 / 10
Reviews analyzed: 45

Sentiment Breakdown:
  • Positive reviews: 88.9%
  • Negative reviews: 6.7%
  • Neutral reviews: 4.4%
  • Average sentiment score: 0.75 (range: -1.0 to 1.0)

VERDICT: GOOD – Most viewers like this movie.

------------------------------------------------------------
Example Positive Reviews:
------------------------------------------------------------

[1] By MovieFan123:
"Absolutely loved the emotional depth and visuals. One of the best superhero movies ever made..."

[2] By CinemaLover:
"Brilliant storytelling and incredible performances. Heath Ledger's Joker is unforgettable..."

------------------------------------------------------------
Example Negative Reviews:
------------------------------------------------------------

[1] By Critic42:
"Thought it was overrated. Too long and some parts dragged..."

------------------------------------------------------------
Movie Overview:
------------------------------------------------------------
Batman raises the stakes in his war on crime. With the help of Lt. Jim Gordon and District Attorney Harvey Dent, Batman sets out to dismantle the remaining criminal organizations...
============================================================
```

## Project Structure

```
movie_sentiment/
├── movie_api.py          # TMDb API integration
├── sentiment_model.py    # Sentiment analysis functions
├── analyzer.py           # Verdict generation logic
├── cli.py                # Command-line interface
├── config_example.env    # Example environment file
├── .env                  # Your API key (not in git)
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Research-Style Notes

### Sentiment vs. Numeric Ratings

This project reveals an interesting phenomenon: **sentiment analysis and numeric ratings don't always agree**. For example:
- A movie might have a high TMDb rating (8.5/10) but only 60% positive reviews (mixed sentiment)
- Conversely, a movie with a lower rating (6.5/10) might have 80% positive reviews (enthusiastic fans)

This happens because:
- **Numeric ratings** reflect the average of all votes, including neutral ones
- **Sentiment analysis** focuses on the emotional tone of written reviews, which tend to be more polarized (people write reviews when they feel strongly)

### Limitations

1. **Limited Review Data**: TMDb may not have many reviews for newer or obscure movies. The analysis is only as good as the available data.

2. **Sarcasm and Irony**: Sentiment analysis can struggle with sarcasm. A review saying "Oh great, another superhero movie" might be classified as positive even though it's negative.

3. **Reviewer Bias**: People who write reviews tend to have stronger opinions (either very positive or very negative) than the average viewer. This can skew the sentiment distribution.

4. **Language Limitations**: The current model (TextBlob) works best with English text and may not handle slang, emojis, or non-English reviews well.

5. **Context Missing**: Short reviews like "meh" or "okay" might be misclassified, and the model doesn't understand movie-specific context (e.g., "predictable" is negative for a thriller but might be fine for a children's movie).

### Ideas for Future Work

1. **Advanced NLP Models**: Replace TextBlob with more sophisticated models like:
   - BERT-based sentiment models from Hugging Face
   - RoBERTa fine-tuned on movie reviews
   - Models trained specifically on entertainment content

2. **Aspect-Based Sentiment**: Instead of overall sentiment, analyze specific aspects:
   - Acting quality
   - Plot/story
   - Visual effects
   - Pacing

3. **Web Interface**: Build a simple web app using Flask or Streamlit so users don't need to use the command line.

4. **TV Shows Support**: Extend the project to analyze TV series and individual episodes.

5. **Comparison Tool**: Allow users to compare two movies side-by-side.

6. **Historical Analysis**: Track how sentiment changes over time as more reviews come in.

7. **Genre-Specific Models**: Train or fine-tune models for different genres (horror, comedy, drama) since what makes a "good" review varies by genre.

8. **Multi-language Support**: Add support for analyzing reviews in multiple languages.

## Troubleshooting

**"TMDB_API_KEY not found"**: Make sure you created a `.env` file (not just `config_example.env`) and added your API key.

**"Movie not found"**: Try using the exact title as it appears on TMDb, or try a more specific search (e.g., "The Dark Knight 2008" instead of just "Dark Knight").

**"No reviews found"**: Some movies, especially very new or obscure ones, may not have user reviews on TMDb yet.

**Import errors**: Make sure you installed all dependencies with `pip install -r requirements.txt`. If TextBlob gives errors, you may need to download its language data: `python -m textblob.download_corpora`

## License

This is an educational project. Feel free to use and modify it for learning purposes.

## Acknowledgments

- [The Movie Database (TMDb)](https://www.themoviedb.org/) for providing the free API
- TextBlob for the sentiment analysis library

