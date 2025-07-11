# Website Summarizer Chatbot

A simple Python tool that summarizes the main content of any public website using LLMs, with a user-friendly Gradio chatbot interface.

## Features
- Enter any website URL and get a concise, markdown-formatted summary.
- Ignores navigation and irrelevant content for focused results.
- Uses Groq LLM API for high-quality summarization.
- Easy-to-use web interface powered by Gradio.

## Setup Instructions

### 1. Clone the Repository
```
git clone <repo-url>
cd <repo-folder>/brochure
```

### 2. Install Dependencies
Make sure you have Python 3.8+ installed. Install required packages:
```
pip install gradio requests beautifulsoup4 python-dotenv groq
```

### 3. Set Up Environment Variables
Create a `.env` file in the `brochure` directory and add your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

## How to Run the Gradio App
From the `brochure` directory, run:
```
python gradio_app.py
```
This will launch a local web server. Open the displayed URL (usually http://127.0.0.1:7860) in your browser.

## Example Usage
1. Enter a website URL (e.g., `https://en.wikipedia.org/wiki/OpenAI`).
2. The chatbot will return a summary of the main content.

## Troubleshooting
- **TypeError about function arguments:** Ensure `summarize_website_chatbot` in `gradio_app.py` accepts two arguments: `message, history`.
- **Unexpected keyword argument errors:** Remove unsupported arguments from `gr.ChatInterface` (e.g., `placeholder`, `retry_btn`, `undo_btn`).
- **Groq API errors:** Make sure your `.env` file is present and contains a valid `GROQ_API_KEY`.
- **Module not found:** Double-check that all dependencies are installed and you are running Python 3.8 or newer.


