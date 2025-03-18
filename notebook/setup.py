import pandas as pd
import logging
import ast
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Dict
import re
from dotenv import load_dotenv
import google.generativeai as genai
import os
import chromadb


load_dotenv()



GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
llm =  genai.GenerativeModel("gemini-2.0-flash")

chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")

def retriever(question):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode([question], convert_to_tensor=True).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=5
    )
    return results

def format_docs(docs):
    return "\n\n".join(['\n'.join([res['name'],res["description"]]) for res in docs["metadatas"][0]])



class RunnableChain:
    """Lớp bọc lambda function để hỗ trợ .invoke()"""
    def __init__(self, func):
        self.func = func

    def invoke(self, **kwargs):
        return self.func(**kwargs)

    def __or__(self, other):
        """Hỗ trợ chaining nhiều bước"""
        if not callable(other):
            raise TypeError(f"Cannot chain with type {type(other)}")

        # Ensure the next step is also a RunnableChain
        return RunnableChain(lambda **kwargs: other.invoke(self.func(**kwargs)))


class ChatPromptTemplate:
    def __init__(self, template: str):
        self.template = template
        self.variables = self.extract_variables(template)

    def extract_variables(self, template: str):
        return re.findall(r"\{(\w+)\}", template)

    def format(self, **kwargs) -> str:
        """Điền giá trị vào template"""
        missing_vars = [var for var in self.variables if var not in kwargs]
        if missing_vars:
            raise ValueError(f"Missing variables: {missing_vars}")

        return self.template.format(**kwargs)

    @classmethod
    def from_template(cls, template: str):
        return cls(template)

    def __or__(self, model):
        if not hasattr(model, "generate_content"):
            raise TypeError(f"Cannot chain with type {type(model)}")

        return RunnableChain(lambda **kwargs: model.generate_content(self.format(**kwargs)))
    

class RunnableFunction:
    def __init__(self, func):
        self.func = func  

    def __or__(self, other):
        if not callable(other):
            raise TypeError(f"Cannot chain with type {type(other)}")
        return RunnableFunction(lambda x: other(self.func(x)))

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def invoke(self, x):
        return self.func(x)


def str_output_parser(output):
    if hasattr(output, "text"):
        return output.text  # Nếu output có thuộc tính `.text`
    if isinstance(output, dict) and "text" in output:
        return output["text"]  # Nếu output là dict chứa key "text"
    return str(output)  # Chuyển tất cả về string


