import streamlit as st
import edge_tts
import asyncio
import io
from pydub import AudioSegment

st.set_page_config(page_title="Myanmar TTS Pro", layout="wide")
st.title("မြန်မာ TTS Pro (Smart Pause)")

# Sidebar Settings
with st.sidebar:
    st.header("Settings")
    voice = st.selectbox("Voice", ["my-MM-ThihaNeural", "my-MM-NilarNeural"])
    pitch = st.slider("Pitch (Hz)", -50, 50, 0)
    rate = st.slider("Speed (%)", -50, 100, 25)
    
    # (NEW) Pause Setting ထပ်ဖြည့်ခြင်း
    st.divider()
    pause_time = st.slider("Pause Time (ms)", 0, 2000, 500, step=100)
    st.caption("စာတစ်ကြောင်းနှင့် တစ်ကြောင်းကြား နားမည့်အချိန် (1000ms = 1 sec)")

# Main Input
text_input = st.text_area("စာရိုက်ထည့်ရန် (Enter ခေါက်ထားသည့် နေရာတိုင်းတွင် ရပ်ပါမည်):", height=200)

async def generate_segment(text, voice, rate, pitch):
    # စာကြောင်းတစ်ကြောင်းချင်းစီကို အသံထုတ်ပေးသည့် Function
    if not text.strip(): return None
    communicate = edge_tts.Communicate(text, voice, rate=f"{'+' if rate>=0 else ''}{rate}%", pitch=f"{'+' if pitch>=0 else ''}{pitch}Hz")
    
    # Byte အနေဖြင့် ပြန်ယူခြင်း
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data

if st.button("Generate Audio", type="primary"):
    if text_input:
        with st.spinner("Processing with Smart Pause..."):
            final_audio = AudioSegment.empty()
            silence = AudioSegment.silent(duration=pause_time) # သတ်မှတ်ထားသော အသံတိတ်ချိန်
            
            # စာကြောင်းများကို Enter ဖြင့် ခွဲလိုက်သည်
            lines = text_input.split('\n')
            
            # တစ်ကြောင်းချင်းစီ အသံထုတ်ပြီး ပေါင်းစပ်ခြင်း
            for line in lines:
                if line.strip():
                    audio_bytes = asyncio.run(generate_segment(line, voice, rate, pitch))
                    if audio_bytes:
                        segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
                        final_audio += segment + silence  # အသံ + တိတ်ဆိတ်ချိန် ပေါင်းထည့်
            
            # အသံဖိုင် Save ခြင်း
            buffer = io.BytesIO()
            final_audio.export(buffer, format="mp3")
            
        st.success("ပြီးပါပြီ!")
        st.audio(buffer, format="audio/mp3")
    else:
        st.warning("စာရိုက်ထည့်ပေးပါ")
