import streamlit as st
import time

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from services.short_generator import ShortGenerator
from services.video_downloader import VideoDownloader
from services.staging import Staging

def download_video(youtube_url,start_second):

    staging = Staging("tmp")
    st.session_state['staging_path']= staging.run()

    file_bytes,filepath,filename = VideoDownloader(youtube_url,start_second).run(st.session_state['staging_path'])

    st.session_state['video_downloaded'] = True
    st.session_state['video_filename'] = filename
    st.session_state['video_filepath'] = filepath
    st.session_state['video_bytes'] = file_bytes

def generate_short(video_filepath,start_second,end_second):
    file_bytes,filepath,filename = ShortGenerator(video_filepath,start_second,end_second).run(st.session_state['staging_path'])

    st.session_state['short_generated'] = True
    st.session_state['short_filename'] = filename
    st.session_state['short_filepath'] = filepath
    st.session_state['short_bytes'] = file_bytes

def restart_short_generated():
    if 'short_generated' in st.session_state:
        del st.session_state['short_generated']

st.title("Shorts Maker")

#1 inputs the youtube
youtube_url = st.text_input("Youtube URL:",placeholder="Enter here...")
st.button("Video Download", on_click=download_video,args=(youtube_url,0))

if 'video_downloaded' in st.session_state:
    st.video(st.session_state['video_bytes'])
    start_second = st.text_input("Seconds Start:",value="0:00",on_change=restart_short_generated)
    end_second = st.text_input("Seconds End:",placeholder="0:59",on_change=restart_short_generated)

    if 'short_generated' not in st.session_state and start_second and end_second:
        with st.spinner('Generating Short...'):
            generate_short(st.session_state['video_filepath'],start_second,end_second)
            st.success('Short Generated!')

    if 'short_generated' in st.session_state:
        st.download_button(label="Download Short",data=st.session_state['short_bytes'],file_name=st.session_state['short_filename'],mime='application/octet-stream')