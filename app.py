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
        
        prompt = f"""Now based on the above transcript provide me some perk ideas for my members.
        Output Format:
        ## Summary : 
        <summary>
        ---
        ## Perks : 
        - Tell me for personalized information about the creator.
        - Suggestion 2 
        - Suggestion 3 
        - Suggestion 4 
        """
        perks,messages = get_response(prompt,messages)
        st.markdown(perks)
        # st.write(perks)
    else:
        st.write("No transcript data found for the video.")
        
        
