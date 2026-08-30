# Movie Recommendation System

A Streamlit web app that recommends movies similar to a selected movie using a precomputed similarity model and poster data from TMDB.
https://movierecommendation-jpfaykpipwyswm4vsg5ure.streamlit.app/
## Features
- Movie recommendation based on similarity scores
- Poster fetching from TMDB
- Streamlit UI for selecting a movie and viewing recommendations

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your TMDB API key:
   ```env
   TMDB=your_api_key_here
   ```

4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Project Files
- `app.py` - Streamlit application
- `movies.pkl` - Movie dataset
- `similarity.pkl` - Precomputed movie similarity matrix
- `.env` - Local environment variables (not committed)

## Notes
- Keep your `.env` file private and do not commit it to version control.
- The app will show a placeholder poster if the API key is missing or the poster request fails.
