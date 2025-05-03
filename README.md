# 📽️ YouTube Insight Summarizer

An AI-powered Streamlit app that takes a YouTube video URL, extracts the transcript, and generates a **rich, structured summary** using **Google Generative AI** — complete with markdown formatting and LaTeX math rendering.

## ✨ Features

- Extracts transcripts from YouTube videos
- Generates detailed, topic-based summaries with examples
- Outputs math-heavy content using clean LaTeX blocks
- User-friendly interface built with Streamlit



## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/)
- [Google Generative AI (Gemini)](https://ai.google.dev/)
- [YouTube Transcript API](https://pypi.org/project/youtube-transcript-api/)
- Python 3.8+


## 📦 Installation

```bash
git clone https://github.com/your-username/YouTube-Insight-Summarizer.git
cd YouTube-Insight-S Usage

Once you have installed the dependencies, you can run the application locally using the following command in your terminal:

streamlit run main.pyummarizer

## 📤 Deployment / Development Notes

After modifying or adding new files (like `requirements.txt`), use the following Git commands to commit and push your changes:

```bash
git add requirements.txt
git commit -m "Add requirements.txt with all dependencies"
git push origin main  # or use your branch name if different

## ⚙️ Configuration
Before running the app, make sure to set up your Google Gemini API key. You can do this by creating a .env file in the project's root directory and adding your API key:

GOOGLE_API_KEY=YOUR_API_KEY
Replace YOUR_API_KEY with your actual Gemini API key.
