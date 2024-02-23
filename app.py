import streamlit as st
import os
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi 

client = OpenAI(api_key=st.secrets["OpenAI_api_key"])

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

# def generate_gemini_content(transcript_text,prompt):
    
#     model = genai.GenerativeModel("gemini-pro")
#     response = model.generate_content(prompt+transcript_text)
#     return response.text 
def get_response(prompt, messages, model="gpt-3.5-turbo"):
    messages.append({"role": 'user', "content": prompt})
    response = client.chat.completions.create(
        messages= messages,
        model = model
    )
    messages.append({
        "role": response.choices[0].message.role,
        "content": response.choices[0].message.content
    })
    return response.choices[0].message.content, messages

messages = []
messages.append({"role": "system", "content": "You are a helpful assistant."})

st.title("Youtube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter Youtube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)
    
if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)
    
    prompt = "I will provide you a transcription of a video, acknowledge the transcription and wait for instructions."
    _, messages = get_response(prompt, messages)
    length = len(transcript_text.split(" "))
    if length > 0:
        i = 0
        while i <= length:
            if i + 3000 <= length:
                prompt = transcript_text[i:i+3000]
            else:
                prompt = transcript_text[i:]
            i += 3000
            _, messages = get_response(prompt, messages)
        
        prompt = f"""Explore the multifaceted advantages of being a YouTube creator by leveraging the YouTube API and engaging in prompt engineering. Dive into the unique benefits that extend beyond content creation, such as community building, analytics-driven growth, monetization strategies, and harnessing the power of YouTube's vast ecosystem. Highlight the tools, insights, and opportunities that arise from integrating with the YouTube API, and delve into the ways creators can thrive in the dynamic landscape of online content creation. Uncover the perks that go beyond crafting compelling videos, emphasizing the broader spectrum of possibilities for success, influence, and innovation within the YouTube creator community
        Output Format:
        ## Summary : 
        <summary>
        ---
        ## Perks : 
        - Deep dive into ‘The sound of silence’ through the director’s analytical lens.
        - One of you from US will get a studio tour and meet the JOE team (secret gift waiting for you in the studio, get excited BRU).
        - tell me about the creator that how is perks are different from other creators ? 
        - Tell about how life style of creator that attracts the users 
        - Suggestion 5 
        - Suggestion 6 
        """
        perks,messages = get_response(prompt,messages)
        st.markdown(perks)
        # st.write(perks)
    else:
        st.write("No transcript data found for the video.")
        
        
