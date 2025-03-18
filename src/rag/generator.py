import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("API_KEY")
genai.configure(api_key=GEMINI_API_KEY)  

class GenAIGenerator:
    def __init__(self, model="gemini-2.0-flash"):
        self.model = model  
        self.api_key = GEMINI_API_KEY 

    def generate(self, context, query):
        """Generates a response using GenAI."""
        prompt = f"""
        You are an e-commerce assistant. Answer customer queries about products using the provided context.
        If the context does not contain enough information, say 'I don't know'.
        Keep responses short and direct.

        Context: {context}
        Question: {query}
        Answer:
        """
        model = genai.GenerativeModel(self.model)
        print(f'=== prompt === {prompt}')
        response = model.generate_content(prompt)  

        return response.text.strip()
