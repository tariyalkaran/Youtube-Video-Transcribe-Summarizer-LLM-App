# import streamlit as st
# from dotenv import load_dotenv

# load_dotenv()  ##load all the environement varibales
# import os
# import google.generativeai as genai

# from youtube_transcript_api import YouTubeTranscriptApi

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# prompt="""You are a Youtube video summarizer. You will be taking the transcript text and summarizing the entire video
# and providing the important summary in points within 250 words. Please provide the summary of the text given here : """

# ## getting the transcript data from yt video
# def extract_transcript_details(youtube_video_url):
#     try:
#         video_id=youtube_video_url.split("=")[1]
#         transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

#         transcript=""
#         for i in transcript_text:
#             transcript += " " + i["text"]

#         return transcript

#     except Exception as e:
#         raise e
        
# ## getting the summary based on Prompt from Google Gemini Pro
# def generate_gemini_content(transcript_text,prompt):

#     model=genai.GenerativeModel("gemini-pro")
#     response=model.generate_content(prompt+transcript_text)
#     return response.text


# st.title("YouTube Transcript to Detailed Notes Converter")
# youtube_link = st.text_input("Enter YouTube Video Link:")

# if youtube_link:
#     video_id=youtube_link.split("=")[1]
#     st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

# if st.button("Get Detailed Notes"):
#     transcript_text=extract_transcript_details(youtube_link)

#     if transcript_text:
#         summary=generate_gemini_content(transcript_text,prompt)
#         st.markdown("## Detailed Notes:")
#         st.write(summary)

import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()

# Configure Google Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for summarization
prompt = """
You are a Youtube video summarizer. You will take the transcript text and summarize the entire video,
providing the important summary in points within 250 words. Please provide the summary of the text given here:
"""

# Function to extract transcript details from YouTube video URL
def extract_transcript_details(youtube_video_url):
    try:
        # Validate if the YouTube URL contains "youtube.com/watch?v="
        if "youtube.com/watch?v=" not in youtube_video_url:
            st.error("Invalid YouTube URL. Please enter a valid YouTube video link.")
            return None

        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        st.error(f"Could not retrieve transcript: {e}")
        return None

# Function to generate summary content using Google Gemini API
def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"Error generating content: {e}")
        return None

# Streamlit UI
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

# Display the YouTube thumbnail if a valid link is entered
if youtube_link:
    try:
        video_id = youtube_link.split("=")[1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    except IndexError:
        st.error("Invalid YouTube URL format. Please ensure it is in the correct format.")

# Button to generate detailed notes
if st.button("Get Detailed Notes"):
    # Fetch transcript
    with st.spinner('Fetching transcript...'):
        transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        # Generate summary
        with st.spinner('Generating summary...'):
            summary = generate_gemini_content(transcript_text, prompt)

        # Display the summary if successful
        if summary:
            st.markdown("## Detailed Notes:")
            st.write(summary)
        else:
            st.error("Failed to generate summary.")
    else:
        st.error("Transcript could not be retrieved. Please check the video URL or try another video.")
