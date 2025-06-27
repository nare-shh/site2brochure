import os
import requests 
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from groq import Groq
import gradio as gr

load_dotenv(override=True)
groq = Groq()

headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    def __init__(self , url):
        self.url = url
        response= requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

class WebsiteSummarizer:

    def create_system_prompt(self):
        return """You are an assistant that analyzes the contents of a website 
        and provides a short summary, ignoring text that might be navigation related. 
        Respond in markdown format with clear headings and bullet points where appropriate.
        Focus on the main content and key information."""

    def create_user_prompt(self, website):
        user_prompt = f"You are looking at a website titled '{website.title}'"
        user_prompt += "\n\nThe contents of this website is as follows. "
        user_prompt += "Please provide a concise summary of this website in markdown format. "
        user_prompt += "If it includes news, announcements, or key information, summarize these too.\n\n"
        
        text_content = website.text[:4000]
        if len(website.text) > 4000:
            text_content += "\n\n[Content truncated...]"
        
        user_prompt += text_content
        return user_prompt
        
        
        def create_messages(self, website):
            return [
                 {"role": "system", "content":create_system_prompt(website)},
                    {"role": "user", "content": create_user_prompt(website)}
         ]



    def summarize(self, url, model="llama-3.3-70b-versatile"):
        """Main function to summarize website"""
        
        # Check API availability
        if not self.api_available:
            return {
                "success": False,
                "error": f"Groq API not available: {self.api_error}",
                "summary": "",
                "title": "",
                "url": url
            }
        
        # Validate URL
        clean_url, url_error = self.validate_url(url)
        if url_error:
            return {
                "success": False,
                "error": url_error,
                "summary": "",
                "title": "",
                "url": url
            }
        
        try:
            # Fetch website
            website = Website(clean_url)
            
            if website.error:
                return {
                    "success": False,
                    "error": website.error,
                    "summary": "",
                    "title": "",
                    "url": clean_url
                }
            
            if not website.text.strip():
                return {
                    "success": False,
                    "error": "No content found on the website",
                    "summary": "",
                    "title": website.title,
                    "url": clean_url
                }
            
            # Generate summary using Groq
            response = self.groq.chat.completions.create(
                model=model,
                messages=self.create_messages(website),
                temperature=0.3,
                max_tokens=1000
            )
            
            summary = response.choices[0].message.content
            
            return {
                "success": True,
                "error": "",
                "summary": summary,
                "title": website.title,
                "url": clean_url
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating summary: {str(e)}",
                "summary": "",
                "title": "",
                "url": clean_url
            }

def summarize_website_chatbot(message, history):
    url = message
    summarizer = WebsiteSummarizer()
    result = summarizer.summarize(url)
    if result["success"]:
        return f"**Title:** {result['title']}\n\n**Summary:**\n{result['summary']}"
    else:
        return f"**Error:** {result['error']}"