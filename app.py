import streamlit as st
import streamlit.components.v1 as components
import speech_recognition as sr
import pandas as pd
from datetime import datetime
import os
import re
import random

st.set_page_config(
    page_title="English Speaking Practice Coach",
    page_icon="🎙️",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #111827 45%,
        #020617 100%
    );

    color: #f8fafc;
}

.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

.hero-card {
    background: rgba(255, 255, 255, 0.08);
    border: 0.5px solid rgba(255,255,255,0.08);
    border-radius: 28px;
    padding: 34px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.35);
    backdrop-filter: blur(12px);
    margin-bottom: 24px;
}

.hero-title {
    font-size: 46px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-subtitle {
    color: #cbd5e1;
    font-size: 18px;
}

            
            
.card {
    background: rgba(255, 255, 255, 0.09);
    border: 0.5px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 4px;
    box-shadow: 0 14px 40px rgba(0,0,0,0.28);
    margin-bottom: 20px;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 12px;
}

.topic-box {
    background: linear-gradient(135deg, #4f46e5, #2563eb);
    border-radius: 20px;
    padding: 22px;
    color: white;
    font-size: 22px;
    font-weight: 700;
    box-shadow: 0 12px 30px rgba(37, 99, 235, 0.35);
}

.small-muted {
    color: #cbd5e1;
    font-size: 15px;
}

.transcript-box {
    background: rgba(15, 23, 42, 0.85);
    border: 0.5px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 20px;
    font-size: 17px;
    line-height: 1.8;
}

.metric-card {
    background: rgba(15, 23, 42, 0.85);
    border: 0.5px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 18px;
    text-align: center;
}

.metric-value {
    font-size: 34px;
    font-weight: 800;
    color: #38bdf8;
}

.metric-label {
    color: #cbd5e1;
    font-size: 14px;
}

mark {
    background-color: #facc15;
    color: #111827;
    padding: 2px 6px;
    border-radius: 6px;
}

.stButton > button {
    width: 100%;

    height: 44px;

    white-space: nowrap;

    padding: 0 18px;

    border-radius: 12px;

    font-weight: 600;

    border: none;

    background: linear-gradient(135deg, #22c55e, #16a34a);

    color: white;

    margin-top: 8px;

    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 28px rgba(34, 197, 94, 0.28);
}

[data-testid="stAudioInput"] {
    background: rgba(255,255,255,0.08);
    padding: 16px;
    border-radius: 18px;
    border: 0.5px solid rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div class="hero-card">
    <div class="hero-title">🎙️ English Speaking Practice Coach 🎙️</div>
    <div class="hero-subtitle">
        Practice speaking English, record your answer, analyze fluency, detect filler words, and save your progress.
    </div>
</div>
""", unsafe_allow_html=True)

topics = [
    "Describe your daily routine.",
    "Talk about your favorite food.",
    "Describe your hometown.",
    "Talk about your dream job.",
    "Describe your best friend.",
    "Talk about a memorable day in your life.",
    "Describe your favorite movie.",
    "Talk about your gym routine.",
    "Describe a difficult challenge you faced.",
    "Talk about your future goals.",
    "Describe your favorite holiday.",
    "Talk about social media and its impact.",
    "Describe your favorite teacher.",
    "Talk about how you spend your weekends.",
    "Describe a skill you want to learn."
]

if "current_topic" not in st.session_state:
    st.session_state.current_topic = random.choice(topics)

if "speech_text" not in st.session_state:
    st.session_state.speech_text = ""

if "temp_audio_path" not in st.session_state:
    st.session_state.temp_audio_path = ""

if "audio_key" not in st.session_state:
    st.session_state.audio_key = 0

topic = st.session_state.current_topic

filler_patterns = [
    r"\bum+\b",
    r"\bu+h+\b",
    r"\ba+h+\b",
    r"\blike\b",
    r"\byou\s*know\b",
    r"\byouknow\b",
    r"\buknow\b",
    r"\buno\b",
    r"\bhuh+\b"
]

# -----------------------------
# TOPIC SECTION
# -----------------------------
left_col, right_col = st.columns([1.15, 0.85], gap="large")

with left_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📌 Today’s Speaking Topic</div>', unsafe_allow_html=True)

    topic_col, toggle_col = st.columns([5, 1])

    with topic_col:
        st.markdown(f'<div class="topic-box">{topic}</div>', unsafe_allow_html=True)

    with toggle_col:
        if st.button("🔁", help="Change topic"):
            st.session_state.current_topic = random.choice(topics)
            st.session_state.speech_text = ""

            if st.session_state.temp_audio_path and os.path.exists(st.session_state.temp_audio_path):
                os.remove(st.session_state.temp_audio_path)

            st.session_state.temp_audio_path = ""
            st.session_state.audio_key += 1
            st.rerun()

    st.markdown("""
    <p class="small-muted">
        Speak around <b>150–250 words</b>. Try to speak naturally, not memorized.
    </p>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⏳ Speaking Timer</div>', unsafe_allow_html=True)

    components.html(
        """
        <div style="
            background: linear-gradient(135deg, #020617, #1e293b);
            padding: 24px;
            border-radius: 22px;
            text-align: center;
            color: white;
            font-family: Arial, sans-serif;
            border: 1px solid rgba(255,255,255,0.12);
        ">
            <p style="margin: 0; font-size: 14px; color: #cbd5e1;">
                Recommended Time
            </p>

            <h1 id="timer" style="
                font-size: 58px;
                margin: 12px 0;
                letter-spacing: 4px;
                color: #38bdf8;
            ">02:00</h1>

            <button onclick="startTimer()" style="
                background: linear-gradient(135deg, #22c55e, #16a34a);
                color: white;
                border: none;
                padding: 11px 22px;
                border-radius: 999px;
                font-size: 15px;
                cursor: pointer;
                margin-right: 8px;
                font-weight: bold;
            ">
                ▶ Start
            </button>

            <button onclick="resetTimer()" style="
                background: linear-gradient(135deg, #ef4444, #dc2626);
                color: white;
                border: none;
                padding: 11px 22px;
                border-radius: 999px;
                font-size: 15px;
                cursor: pointer;
                font-weight: bold;
            ">
                ↺ Reset
            </button>

            <p style="font-size: 13px; color: #94a3b8; margin-top: 14px;">
                Start timer, then record below.
            </p>
        </div>

        <script>
            let totalTime = 120;
            let timeLeft = totalTime;
            let timerInterval = null;

            function updateDisplay() {
                let minutes = Math.floor(timeLeft / 60);
                let seconds = timeLeft % 60;

                document.getElementById("timer").innerHTML =
                    String(minutes).padStart(2, "0") + ":" + String(seconds).padStart(2, "0");
            }

            function startTimer() {
                clearInterval(timerInterval);

                timerInterval = setInterval(function() {
                    updateDisplay();

                    if (timeLeft <= 0) {
                        clearInterval(timerInterval);
                        document.getElementById("timer").innerHTML = "Time Up!";
                    }

                    timeLeft -= 1;
                }, 1000);
            }

            function resetTimer() {
                clearInterval(timerInterval);
                timeLeft = totalTime;
                updateDisplay();
            }

            updateDisplay();
        </script>
        """,
        height=245
    )

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# RECORDING SECTION
# -----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🎤 Record Your Voice</div>', unsafe_allow_html=True)

audio_file = st.audio_input(
    "Click record, speak, then stop recording manually",
    key=f"audio_{st.session_state.audio_key}"
)

st.markdown('</div>', unsafe_allow_html=True)

if audio_file is not None:
    temp_audio_path = "temp_recorded_audio.wav"

    with open(temp_audio_path, "wb") as f:
        f.write(audio_file.getbuffer())

    st.session_state.temp_audio_path = temp_audio_path

    recognizer = sr.Recognizer()

    with st.spinner("⏳ Please wait... Analyzing your speech..."):

        with sr.AudioFile(temp_audio_path) as source:
            audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio)

            st.success("Speech converted to text successfully.")
            st.session_state.speech_text = text

        except sr.UnknownValueError:
            st.error("I heard your voice, but could not convert it clearly to text.")

        except sr.RequestError:
            st.error("Speech recognition service error.")

# -----------------------------
# RESULT SECTION
# -----------------------------
if st.session_state.speech_text:
    text = st.session_state.speech_text

    highlighted_text = text

    for pattern in filler_patterns:
        highlighted_text = re.sub(
            pattern,
            lambda match: f"<mark>{match.group(0)}</mark>",
            highlighted_text,
            flags=re.IGNORECASE
        )

    words = text.split()
    word_count = len(words)

    lower_text = text.lower()

    filler_count = 0
    detected_fillers = []

    for pattern in filler_patterns:
        matches = re.findall(pattern, lower_text)

        filler_count += len(matches)

        if matches:
            detected_fillers.extend(matches)

    fluency_score = 10

    if filler_count > 10:
        fluency_score -= 4
    elif filler_count > 5:
        fluency_score -= 2

    if word_count < 50:
        fluency_score -= 2

    fluency_score = max(fluency_score, 1)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📝 Speech Transcript</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="transcript-box">{highlighted_text}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Speaking Analysis</div>', unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{word_count}</div>
            <div class="metric-label">Total Words</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{filler_count}</div>
            <div class="metric-label">Filler Words</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{fluency_score}/10</div>
            <div class="metric-label">Fluency Score</div>
        </div>
        """, unsafe_allow_html=True)

    if detected_fillers:
        st.info("Detected Fillers: " + ", ".join(detected_fillers))

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# BOTTOM ACTION BUTTONS
# -----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">⚙️ Actions</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.3,2.2,5], gap="small")

with col1:
    restart_btn = st.button("🔄 Restart")

with col2:
    save_btn = st.button("💾 Save Speech & Text")

st.markdown('</div>', unsafe_allow_html=True)

if restart_btn:
    st.session_state.speech_text = ""

    if (
        st.session_state.temp_audio_path
        and os.path.exists(st.session_state.temp_audio_path)
    ):
        os.remove(st.session_state.temp_audio_path)

    st.session_state.temp_audio_path = ""
    st.session_state.audio_key += 1

    st.rerun()

if save_btn:

    if st.session_state.speech_text == "":
        st.warning("No speech text to save yet.")

    elif st.session_state.temp_audio_path == "":
        st.warning("No audio recording found.")

    else:
        os.makedirs("saved_speeches", exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        saved_audio_path = f"saved_speeches/speech_{timestamp}.wav"
        saved_csv_path = "speech_history.csv"

        with open(st.session_state.temp_audio_path, "rb") as old_audio:
            audio_data = old_audio.read()

        with open(saved_audio_path, "wb") as new_audio:
            new_audio.write(audio_data)

        new_data = {
            "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "topic": topic,
            "speech_text": st.session_state.speech_text,
            "audio_file": saved_audio_path
        }

        new_df = pd.DataFrame([new_data])

        if os.path.exists(saved_csv_path):
            old_df = pd.read_csv(saved_csv_path)

            final_df = pd.concat(
                [old_df, new_df],
                ignore_index=True
            )

        else:
            final_df = new_df

        final_df.to_csv(saved_csv_path, index=False)

        if os.path.exists(st.session_state.temp_audio_path):
            os.remove(st.session_state.temp_audio_path)

        st.session_state.temp_audio_path = ""

        st.success("Speech and text saved successfully.")