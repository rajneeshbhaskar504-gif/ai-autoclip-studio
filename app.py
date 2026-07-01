import streamlit as st
import os
import subprocess

st.set_page_config(page_title="AI AutoClip Studio", page_icon="🎬", layout="wide")
st.title("🎬 AI AutoClip Studio - Long Video to Shorts")

uploaded_file = st.file_uploader("Apni horizontal video upload karein (MP4)", type=["mp4"])

def crop_and_cut(video_path, start_time, end_time, output_path):
    # FFmpeg formula to center-crop 16:9 into 9:16 vertical short
    cmd = f'ffmpeg -y -ss {start_time} -to {end_time} -i "{video_path}" -vf "crop=ih*9/16:ih" -c:a copy "{output_path}"'
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if uploaded_file is not None:
    with open("input_video.mp4", "wb") as f:
        f.write(uploaded_file.read())
    
    st.video("input_video.mp4")
    
    if st.button("🚀 Generate Short Clip"):
        with st.spinner("AI Crop chal raha hai..."):
            out_name = "output_short.mp4"
            
            # Example: 10th second se lekar 40th second tak ka short cut karega
            crop_and_cut("input_video.mp4", "00:00:10", "00:00:40", out_name)
            
            if os.path.exists(out_name):
                st.success("🔥 Aapka Short ready hai!")
                st.video(out_name)
                with open(out_name, "rb") as file:
                    st.download_button(label="📥 Download Short", data=file, file_name=out_name, mime="video/mp4")
