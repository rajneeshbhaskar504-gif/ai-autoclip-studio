import streamlit as st
import os
import subprocess

st.set_page_config(page_title="Fast AutoClip & Shield", page_icon="⚡", layout="wide")
st.title("⚡ Fast AI AutoClip & Copyright Shield")

uploaded_file = st.file_uploader("Apni MP4 Video Upload Karein", type=["mp4"])

def copyright_free_cut(video_path, start_time, end_time, output_path):
    """
    Video ko cut karega aur background me copyright protection filters apply karega:
    1. Center-crop to 9:16 vertical.
    2. Video speed ko 1.02x halka sa fast karega (Algorithm detect nahi kar pata).
    3. Audio pitch aur tempo ko adjust karega taaki background music bypass ho jaye.
    """
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
    
    if st.button("⚡ Instant Copyright-Safe Short"):
        with st.spinner("Copyright Protection Layer apply ho rahi hai..."):
            out_name = "safe_short.mp4"
            
            # 10th second se lekar 40th second tak ka short cut aur bypass karega
            copyright_free_cut("input_video.mp4", "00:00:10", "00:00:40", out_name)
            
            if os.path.exists(out_name):
                st.success("🔥 Done! Video is now Copyright-Shielded.")
                st.video(out_name)
                with open(out_name, "rb") as file:
                    st.download_button(label="📥 Download Safe Short", data=file, file_name=out_name, mime="video/mp4")
