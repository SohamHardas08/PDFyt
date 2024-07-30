import streamlit as st
from googleapiclient.discovery import build
import requests
from dotenv import load_dotenv
import os
from text_extraction import *

# Load environment variables
load_dotenv()

# Function to search Google Custom Search API
def search_google(query, num_results=2):
    api_key = os.getenv('GOOGLE_API_KEY')
    cse_id = os.getenv('SEARCH_ENGINE_ID')
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': cse_id,
        'q': query,
        'num': num_results
    }
    response = requests.get(url, params=params)
    results = response.json()
    return results

# Function to search YouTube API
def search_youtube(query, num_results=4):
    api_key = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    request = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=num_results
    )
    response = request.execute()
    
    results = []
    for item in response['items']:
        if item['id']['kind'] == 'youtube#video':
            video_title = item['snippet']['title']
            video_id = item['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            results.append({'title': video_title, 'url': video_url})
        return results

# Streamlit app
st.title("Document Content Search App")
st.write("Upload a PDF file to extract content and search on Google and YouTube.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    extracted = extract("temp.pdf")
    tokens = tokenize(extracted)
    words = keywords(tokens)
    keyword_combinations = generate_combinations(words, num_combinations=2)
    additional_terms = st.text_input("Add some context to improve the search query like subject or domain (comma-separated):")
    
    if additional_terms:
        terms = [term.strip() for term in additional_terms.split(',')]
        search = queries(keyword_combinations, terms)
        search_query = ' '.join(search)

        st.write("## Google Search Results")
        google_results = search_google(search_query)
        for item in google_results.get('items', []):
            title = item['title']
            link = item['link']
            snippet = item['snippet']
            st.write(f"**Title:** {title}")
            st.write(f"**Link:** {link}")
            st.write(f"**Snippet:** {snippet}")
            st.write("---")

        # Search YouTube
        st.write("## YouTube Search Results")
        youtube_results = search_youtube(search_query)
        for result in youtube_results:
            st.write(f"**Title:** {result['title']}")
            st.write(f"**URL:** {result['url']}")
            st.write("---")
    else:
        st.write("Please add some context to improve the search query.")
        
        
        
