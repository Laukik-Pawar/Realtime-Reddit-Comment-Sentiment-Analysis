📊 Reddit Real-Time Comment Sentiment Analyzer
A real-time data engineering project that pulls Reddit comments from a post, performs sentiment analysis, stores them in a SQLite database, and displays historical insights through an interactive Streamlit dashboard.

🚀 Features
🔁 Live ETL Pipeline: Pulls fresh Reddit comments every minute using the Reddit API.
💬 Sentiment Analysis: Uses TextBlob to assign polarity and label (Positive, Negative, Neutral) to each comment.
🧠 Toxic Comment Detection: Flags highly negative, low-scoring comments.
📦 SQLite Storage: Persists all comments for historical trend analysis.
📈 Real-Time Dashboard:
  Streamlit-based interactive visualization of:
    Sentiment distribution
    Sentiment trend over time
    Comment volume trend
    Toxic comment insights

🧱 Architecture

Reddit API --> PRAW --> ETL --> SQLite --> Streamlit Dashboard

⚙️ Tech Stack
Component	       |   Technology
--------------------------------------
Data Source	     |    Reddit API (via PRAW)
Sentiment Engine |	  TextBlob (NLP)
Storage	         |    SQLite3
Visualization	   |    Streamlit
Language	       |    Python 

Run the app:
python -m streamlit run your_script_name.py
Paste a Reddit Post URL, and you're live!

🧠 How Sentiment Works
TextBlob returns a polarity score between -1 and +1:

0 → Positive 😄

= 0 → Neutral 😐

< 0 → Negative 😠

Each comment is analyzed and labeled accordingly.

📊 Use Cases
🔎 Brand monitoring on Reddit
🧪 Social listening and community mood analysis
🚩 Toxic content flagging
📈 Trend visualization over time

