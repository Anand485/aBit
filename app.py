import streamlit as st 
from dotenv import load_dotenv
load_dotenv()

import os
import google.generativeai as genai 

from youtube_transcript_api import YouTubeTranscriptApi 

genai.configure(api_key=st.secrets['GOOGLE_API_KEY"])

prompt = """You are Youtube video sumaarizer.You will be taking the transcript text and summarizing the entire video"""

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        print(video_id)
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        return transcript
    
    except Exception as e:
        raise e 

def generate_gemini_content(transcript_text,prompt):
    
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text 

st.title("Youtube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter Youtube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)
    
if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)
    
    if transcript_text:
        summary = generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
        
