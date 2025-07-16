import streamlit as st
import praw
import pandas as pd
import sqlite3
from textblob import TextBlob
from datetime import datetime
import time
import hashlib

# --- Config --- #
DB_NAME = "reddit_comments.db"
REDDIT_CLIENT_ID = ""
REDDIT_CLIENT_SECRET = ""
REDDIT_USER_AGENT = ""

# --- DB Setup --- #
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id TEXT PRIMARY KEY,
            post_id TEXT,
            body TEXT,
            score INTEGER,
            created_utc TEXT,
            sentiment REAL,
            sentiment_label TEXT
        )
    """)
    conn.commit()
    conn.close()

# --- Reddit API --- #
def reddit_auth():
    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

def get_post_id_from_url(url):
    try:
        parts = url.strip("/").split("/")
        idx = parts.index("comments")
        return parts[idx + 1]
    except Exception:
        return None

# --- Fetch Comments --- #
def extract_comments(reddit, post_id):
    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=0)
    comments = []
    for comment in submission.comments.list():
        comments.append({
            "id": hashlib.md5(comment.id.encode()).hexdigest(),
            "post_id": post_id,
            "body": comment.body,
            "score": comment.score,
            "created_utc": datetime.fromtimestamp(comment.created_utc).isoformat()
        })
    return comments

# --- Analyze + Store in SQLite --- #
def analyze_and_store(comments):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    inserted = 0

    for c in comments:
        blob = TextBlob(c['body'])
        sentiment = blob.sentiment.polarity
        label = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"

        try:
            cursor.execute("""
                INSERT INTO comments (id, post_id, body, score, created_utc, sentiment, sentiment_label)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                c['id'], c['post_id'], c['body'], c['score'], c['created_utc'], sentiment, label
            ))
            inserted += 1
        except sqlite3.IntegrityError:
            continue  # Skip duplicates

    conn.commit()
    conn.close()
    return inserted

# --- Load from SQLite --- #
def load_comments(post_id):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(
        "SELECT * FROM comments WHERE post_id = ? ORDER BY created_utc DESC", conn, params=(post_id,)
    )
    conn.close()
    return df

# --- Streamlit UI --- #
st.set_page_config(page_title="Reddit Sentiment (Historical)", layout="wide")
st.title("\U0001F4AC Reddit Comment Sentiment Analyzer with History")

post_url = st.text_input("Paste a Reddit Post URL", value="", placeholder="https://www.reddit.com/r/.../comments/...")
refresh_rate = st.slider("Auto-refresh every N seconds", 30, 300, 60)

if post_url:
    post_id = get_post_id_from_url(post_url)
    if post_id:
        reddit = reddit_auth()
        init_db()

        if "last_run" not in st.session_state or time.time() - st.session_state.last_run > refresh_rate:
            with st.spinner("Fetching and analyzing new comments..."):
                new_comments = extract_comments(reddit, post_id)
                new_count = analyze_and_store(new_comments)
                df = load_comments(post_id)

                st.session_state.df = df
                st.session_state.last_run = time.time()

        df = st.session_state.get("df", pd.DataFrame())

        st.success(f"\U0001F4BE Total stored comments: {len(df)} | \U0001F195 New this round: {new_count if 'new_count' in locals() else 0}")

        st.subheader("\U0001F4CA Sentiment Breakdown")
        st.bar_chart(df["sentiment_label"].value_counts())

        st.subheader("\U0001F4DD All Comments")
        st.dataframe(df[["body", "sentiment", "sentiment_label", "score", "created_utc"]], height=500)

        # --- Additional Insights --- #
        st.subheader("\U0001F4C8 Sentiment Over Time")
        df["created_dt"] = pd.to_datetime(df["created_utc"])
        sentiment_trend = df.resample('H', on='created_dt')["sentiment"].mean()
        st.line_chart(sentiment_trend)

        st.subheader("\U0001F4CA Comment Volume Over Time")
        comment_volume = df.resample('H', on='created_dt').size()
        st.area_chart(comment_volume)

        st.subheader("\U0001F6A8 Potential Toxic Comments (Negative & Downvoted)")
        toxic_df = df[(df["sentiment"] < -0.5) & (df["score"] < 1)]
        st.write(f"Found {len(toxic_df)} potentially toxic comments:")
        st.dataframe(toxic_df[["body", "sentiment", "score", "created_utc"]])

    else:
        st.error("\u274C Invalid Reddit post URL.")
else:
    st.info("\U0001F517 Enter a valid Reddit post URL to begin analysis.")
