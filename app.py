import streamlit as st
import os
import subprocess
import json
from openai import OpenAI

# OpenAI Client aapki direct API key ke sath configure kar diya hai
OΡΕΝΑΙ_KEY = "Sk-proj-lT4MAz_yswU73dukbi5k-UIE2nmV-_pYXQXlwEn9QV0NQMw7X-4uMqco_BJ8m7HyHb6bGfnCVQT3BlbkFJb_T4KxaKjT0UB81UpXFtyoHDA4TJ0ka5ykzeGaxNaTzp1HURXughohl610SRkeAyGzHyLGNocA"
client = OpenAI(api_key=OΡΕΝΑΙ_KEY)

st.set_page_config(page_title="AI Viral Clipper", page_icon="⚡", layout="wide")
st.title("⚡ AI AutoClip & Copyright Shield (90s Max)")
st.subheader("Lambi video se automatic 90 seconds tak ka viral part nikalne wala system")

uploaded_file = st.file_uploader("Apni MP4 Video Upload Karein", type=["mp4"])

def extract_audio(video_path, audio_path):
    cmd = f'ffmpeg -y -i "{video_path}" -vn -acodec libmp3lame -ar 16000 -ac 1 "{audio_path}"'
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def get_viral_timestamps(audio_file_path):
    # 1. Whisper se Transcribe karna
    with open(audio_file_path, "rb") as audio_file:
        transcript_response = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            response_format="verbose_json"
        )
    
    transcript_text = ""
    for segment in transcript_response.segments:
        transcript_text += f"[{segment['start']:.2f}s - {segment['end']:.2f}s]: {segment['text']}\n"
    
    # 2. GPT-4o Prompt 90 seconds tak ke high-energy content ke liye
    prompt = f"""
    You are an expert social media editor. Analyze this video transcript with timestamps.
    Find the single most viral, high-energy, or engaging continuous segment that is between 30 to 90 seconds long.
    Output MUST be strictly valid JSON format with keys 'start_seconds' and 'end_seconds'.
    Example: {{"start_seconds": 10.0, "end_seconds": 100.0}}
    
    Transcript:
    {transcript_text}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)

def copyright_free_cut(video_path, start_time, end_time, output_path):
    cmd = (
        f'ffmpeg -y -ss {start_time} -to {end_time} -i "{video_path}" '
        f'-vf "crop=ih*9/16:ih,setpts=0.98*PTS" '
        f'-filter_complex "atempo=1.02" '
        f'-c:v libx264 -crf 23 -preset ultrafast -c:a aac "{output_path}"'
    )
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if uploaded_file is not None:
    with open("input_video.mp4", "wb") as f:
        f.write(uploaded_file.read())
    
    st.video("input_video.mp4")
    
    if st.button("🚀 Find & Cut 90s Viral Short"):
        with st.spinner("AI video ko analyze karke 90s tak ka best part dhoond raha hai..."):
            extract_audio("input_video.mp4", "extracted_audio.mp3")
            
            try:
                timestamps = get_viral_timestamps("extracted_audio.mp3")
                start = timestamps.get("start_seconds", 0)
                end = timestamps.get("end_seconds", 90)
                
                st.info(f"🎯 AI ne {start}s se {end}s ke beech ka viral hook dhoond liya hai!")
                
                out_name = "viral_safe_90s_short.mp4"
                
                # Cut aur Shield layer render karna
                copyright_free_cut("input_video.mp4", str(start), str(end), out_name)
                
                if os.path.exists(out_name):
                    st.success("🔥 Aapka AI 90s Short ready hai!")
                    st.video(out_name)
                    with open(out_name, "rb") as file:
                        st.download_button(label="📥 Download 90s Short", data=file, file_name=out_name, mime="video/mp4")
            except Exception as e:
                st.error(f"Error: {e}")

