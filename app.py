import streamlit as st
import edge_tts
import asyncio

st.set_page_config(page_title="Myanmar TTS Pro", layout="wide")

st.title("မြန်မာ TTS Pro (Render Version)")

# Sidebar for Settings
with st.sidebar:
    st.header("Settings")
    voice = st.selectbox("Voice", ["my-MM-ThihaNeural", "my-MM-NilarNeural"])
    pitch = st.slider("Pitch (Hz)", -50, 50, 0)
    rate = st.slider("Speed (%)", -50, 100, 25)
    
    st.markdown("### Rules")
    rules_text = st.text_area("Pronunciation Rules", "မေတ္တာ=မျစ်တာ\nသစ္စာ=သစ်စာ")

# Main Area
text = st.text_area("စာရိုက်ထည့်ရန်:", height=200, placeholder="ဒီမှာ စာရိုက်ပါ...")

async def text_to_speech(text, voice, rate, pitch):
    # Rules Application
    for line in rules_text.split('\n'):
        if '=' in line:
            k, v = line.split('=')
            text = text.replace(k.strip(), v.strip())
            
    communicate = edge_tts.Communicate(text, voice, rate=f"{'+' if rate>=0 else ''}{rate}%", pitch=f"{'+' if pitch>=0 else ''}{pitch}Hz")
    await communicate.save("output.mp3")

if st.button("Generate Audio", type="primary"):
    if text:
        with st.spinner("အသံထုတ်နေသည်..."):
            asyncio.run(text_to_speech(text, voice, rate, pitch))
            
        st.success("ပြီးပါပြီ!")
        audio_file = open("output.mp3", "rb")
        st.audio(audio_file.read(), format="audio/mp3")
    else:
        st.warning("စာရိုက်ထည့်ပေးပါ")
