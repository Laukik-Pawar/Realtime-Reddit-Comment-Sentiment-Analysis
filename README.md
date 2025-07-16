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

🔐 How to Get Reddit API Credentials
✅ Step 1: Create a Reddit Account (if you don't have one)
Go to https://www.reddit.com/register and sign up.
✅ Step 2: Visit Reddit Developer Portal
Go to https://www.reddit.com/prefs/apps
Scroll to the bottom and click “Create App” or “Create Another App”
✅ Step 3: Fill the App Details
name: A name for your app (e.g., Reddit Sentiment Analyzer)
App type: Select script
description: (Optional)
about url: Leave blank
redirect uri: Use http://localhost:8080
permissions: You don’t need to select anything here
Click “Create app”.
✅ Step 4: Get Your Credentials
After creating the app, you’ll see something like this:
personal use script   ->  YOUR_CLIENT_ID
client secret         ->  YOUR_CLIENT_SECRET
Now copy:
✅ client_id: The string under the “personal use script”
✅ client_secret: The “secret” field below it
✅ user_agent: A string like project_name:v1.0 (by /u/your_reddit_username)
✅ Example for Your Python Script

REDDIT_CLIENT_ID = "abc123XYZ"
REDDIT_CLIENT_SECRET = "yourclientsecret"
REDDIT_USER_AGENT = "reddit_sentiment:v1.0 (by /u/lucky4403)"
