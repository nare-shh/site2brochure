import gradio as gr
from main import WebsiteSummarizer

def summarize_website_chatbot(message, history):
    url = message
    summarizer = WebsiteSummarizer()
    result = summarizer.summarize(url)
    if result["success"]:
        return f"**Title:** {result['title']}\n\n**Summary:**\n{result['summary']}"
    else:
        return f"**Error:** {result['error']}"

with gr.Blocks() as demo:
    gr.Markdown("# Website Summarizer Chatbot\nEnter a website URL to get a concise summary.")
    chatbot = gr.ChatInterface(
        fn=summarize_website_chatbot
    )

demo.launch() 