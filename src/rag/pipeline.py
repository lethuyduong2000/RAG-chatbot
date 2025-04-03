import re

from retriever import ChromaRetriever

class RAGPipeline:
    def __init__(self):
        self.retriever = ChromaRetriever()
        # self.generator = OpenAIGenerator()

    # def chat(self, query):
    #     """Runs full RAG retrieval + generation."""
    #     docs, _ = self.retriever.retrieve(query)
    #     context = "\n".join(docs) if docs else "No relevant information found."
    #     return self.generator.generate(context, query)
    # def chat(request: ChatRequest):
    #     query = request.query
    #     if not query:
    #         raise HTTPException(status_code=400, detail="Query is required")
    #     docs, metadatas = retrieve_relevant_docs(query)
    #     context = "\n".join(docs)
    #     response = generate_response(context, query)
    #     return {"response": response}

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