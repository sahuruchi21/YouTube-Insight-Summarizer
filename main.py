import os
import streamlit as st
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import google.generativeai as genai
from google.generativeai.types import GenerationConfig


# Step 1: Load API key from .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ Missing GOOGLE_API_KEY in .env")
    st.stop()

# Step 2: Page config
st.set_page_config(page_title="YouTube Transcript Summarizer", layout="centered")

# Step 3: Configure Google Generative AI
genai.configure(api_key=api_key)

# Step 4: Set up generation config & select model
gen_config = GenerationConfig(temperature=0.2, max_output_tokens=4096)
models = genai.list_models()
model_names = [m.name for m in models if "generateContent" in m.supported_generation_methods]
default = "models/gemini-1.5-flash-latest"
default_index = model_names.index(default) if default in model_names else 0
selected_model = st.sidebar.selectbox("🛠️ Choose model:", model_names, index=default_index)

model = genai.GenerativeModel(
    model_name=selected_model,
    generation_config=gen_config
)

# Step 5: Helpers

def get_video_id(url: str) -> str:
    """Extract the YouTube video ID from a URL."""
    p = urlparse(url)
    query = parse_qs(p.query)
    return query.get("v", [None])[0]
def get_transcript_from_url(url: str) -> str:
    video_id = get_video_id(url)
    if not video_id:
        raise RuntimeError("❌ Invalid YouTube URL — no video ID found.")
    
    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcripts.find_transcript(['en'])  # prefer English
        segments = transcript.fetch()
        return " ".join(seg.text for seg in segments)

    except TranscriptsDisabled:
        raise RuntimeError("❌ Transcripts are disabled for this video.")
    except NoTranscriptFound:
        raise RuntimeError("❌ No transcript found for this video.")
    except Exception as e:
        raise RuntimeError(f"❌ Failed to fetch transcript: {str(e)}")


def generate_summary(text: str) -> str:
    """Generate enriched summary using Gemini model."""
    prompt = (
        "You are a knowledgeable and precise educational AI. A technical YouTube transcript is provided.\n\n"
        "Your job is to generate a well-structured, human-friendly enriched summary in **Markdown** with clean **LaTeX** math formatting.\n\n"
        "**Output Structure:**\n"
        "### 1. Overview\n"
        "- List all key topics discussed in bullet points.\n\n"
        "### 2. Detailed Explanation\n"
        "- For each topic:\n"
        "  - Use proper headings and subheadings.\n"
        "  - Define key terms and formulas.\n"
        "  - Show clean math using `$$...$$` (not inline `$...$` unless very short).\n"
        "  - Use clean matrix formatting. For example:\n"
        "    $$\n"
        "    \\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix}\n"
        "    $$\n"
        "  - Provide full and readable examples.\n"
        "  - Avoid messy LaTeX or line-breaking errors.\n\n"
        "### 3. Extra Notes\n"
        "- Include assumptions, tips, and real-world links.\n\n"
        "Here is the full transcript:\n"
        f"{text}\n\n"
        "Now generate the structured enriched summary as described."
    )
    response = model.generate_content(prompt)
    return response.text

def get_video_thumbnail(video_id: str) -> str:
    """Return the thumbnail URL of the YouTube video."""
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

# Step 6: Streamlit UI

st.title("📽️ YouTube Transcript to Enriched Summary")

video_url = st.text_input("🔗 Enter YouTube Video Link:")

if video_url:
    try:
        with st.spinner("⏳ Fetching transcript..."):
            vid = get_video_id(video_url)
            st.write(f"🔎 Video ID: `{vid}`")
            transcript = get_transcript_from_url(video_url)
            thumbnail_url = get_video_thumbnail(vid)
            st.image(thumbnail_url, use_container_width=True)

        with st.spinner(f"🤖 Generating enriched summary with `{selected_model}`..."):
            enriched_summary = generate_summary(transcript)

        st.subheader("🧠 Enriched Summary with Examples")
        st.markdown(enriched_summary, unsafe_allow_html=True)

    except Exception as err:
        st.error(str(err))

