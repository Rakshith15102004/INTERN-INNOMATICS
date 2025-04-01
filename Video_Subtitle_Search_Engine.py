import os
import whisper
import streamlit as st
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.qparser import QueryParser

# Ensure necessary directories exist
if not os.path.exists("index"):  
    os.mkdir("index")

# Function to extract subtitles using OpenAI Whisper
def extract_subtitles(video_path):
    model = whisper.load_model("base")
    result = model.transcribe(video_path)
    return result["segments"]  # List of timestamped text

# Define schema for subtitle indexing
schema = Schema(timestamp=NUMERIC(stored=True), text=TEXT(stored=True))

# Create index
if not os.path.exists("index/main"):  
    ix = create_in("index", schema)
else:
    ix = open_dir("index")

# Function to index subtitles
def index_subtitles(subtitles):
    ix = open_dir("index")
    writer = ix.writer()
    for segment in subtitles:
        writer.add_document(timestamp=int(segment["start"]), text=segment["text"])
    writer.commit()

# Function to search for subtitles
def search_subtitles(query):
    ix = open_dir("index")
    with ix.searcher() as searcher:
        parser = QueryParser("text", ix.schema)
        my_query = parser.parse(query)
        results = searcher.search(my_query)
        return [(r["timestamp"], r["text"]) for r in results]

# Streamlit UI
st.title("Video Subtitle Search Engine")

uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov", "mkv"])
if uploaded_file:
    video_path = "temp_video.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())
    
    st.write("Extracting subtitles... This may take a few minutes.")
    subtitles = extract_subtitles(video_path)
    index_subtitles(subtitles)
    st.success("Subtitles indexed successfully!")

query = st.text_input("Search for a phrase in the video")
if st.button("Search"):
    results = search_subtitles(query)
    if results:
        for timestamp, text in results:
            st.write(f"**Timestamp:** {timestamp} sec - {text}")
    else:
        st.write("No matching subtitles found.")
